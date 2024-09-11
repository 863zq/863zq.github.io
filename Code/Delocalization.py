# Delocalized information in optical speckles: an entropy analysis
import argparse, os, h5py, datetime, math, random
import torch, torchvision, pytorch_msssim, vit_pytorch
import pytorch_lightning as pl
from torchvision import transforms
from torchmetrics.functional import pearson_corrcoef, structural_similarity_index_measure, peak_signal_noise_ratio

parser = argparse.ArgumentParser()
parser.add_argument("--dataset_path", type=str,   default='speckle_dataset.h5', help="Dataset_path")
parser.add_argument("--epochs",       type=int,   default=50,    help="Number of epochs of training")
parser.add_argument("--batch_size",   type=int,   default=16,    help="Don't change batch_size")
parser.add_argument("--dataset_size", type=int,   default=2000,  help="Size of the dataset")
parser.add_argument("--testset_size", type=int,   default=200,   help="Size of the testset")
parser.add_argument("--lr",           type=float, default=1e-4,  help="Adam learning rate for generator, default 0.0001")
parser.add_argument("--img_size",     type=int,   default=64,    help="Resolution of output image  128x128, 64x64, or 32x32")
parser.add_argument("--spk_size",     type=int,   default=128,   help="Resolution of input speckle 256x256, 128x128, 64x64, or 32x32")
parser.add_argument("--block_choose", type=int,   default=0,     help="Choose sub_block from dwon_sampled speckles")
parser.add_argument("--model_choose", type=int,   default=1,     help="Choose model, 1:FC, 3:Vision-Transformer")
parser.add_argument("--save_model",   type=bool,  default=False, help="Save model by enable_checkpoin), 0:False, 1:True")
parser.add_argument("--loss_pcc",     type=float, default=0.8,   help="loss = loss_mse-opt.loss_pcc*loss_pcc-opt.loss_ssim*loss_ssim")
parser.add_argument("--loss_ssim",    type=float, default=0.8,   help="loss = loss_mse-opt.loss_pcc*loss_pcc-opt.loss_ssim*loss_ssim")
parser.add_argument("--optimizer",    type=int,   default=1,     help="PyTorch Optimizer (Adam is better), 1:Adam, 0:SGD")
opt = parser.parse_args()

def autocorrelation(spk): 
    # Ref https://github.com/qhzhang95/PEACE_Speckle/blob/main/1_read%20the%20raw%20image%20and%20calculate%20the%20autocorrelations.ipynb
    spk = (spk-spk.min())/(spk.max()-spk.min()) # normalization
    at = torch.fft.fft2(spk).abs().pow(2)
    at = torch.fft.ifftshift(torch.fft.ifft2(at))/spk.shape[0]/spk.shape[1]
    at = (torch.abs(at)-torch.mean(spk)**2)/(torch.mean(spk**2)-(torch.mean(spk))**2)
    at = at - (torch.mean(at)).min() # subtract background
    return at
def normalization(x): # normalize to [0,1]
    Min = x.min(-2,keepdims=True)[0].min(-1,keepdims=True)[0]
    Max = x.max(-2,keepdims=True)[0].max(-1,keepdims=True)[0]
    return (x-Min)/(Max-Min)
def entropy(x,bit=16): # derive entropy of input
    x = torch.ceil(x*2**bit)
    _,count = torch.unique(x,return_counts=True)
    count   = count/count.sum()
    result  = -(count*torch.log2(count)).sum()
    return result

