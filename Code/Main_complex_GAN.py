# Extended Neural Network Generalizability for High-fidelity
# Human Face Imaging from Spatiotemporally Decorrelated Speckles
# Data underlying the results presented in this paper are not publicly available 
# at this time but may be obtained from the authors upon reasonable request.
# With PyTorch 2.0.1 with CUDA 12.1 and Python 3.11.4 implemented on RTX 3090

# Complex conv from PyTorch 2.0 is used in generator(UNet)
# Add complex Relu and BatchNorm, add complex_dropout for Dense_block, add data-sampler for diffuser results
# GAN ref: https://github.com/eriklindernoren/PyTorch-GAN/blob/master/implementations/acgan/acgan.py

import argparse, os, h5py, datetime, textwrap
import torch, torchvision, pytorch_msssim
from tqdm import tqdm
from torchmetrics.functional import pearson_corrcoef, structural_similarity_index_measure, peak_signal_noise_ratio

parser = argparse.ArgumentParser()
parser.add_argument("--dataset_path", type=str,   help="Dataset_path") # /home/frank/speckle_data/my_hdf5_file_20210326_9.h5
parser.add_argument("--n_epochs",     type=int,   default=20,    help="Number of epochs of training")
parser.add_argument("--eval_dataset_sampler",type=float,default=11.01,help="Eval_dataset_sampler")
parser.add_argument("--eval_dataset_size",type=int,default=1,    help="Eval_dataset_size = opt.eval_dataset_size*batch_size")
parser.add_argument("--dis_iteration",type=int,   default=5,     help="When train generator once, train discriminator more times. If 0, dis is not trained")
parser.add_argument("--lr",           type=float, default=1e-4,  help="Adam learning rate for generator, default 0.0001")
parser.add_argument("--lr_dis",       type=float, default=1e-4,  help="Learning rate for discriminator,  default 0.0001")

parser.add_argument("--batch_size",   type=int,   default=32,    help="Size of the batches")
parser.add_argument("--b1",           type=float, default=0.5,   help="Adam: decay of 1st order momentum of gradient")
parser.add_argument("--b2",           type=float, default=0.999, help="Adam: decay of 2nd order momentum of gradient")
parser.add_argument("--loss_weight_g",type=float, default=0.8,   help="Weight of img_loss in g_loss (from 0 to 1, default 0.8)")
parser.add_argument("--save_model",   type=int,   default=0,     help="Save model after training, 0:Disable, 1:Enable")

opt = parser.parse_args()
max_epochs, batch_size, dataset_path = opt.n_epochs, opt.batch_size, opt.dataset_path

def normalization(x):
    Min, Max = x.min(-2,keepdims=True)[0].min(-1,keepdims=True)[0], x.max(-2,keepdims=True)[0].max(-1,keepdims=True)[0]
    return (x-Min)/(Max-Min)

# Implemented with 
class DataSet(torch.utils.data.Dataset):
    def __init__(self,dataset_path,dataset_sampler):
        self.speckle, self.image, self.dataset_sampler = h5py.File(dataset_path,'r')['speckle'], h5py.File(dataset_path,'r')['image'], dataset_sampler
    def __getitem__(self, index):
        speckle, image = torch.tensor(self.speckle[self.dataset_sampler[index]]), torch.tensor(self.image[self.dataset_sampler[index]])
        image, a, b = image[::128//64,::128//64], 64, 64
        return speckle[a:a+128,b:b+128].unsqueeze(0), image.unsqueeze(0)
    def __len__(self): return len(self.dataset_sampler)

def dataset_load_split(dataset_path, batch_size = opt.batch_size, num_workers = 6):
    eval_dataset_size     = opt.eval_dataset_size*batch_size
    train_size, interval  = int(opt.eval_dataset_sampler-10)*1000, int(opt.eval_dataset_sampler *100 %100)
    eval_dataset_sampler  = list(range(train_size+interval*500-eval_dataset_size,train_size+interval*500))
    train_dataset_sampler = list(range(0, train_size))
    train_dataset, eval_dataset, dataset = DataSet(dataset_path, train_dataset_sampler), DataSet(dataset_path, eval_dataset_sampler), {}
    dataset['train'] = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, num_workers=num_workers, shuffle=False)
    dataset['eval' ] = torch.utils.data.DataLoader( eval_dataset, batch_size=batch_size, num_workers=num_workers, shuffle=False)
    return dataset

