# Digit classification through scattering medium, using vision_transformer
# Compare direct_classification VS reconstruction+classification
import argparse, os, h5py, datetime, math, random
import torch, torchvision, pytorch_msssim, vit_pytorch
import pytorch_lightning as pl
from torchvision import transforms
from torchmetrics.functional import pearson_corrcoef

parser = argparse.ArgumentParser()
parser.add_argument("--dataset_size", type=int,   default=20000, help="Dataset_size")
parser.add_argument("--testset_size", type=int,   default=500,   help="Testset_size")
parser.add_argument("--dataset_class",type=int,   default=10,    help="Dataset class numbers, 10 for MNIST")
parser.add_argument("--batch_size",   type=int,   default=256,   help="Batch_size in torch.utils.data.DataLoader")
parser.add_argument("--num_workers",  type=int,   default=6,     help="Number of cpu threads in torch.utils.data.DataLoader")
parser.add_argument("--epochs",       type=int,   default=10,    help="Epochs during training")
parser.add_argument("--img_size",     type=int,   default=32,    help="Image_size")
parser.add_argument("--spk_size",     type=int,   default=256,   help="Speckle_size")
parser.add_argument("--crop_or_down", type=int,   default=0,     help="For spk_size != 256, crop_ROI_block_choose(>=0) or downsample(-1)")
parser.add_argument("--lr",         type=float,   default=1e-4,  help="Adam: learning rate for generator, default 0.0001")
parser.add_argument("--vit_depth",    type=int,   default=4,     help="Number of Transformer blocks")
parser.add_argument("--vit_dim",      type=int,   default=1024,  help="Last dimension of output tensor after linear transformation")
parser.add_argument("--network",      type=int,   default=0,     help="Choose network, 0:Transformer, 2:Complex_FC+Classifier")
parser.add_argument("--save_model",   type=int,   default=0,     help="Save model, default:0-Disable, 1-Enable")
parser.add_argument("--dataset_path",type=str,   default="MNIST_tag.h5", help="Dataset path")
opt = parser.parse_args()

def normalization(image): # normalize to [0,1]
    Min = image.min(-2,keepdims=True)[0].min(-1,keepdims=True)[0]
    Max = image.max(-2,keepdims=True)[0].max(-1,keepdims=True)[0]
    image = (image-Min)/(Max-Min)
    image = torch.nan_to_num(image)
    if torch.isinf(image).sum()!=0: print(f'warning:inf {torch.isinf(image).sum()}')
    if torch.isnan(image).sum()!=0: print(f'warning:nan {torch.isnan(image).sum()}')
    return image

def autocorrelation(spk): # speckle_autocorrelation
    # Ref https://github.com/qhzhang95/PEACE_Speckle/blob/main/1_read%20the%20raw%20image%20and%20calculate%20the%20autocorrelations.ipynb
    spk = (spk-spk.min())/(spk.max()-spk.min()) # normalization
    at = torch.fft.fft2(spk).abs().pow(2) # power spectrum
    at = torch.fft.ifftshift(torch.fft.ifft2(at))/spk.shape[0]/spk.shape[1] # autocorrelation
    at = (torch.abs(at)-torch.mean(spk)**2)/(torch.mean(spk**2)-(torch.mean(spk))**2) # 
    at = at - (torch.mean(at)).min() # subtract background
    return at

def entropy(x,bit=16): # derive entropy of input
    x = torch.ceil(x*2**bit)
    _,count = torch.unique(x,return_counts=True)
    count   = count/count.sum()
    result  = -(count*torch.log2(count)).sum()
    return result