class DataSet(torch.utils.data.Dataset): # Load data in memory before training to speed up
    def __init__(self, dataset_path = opt.dataset_path, dataset_size = opt.dataset_size, test_dataset_size = opt.testset_size, train=False):
        train_dataset_size, step = 20000 - 200, 20000//200-1
        test_dataset_sampler, train_dataset_sampler = list(range(1,20000,step))[:test_dataset_size], list(range(0, dataset_size))
        for i in test_dataset_sampler:
            if i in train_dataset_sampler:
                train_dataset_sampler.remove(i)
        self.sampler = train_dataset_sampler if train else test_dataset_sampler
        self.dataset, self.dataset_path = h5py.File(f"/home/frank/speckle_data/{dataset_path}",'r'), dataset_path
        self.speckle, self.image = self.dataset['speckle'][self.sampler], self.dataset['image'][self.sampler]
    def __len__(self): return len(self.sampler)
    def __getitem__(self, item):
        speckle, image = torch.tensor(self.speckle[item]), torch.tensor(self.image[item])
        if opt.spk_size >= 200:
            in_dim_start = (256 - opt.spk_size) // 2
            speckle = speckle[in_dim_start:in_dim_start+opt.spk_size,in_dim_start:in_dim_start+opt.spk_size]
        if opt.spk_size in [128,85,64,51,42,36,32,28,25,16,8,4,2] or opt.spk_size in [84,50,24]: # 85 and 51 is difficult to deal with in U-Net
            if opt.block_choose == -1:
                speckle = torch.nn.AvgPool2d(kernel_size=256//opt.spk_size)(speckle.unsqueeze(0)).squeeze()
            else:
                in_dim_start_x  = opt.block_choose // (256//opt.spk_size) * opt.spk_size
                in_dim_start_y  = opt.block_choose * opt.spk_size - opt.block_choose // (256//opt.spk_size) * (256//opt.spk_size) * opt.spk_size
                speckle = speckle[in_dim_start_x:in_dim_start_x+opt.spk_size, in_dim_start_y:in_dim_start_y+opt.spk_size]
        if opt.img_size in [64,42,32,25,21,18,16]: image = torch.nn.AvgPool2d(kernel_size=128//opt.img_size)(image.unsqueeze(0)).squeeze()
        
        return speckle.unsqueeze(0), image.unsqueeze(0)


class Model(pl.LightningModule):
    def __init__(self, in_dim, out_dim):
        super().__init__()
        self.lr, self.in_dim, self.out_dim, self.val_step_outputs, self.training_step_outputs = opt.lr, in_dim, out_dim, [], []
        if opt.model_choose == 1: self.model = torch.nn.Linear(in_dim*in_dim, out_dim*out_dim).to(torch.complex64)
        if opt.model_choose == 3:
            # Ref: Better plain ViT baselines for ImageNet-1k, https://github.com/lucidrains/vit-pytorch
            self.model = vit_pytorch.ViT(image_size = opt.spk_size, patch_size = opt.spk_size, num_classes = opt.img_size ** 2,
                dim = opt.img_size * 32, depth = 4, heads = 8, mlp_dim = 256, channels = 1, dropout = 0.1, emb_dropout = 0.1)
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

    def forward(self,x):
        if opt.model_choose == 1:
            x = x.reshape(-1, self.in_dim*self.in_dim).to(torch.complex64)
            x = self.model(x).abs().reshape(-1, 1, self.out_dim, self.out_dim)
        if opt.model_choose == 3:
            x = self.model(x).reshape(-1, 1, self.out_dim, self.out_dim)
        return x

    def get_loss(self, batch, batch_idx):
        speckle, image = batch
        image_pred = model(speckle)
        loss_mse = torch.nn.functional.mse_loss(image_pred, image)
        loss_pcc = pearson_corrcoef(image_pred.reshape(-1,self.out_dim*self.out_dim).t(), image.reshape(-1,self.out_dim*self.out_dim).t())
        loss_psnr = peak_signal_noise_ratio(image_pred.reshape(-1,self.out_dim*self.out_dim),image.reshape(-1,self.out_dim*self.out_dim),reduction='none',dim=[-1],data_range=1)
        loss_ssim = structural_similarity_index_measure(image_pred,image,reduction='none')
        if self.current_epoch > opt.epochs * 0.8 and opt.dataset_path[:4]!="holo": loss = loss_mse.mean()
        else: loss = loss_mse.mean() - opt.loss_pcc*loss_pcc.mean() - opt.loss_ssim*loss_ssim.mean()
        return loss.cpu(), loss_pcc.cpu(), loss_psnr.cpu(), loss_ssim.cpu(), image_pred.cpu(), speckle.cpu(), image.cpu()

    def training_step(self, batch, batch_idx):
        loss, loss_pcc, _, _, _, _, _ = self.get_loss(batch, batch_idx)
        self.log_dict({"loss/train":loss, "loss/train_pcc":loss_pcc.mean()})
        self.training_step_outputs.append([loss])
        return loss

    def on_train_epoch_end(self):
        loss = torch.tensor([i for i in self.training_step_outputs])
        self.training_step_outputs.clear()
        self.log("loss_mean/train_loss_mean", loss.mean())
        
    def validation_step(self, batch, batch_idx):
        loss, loss_pcc, loss_psnr, loss_ssim, image_pred, speckle, image = self.get_loss(batch, batch_idx)
        self.log_dict({"loss/val":loss, "loss/val_pcc":loss_pcc.mean(), "loss/val_ssim":loss_ssim.mean(), "loss/val_psnr":loss_psnr.mean()})
        self.val_step_outputs.append([loss, loss_pcc, loss_psnr, loss_ssim, image_pred, speckle, image])
    
    def on_validation_epoch_end(self):
        loss_pcc, loss_psnr, loss_ssim = torch.cat([i[1] for i in self.val_step_outputs]), torch.cat([i[2] for i in self.val_step_outputs]), torch.cat([i[3] for i in self.val_step_outputs])
        image_pred, speckle, image = torch.cat([i[-3] for i in self.val_step_outputs]), torch.cat([i[-2] for i in self.val_step_outputs]), torch.cat([i[-1] for i in self.val_step_outputs])
        self.val_step_outputs.clear()
        self.log_dict({"loss_mean/val_pcc":loss_pcc.mean(), "loss_mean/val_ssim":loss_ssim.mean(), "loss_mean/val_psnr":loss_psnr.mean()})
        output_text = f"Retrieved PCC = {loss_pcc.mean().item():.4f}, SSIM = {loss_ssim.mean().item():.4f}, PSNR = {loss_psnr.mean().item():.4f}"
        print(f"Epoch {self.current_epoch+1}/{opt.epochs} {output_text}"), trainer.logger.experiment.add_text("Retrieved_PCC", output_text, self.current_epoch)

    def configure_optimizers(self):
        if opt.optimizer == 0: optimizer = torch.optim.SGD (self.parameters(), lr=self.lr,momentum=0.9,weight_decay=0,nesterov=True)
        if opt.optimizer == 1: optimizer = torch.optim.Adam(self.parameters(), lr=self.lr) # Adam use more GPU memory
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, opt.epochs)
        return [optimizer], [scheduler]

if __name__ == "__main__":
    train_loader = torch.utils.data.DataLoader(DataSet(train=True),  batch_size=opt.batch_size, num_workers=6, shuffle=False)
    val_loader   = torch.utils.data.DataLoader(DataSet(train=False), batch_size=opt.batch_size, num_workers=6, shuffle=False)
    pl.seed_everything(1, workers=True) # Set random seeds before training
    model = Model(in_dim = opt.spk_size, out_dim = opt.img_size)
    tensor_board_path = f"{datetime.datetime.now().strftime('%b%d_%H-%M-%S')}"
    tb_logger = pl.loggers.TensorBoardLogger("runs/", name=f"Delocalization_{tensor_board_path}")
    lr_monitor = pl.callbacks.LearningRateMonitor(logging_interval='epoch',log_momentum=True) # lr-Adam in tensorboard
    trainer = pl.Trainer(max_epochs=opt.epochs, log_every_n_steps=1, accelerator="auto", logger=tb_logger, enable_checkpointing=opt.save_model, callbacks=[lr_monitor], enable_progress_bar=False)
    print(f"tb_logger_folder runs/Delocalization_{tensor_board_path} total parameters = {sum(p.numel() for p in model.parameters() if p.requires_grad)}\n")
    trainer.fit(model, train_loader, val_loader)