class UNet(torch.nn.Module):
    def __init__(self, UNet_channel_number=64):
        class Real_to_Complex(torch.nn.Module):
            def forward(self, input): return input + 1j * input
        class Complex_to_Real(torch.nn.Module):
            def forward(self, input): return input.abs()
        class Complex_conv2d(torch.nn.Module):
            def __init__(self, in_channels, out_channels, kernel_size=3, stride=1, padding=1, dilation=1, groups=1, bias=True):
                super(Complex_conv2d, self).__init__()
                self.conv = torch.nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding, dilation, groups, bias).to(torch.complex64)
            def forward(self, input): return self.conv(input)
        class Complex_ConvTranspose2d(torch.nn.Module):
            def __init__(self,in_channels, out_channels, kernel_size=4, stride=1, padding=0, output_padding=0, groups=1, bias=True, dilation=1, padding_mode='zeros'):
                super(Complex_ConvTranspose2d, self).__init__()
                self.conv_tran = torch.nn.ConvTranspose2d(in_channels, out_channels, kernel_size, stride, padding, output_padding, groups, bias, dilation, padding_mode).to(torch.complex64)
            def forward(self, input): return self.conv_tran(input)
        class Complex_Sigmoid(torch.nn.Module):
            def __init__(self, inplace=False):
                super(Complex_Sigmoid,self).__init__()
                self.sigmoid = torch.nn.Sigmoid().to(torch.complex64)
            def forward(self, input): return self.sigmoid(input)
        class Complex_ReLU(torch.nn.Module):
            def __init__(self, inplace=False):
                super(Complex_ReLU, self).__init__()
                self.ReLU = torch.nn.ReLU(inplace)
            def forward(self, input): return self.ReLU(input.real) + 1j * self.ReLU(input.imag)
        class Complex_batch_norm2d(torch.nn.Module):
            def __init__(self, num_features, eps=1e-5, momentum=0.1, affine=True):
                super(Complex_batch_norm2d, self).__init__()
                self.bn = torch.nn.BatchNorm2d(num_features, eps, momentum, affine, track_running_stats = False)
            def forward(self, input): return self.bn(input.real) + 1j * self.bn(input.imag)
        class Complex_dropout2d(torch.nn.Module):
            def __init__(self, drop_rate=0.2, inplace=False):
                super(Complex_dropout2d,self).__init__()
                self.dropout = torch.nn.Dropout2d(drop_rate,inplace)
            def forward(self, input): return self.dropout(input.real) + 1j * self.dropout(input.imag)       

        class DenseBlock(torch.nn.Module):
            def __init__(self, in_ch, out_ch, growth_rate=16, num_layer=4):
                super(DenseBlock, self).__init__()
                class DenseLayer(torch.nn.Module): # Conv2d
                    def __init__(self, in_ch, out_ch):
                        super(DenseLayer, self).__init__()
                        self.conv = torch.nn.Sequential(Complex_conv2d(in_ch, out_ch, 3, 1, 1), Complex_batch_norm2d(out_ch), Complex_ReLU(), Complex_dropout2d())
                    def forward(self, input):  return self.conv(input)
                self.DenseLayer1 = DenseLayer(in_ch=in_ch + 0,             out_ch=growth_rate)
                self.DenseLayer2 = DenseLayer(in_ch=in_ch + growth_rate,   out_ch=growth_rate)
                self.DenseLayer3 = DenseLayer(in_ch=in_ch + growth_rate*2, out_ch=growth_rate)
                self.DenseLayer4 = DenseLayer(in_ch=in_ch + growth_rate*3, out_ch=out_ch)
            def forward(self, x):
                d = [x]
                d.append(self.DenseLayer1(x))
                d.append(self.DenseLayer2(torch.cat(d, 1)))
                d.append(self.DenseLayer3(torch.cat(d, 1)))
                return self.DenseLayer4(torch.cat(d, 1))

        class down(torch.nn.Module):
            def __init__(self, in_ch=1, out_ch=1, kernel_size=4, padding=1, stride=2):
                super(down, self).__init__()
                self.same = torch.nn.Sequential(DenseBlock(out_ch=out_ch, in_ch=in_ch))
                self.d = torch.nn.Sequential(Complex_conv2d(out_ch, out_ch, kernel_size, stride, padding), Complex_batch_norm2d(out_ch), Complex_ReLU())
            def forward(self, x):
                x_skip = self.same(x)
                return x_skip, self.d(x_skip)

        class up(torch.nn.Module):
            def __init__(self, in_ch=1, in_m_ch=1, out_ch=1, kernel_size=4, padding=1, stride=2):
                super(up, self).__init__()
                self.u = torch.nn.Sequential(Complex_ConvTranspose2d(in_ch, in_ch, kernel_size, stride, padding), Complex_batch_norm2d(in_ch), Complex_ReLU())
                self.h = torch.nn.Sequential(DenseBlock(out_ch=out_ch, in_ch=in_m_ch))
            def forward(self, x, x_skip): return self.h(torch.cat([self.u(x), x_skip], 1))

        super(UNet, self).__init__()
        self.Real_to_Complex = Real_to_Complex()
        self.s1_down = down(1, UNet_channel_number)
        self.s2_down = down(UNet_channel_number,   UNet_channel_number*2)
        self.s3_down = down(UNet_channel_number*2, UNet_channel_number*4)
        self.s4_down = down(UNet_channel_number*4, UNet_channel_number*8)
        self.s5_down = down(UNet_channel_number*8, UNet_channel_number*16)
        self.s4_up   = up  (UNet_channel_number*16,UNet_channel_number*24,UNet_channel_number*4)
        self.s3_up   = up  (UNet_channel_number*4, UNet_channel_number*8, UNet_channel_number*2)
        self.s2_up   = up  (UNet_channel_number*2, UNet_channel_number*4, UNet_channel_number)
        self.s1_up   = up (UNet_channel_number, UNet_channel_number*2, 32)
        self.output = torch.nn.Sequential(Complex_conv2d(32, 1, kernel_size=3, stride=2, padding=1), Complex_Sigmoid())
        self.Complex_to_Real = Complex_to_Real()
    def forward(self, x_s):
        x_s1_skip, x_s = self.s1_down(self.Real_to_Complex(x_s))
        x_s2_skip, x_s = self.s2_down(x_s)
        x_s3_skip, x_s = self.s3_down(x_s)
        x_s4_skip, x_s = self.s4_down(x_s)
        x_s, _ = self.s5_down(x_s)
        x_s = self.s4_up(x_s, x_s4_skip)
        x_s = self.s3_up(x_s, x_s3_skip)
        x_s = self.s2_up(x_s, x_s2_skip)
        x_s = self.s1_up(x_s, x_s1_skip)
        x_s = self.output(x_s)
        return self.Complex_to_Real(x_s)