class MNIST_Net(torch.nn.Module): # Input is image N*1*28*28 [0,255]
    def __init__(self):
        super(MNIST_Net, self).__init__()
        self.conv1, self.conv2 = torch.nn.Conv2d(1, 10, kernel_size=5), torch.nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop, self.fc1, self.fc2 = torch.nn.Dropout2d(), torch.nn.Linear(320, 50), torch.nn.Linear(50, 10)
    def forward(self, x):
        x = torch.nn.functional.relu(torch.nn.functional.max_pool2d(self.conv1(x), 2))
        x = torch.nn.functional.relu(torch.nn.functional.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = torch.nn.functional.relu(self.fc1(x.view(-1, 320)))
        x = torch.nn.functional.dropout(x, training=self.training)
        return torch.nn.functional.log_softmax(self.fc2(x), dim=1)

class DataSet2(torch.utils.data.Dataset): # Load data in memory before training to speed up
    def __init__(self,dataset_path, dataset_size = 2000, test_dataset_size = 200, train=False , shuffle = False):
        train_dataset_size, step = dataset_size - test_dataset_size, int(dataset_size/test_dataset_size-1)
        test_dataset_sampler, train_dataset_sampler = list(range(1,dataset_size,step))[:test_dataset_size], list(range(0, dataset_size))
        for i in test_dataset_sampler: train_dataset_sampler.remove(i) # dataset_sampler is used to sample from h5 file
        self.sampler = train_dataset_sampler if train else test_dataset_sampler
        self.dataset, self.dataset_path = h5py.File(f"/home/frank/speckle_data/{dataset_path}",'r'), dataset_path
        self.speckle, self.image = self.dataset['speckle'][self.sampler], self.dataset['image'][self.sampler]
        if opt.dataset_class == 10: self.tag = self.dataset['tag'][self.sampler]

    def __len__(self): return len(self.sampler)
    def __getitem__(self, item):
        speckle, image, tag = torch.tensor(self.speckle[item]), torch.tensor(self.image[item]), torch.tensor(self.tag[item]).float()
        if opt.spk_size != 256:
            if opt.crop_or_down == -1: speckle = torch.nn.AvgPool2d(kernel_size=256//opt.spk_size)(speckle.unsqueeze(0)).squeeze()
            else:
                in_dim_start_x  = opt.crop_or_down // (256//opt.spk_size) * opt.spk_size
                in_dim_start_y  = opt.crop_or_down * opt.spk_size - opt.crop_or_down // (256//opt.spk_size) * (256//opt.spk_size) * opt.spk_size
                speckle = speckle[in_dim_start_x:in_dim_start_x+opt.spk_size, in_dim_start_y:in_dim_start_y+opt.spk_size]
        if opt.img_size == 32: image = torch.nn.AvgPool2d(kernel_size=4)(image.unsqueeze(0)).squeeze()
        if opt.img_size == 64: image = torch.nn.AvgPool2d(kernel_size=2)(image.unsqueeze(0)).squeeze()
        return speckle.unsqueeze(0), image.unsqueeze(0), tag

class Model(pl.LightningModule):
    def __init__(self):
        super(Model, self).__init__()
        self.lr, self.training_step_outputs, self.validation_step_outputs = opt.lr, [], []
        if opt.network == 0: # Ref: Better plain ViT baselines for ImageNet-1k
            self.vit = vit_pytorch.ViT(image_size = opt.spk_size, patch_size = opt.spk_size, num_classes = opt.dataset_class,
            dim = opt.vit_dim, depth = opt.vit_depth, heads = 16, mlp_dim = 2048, channels = 1, dropout = 0.1, emb_dropout = 0.1)
            # image_size: Image size. 
            # patch_size: Number of patches. image_size must be divisible by patch_size.
            # The number of patches is: n = (image_size // patch_size) ** 2 and n must be greater than 16.
            # num_classes: Number of classes to classify.
            # dim: Last dimension of output tensor after linear transformation.
            # depth: Number of Transformer blocks.
            # heads: Number of heads in Multi-head Attention layer.
            # mlp_dim: Dimension of the MLP (FeedForward) layer.
            # channels: Number of image's channels.
            # dropout: Dropout rate.
            # emb_dropout: Embedding dropout rate.

        if opt.network == 2: # use complex fully connected layer for image retrieval from speckles
            self.mnist_net = torch.load('/home/frank/data/model_mnist.pth').eval().to(self.device)
            self.in_dim, self.out_dim = opt.spk_size, opt.img_size
            self.layer = torch.nn.Linear(self.in_dim*self.in_dim, self.out_dim*self.out_dim).to(torch.complex64)

    def forward(self,x):
        if opt.network == 0:
            return self.vit(x)
        if opt.network == 2:
            x = x.reshape(-1, self.in_dim*self.in_dim).to(torch.complex64)
            x = self.layer(x).abs().reshape(-1, 1, self.out_dim, self.out_dim)
            return x

    def get_loss(self, batch, batch_idx):
        speckle, image, tag = batch
        model_output = self.forward(speckle)
        if opt.network == 0:
            loss = torch.nn.functional.binary_cross_entropy_with_logits(model_output, tag)
            predicted_tag = model_output
        if opt.network == 2:
            pcc  = pearson_corrcoef(model_output.reshape(-1,self.out_dim*self.out_dim).t(), image.reshape(-1,self.out_dim*self.out_dim).t())
            loss = torch.nn.functional.mse_loss(model_output, image).mean() - pcc.mean()
            predicted_tag = self.mnist_net(255*model_output[:,:,2:30,2:30])
        return loss.cpu(), predicted_tag.cpu()

    def training_step(self, batch, batch_idx):
        loss, _ = self.get_loss(batch, batch_idx)
        self.log("train_loss", loss)
        self.training_step_outputs.append([loss])
        return loss

    def on_train_epoch_end(self):
        loss = torch.tensor([i for i in self.training_step_outputs])
        self.training_step_outputs.clear()
        self.log("loss_mean/train_loss_mean", loss.mean())

    def validation_step(self, batch, batch_idx):
        speckle, image, tag = batch
        with torch.no_grad(): loss, predicted_tag = self.get_loss(batch, batch_idx)
        self.log("val_loss", loss)
        self.validation_step_outputs.append([predicted_tag.cpu(), tag.cpu(), loss.cpu(), speckle.cpu(), image.cpu()])

    def on_validation_epoch_end(self):
        predicted_tag, expected_tag = torch.cat([i[0] for i in self.validation_step_outputs]), torch.cat([i[1] for i in self.validation_step_outputs])
        predicted_tag, expected_tag = predicted_tag.data.max(1, keepdim=True)[1], expected_tag.data.max(1, keepdim=True)[1]
        Accruacy = (predicted_tag == expected_tag).sum()/expected_tag.shape[0]
        print(f"Epoch {self.current_epoch} Accuracy = {100*Accruacy:.2f}%"), self.log("val_accuracy", 100*Accruacy)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.lr)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, opt.epochs)
        return [optimizer], [scheduler]