class Generator(torch.nn.Module):
    def __init__(self):
        super(Generator, self).__init__()
        self.UNet = UNet()
    def forward(self, speckle):
        return self.UNet(speckle)

class Discriminator(torch.nn.Module):
    def __init__(self, dis_channel_number = 1):
        super(Discriminator, self).__init__()
        def discriminator_block(in_filters, out_filters, bn=True):  #each discriminator block
            block = [torch.nn.Conv2d(in_filters, out_filters, kernel_size=3, stride=2, padding=1),torch.nn.ReLU(inplace=False)]
            if bn: block.append(torch.nn.BatchNorm2d(out_filters, 0.8))
            return block
        self.conv_blocks = torch.nn.Sequential(*discriminator_block(1, dis_channel_number*2, bn=False),
            *discriminator_block(dis_channel_number*2, dis_channel_number*4), 
            *discriminator_block(dis_channel_number*4, dis_channel_number*8), 
            *discriminator_block(dis_channel_number*8, dis_channel_number*8),
            *discriminator_block(dis_channel_number*8, 16)) 
        self.conv_blocks = torch.nn.Sequential(self.conv_blocks,*discriminator_block(16, 16))
        self.val_layer = torch.nn.Sequential(torch.nn.Linear(16, 1), torch.nn.Sigmoid())
    def forward(self, image):
        return self.val_layer(self.conv_blocks(image).reshape(image.shape[0],-1))

class com_loss(torch.nn.Module):
    def PCC(x,y): return pearson_corrcoef(x.reshape(x.shape[0],-1).t(), y.reshape(y.shape[0],-1).t())
    def MSE(x,y): return torch.mean((x-y).square(),[1,2,3])
    def SSIM(x,y): return structural_similarity_index_measure(x,y,reduction='none')
    def PSNR(x,y): return peak_signal_noise_ratio(x.reshape(x.shape[0],-1),y.reshape(y.shape[0],-1),reduction='none',dim=[-1],data_range=1)
    def forward(self, x, y, epoch=0): return com_loss.MSE(x,y) - com_loss.PCC(x,y) # com_loss combine MSE and PCC

# Prepare PyTorch and TensorBoard
torch.cuda.synchronize(), torch.cuda.init(), torch.cuda.empty_cache()
torch.backends.cudnn.enabled, torch.backends.cudnn.deterministic = False, True
torch.manual_seed(20), torch.cuda.manual_seed_all(20)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

dataloader = dataset_load_split(dataset_path) # Prepare datasets
image_loss, adversarial_loss = com_loss(), torch.nn.MSELoss() # com_loss combine MSE and PCC
generator, discriminator = Generator().to(device), Discriminator().to(device)
optimizer_G, optimizer_D = torch.optim.Adam(generator.parameters(), lr=opt.lr, betas=(opt.b1, opt.b2)), torch.optim.Adam(discriminator.parameters(), lr=opt.lr_dis, betas=(opt.b1, opt.b2))
scheduler_G, scheduler_D = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer_G,max_epochs), torch.optim.lr_scheduler.CosineAnnealingLR(optimizer_D,max_epochs)

global speckle, image, Gen_imgs

def generator_train(train=True, epoch=0):
    if train: generator.train(),discriminator.eval(),optimizer_G.zero_grad()
    else:     generator.eval (),discriminator.eval()
    gen_imgs = generator(speckle)
    validity,valid_expected = discriminator(gen_imgs), discriminator(image)
    g_loss_adv = adversarial_loss(validity, valid_expected)
    g_loss_img = image_loss(gen_imgs, image, epoch).mean()
    g_loss = g_loss_adv * (1-opt.loss_weight_g) + g_loss_img * opt.loss_weight_g
    if train: g_loss.backward(), optimizer_G.step()
    Gen_imgs = gen_imgs.detach()
    gen_imgs_mse,  gen_imgs_pcc  = com_loss.MSE (Gen_imgs, image).cpu(), com_loss.PCC (Gen_imgs, image).cpu()
    gen_imgs_ssim, gen_imgs_psnr = com_loss.SSIM(Gen_imgs, image).cpu(), com_loss.PSNR(Gen_imgs, image).cpu()
    return Gen_imgs, g_loss, gen_imgs_mse, gen_imgs_pcc, gen_imgs_ssim, gen_imgs_psnr

def discriminator_train(train=True, iteration=5):
    if train: generator.eval(),discriminator.train()
    else:     generator.eval(),discriminator.eval ()
    if not train: iteration = 1
    for j in range(iteration):
        optimizer_D.zero_grad()
        real_pred, fake_pred, fake_estimated = discriminator(image), discriminator(Gen_imgs), image_loss(Gen_imgs, image).unsqueeze(-1)
        d_loss = adversarial_loss(fake_pred, fake_estimated)
        if train: d_loss.backward(), optimizer_D.step()
    return d_loss, real_pred, fake_pred