if __name__ == "__main__":
    train_loader = torch.utils.data.DataLoader(DataSet2(opt.dataset_path, opt.dataset_size, opt.testset_size, train=True ), batch_size=opt.batch_size, num_workers=6, shuffle=False)
    val_loader   = torch.utils.data.DataLoader(DataSet2(opt.dataset_path, opt.dataset_size, opt.testset_size, train=False), batch_size=opt.batch_size, num_workers=6, shuffle=False)
    pl.seed_everything(1, workers=True) # Set random seeds before training
    model = Model()
    tensor_board_path = f"{datetime.datetime.now().strftime('%b%d_%H-%M-%S')}" # path for recording
    tb_logger = pl.loggers.TensorBoardLogger("runs/", name=f"Classifier_{tensor_board_path}")
    torch.set_printoptions(threshold=100000), print(f"tb_logger_folder runs/{tensor_board_path}")
    lr_monitor = pl.callbacks.LearningRateMonitor(logging_interval='step') # lr-Adam in tensorboard
    trainer = pl.Trainer(max_epochs=opt.epochs, log_every_n_steps=1, accelerator="auto", logger=tb_logger, enable_checkpointing=opt.save_model, callbacks=[lr_monitor], enable_progress_bar=False)
    trainer.fit (model, train_loader, val_loader) # Training Speckle Transformer