def unpack_tensor_results(Tensor_results, epoch=0, prefix='', train=True):
    d_loss, g_loss = torch.cat([i[0].reshape(1,1) for i in Tensor_results]), torch.cat([i[1].reshape(1,1) for i in Tensor_results])
    real_pred, fake_pred = torch.cat([i[2].cpu() for i in Tensor_results]), torch.cat([i[3].cpu() for i in Tensor_results])
    gen_imgs_mse, gen_imgs_pcc = torch.cat([i[4].cpu() for i in Tensor_results]), torch.cat([i[5].cpu() for i in Tensor_results])
    gen_imgs_ssim, gen_imgs_psnr = torch.cat([i[6].cpu() for i in Tensor_results]), torch.cat([i[7].cpu() for i in Tensor_results])
    return d_loss, g_loss, real_pred, fake_pred, gen_imgs_mse, gen_imgs_pcc, gen_imgs_ssim, gen_imgs_psnr

with tqdm(range(max_epochs)) as tepoch:
    for epoch in tepoch:
        tepoch.set_description(f"Epoch {epoch}")
        
        global speckle, image, Gen_imgs
        Tensor_results = []
        for i, (speckle,image) in (enumerate(dataloader['train'])):
            speckle, image = normalization(speckle.to(device)), normalization(image.to(device))
            Gen_imgs, g_loss, gen_imgs_mse, gen_imgs_pcc, gen_imgs_ssim, gen_imgs_psnr = generator_train(train=True,epoch=epoch) 
            d_loss, real_pred, fake_pred = discriminator_train(train=True, iteration=opt.dis_iteration)
            s = f'[Gen_img PCC/SSIM:{gen_imgs_pcc.mean().item():.4f}/{gen_imgs_ssim.mean().item():.4f}] [D loss:{d_loss.item():.4f}]'
            tepoch.set_postfix_str(f"[Batch {i+1}] [G loss:{g_loss.item():.4f}] {s}")
            Tensor_results.append([d_loss, g_loss, real_pred, fake_pred, gen_imgs_mse, gen_imgs_pcc, gen_imgs_ssim, gen_imgs_psnr])
            
        d_loss, g_loss, _, _, _, gen_imgs_pcc, gen_imgs_ssim, _ = unpack_tensor_results(Tensor_results,epoch,train=True)
        s = f'[Gen PCC/SSIM:{gen_imgs_pcc.mean().item():.6f}/{gen_imgs_ssim.mean().item():.6f}] [D loss: {d_loss.mean().item():.6f}]'
        tqdm.write(f'[Train epoch {epoch+1:04d} / {max_epochs:04d}]  [G loss: {g_loss.mean().item():.6f}] {s}')
        scheduler_G.step(), scheduler_D.step()

        Image_results, Tensor_results = [], []
        with torch.no_grad():
            for i, (speckle,image) in (enumerate(dataloader['eval'])):
                speckle, image = normalization(speckle.to(device)), normalization(image.to(device))
                Gen_imgs, g_loss, gen_imgs_mse, gen_imgs_pcc, gen_imgs_ssim, gen_imgs_psnr = generator_train(train=False)
                d_loss, real_pred, fake_pred = discriminator_train(train=False, iteration=1)
                Image_results.append([Gen_imgs.cpu(), speckle.cpu(), image.cpu()])
                Tensor_results.append([d_loss, g_loss, real_pred, fake_pred, gen_imgs_mse, gen_imgs_pcc, gen_imgs_ssim, gen_imgs_psnr])
        
        d_loss, g_loss, _, _, _, gen_imgs_pcc, gen_imgs_ssim, gen_imgs_psnr = unpack_tensor_results(Tensor_results,epoch,train=False) 
        Gen_imgs, speckle, image = torch.cat([i[0] for i in Image_results]), torch.cat([i[1] for i in Image_results]), torch.cat([i[2] for i in Image_results])
        s = f'[Gen PCC/SSIM/PSNR:{gen_imgs_pcc.mean().item():.6f}/{gen_imgs_ssim.mean().item():.6f}/{gen_imgs_psnr.mean().item():.6f}]'
        tqdm.write(f'[Test  epoch {epoch+1:04d} / {max_epochs:04d}] [G loss: {g_loss.mean().item():.4f}] [D loss: {d_loss.mean().item():.6f}] {s}')
        

