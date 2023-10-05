# Main file for "Extended Neural Network Generalizability for High-fidelity Human Face Imaging from Spatiotemporally Decorrelated Speckles"

# Complex conv from PyTorch 2.0 is used in generator(UNet)
# Add complex Relu and BatchNorm, add complex_dropout for Dense_block, add data-sampler for diffuser results
# GAN ref: https://github.com/eriklindernoren/PyTorch-GAN/blob/master/implementations/acgan/acgan.py
# python Main_complex_GAN.py --n_epochs 20 --eval_dataset_sampler 25.01 # sample
import argparse, os, h5py, datetime, textwrap
import torch, torchvision, pytorch_msssim
from torch.utils.tensorboard import SummaryWriter 
from tqdm import tqdm
from torchmetrics.functional import pearson_corrcoef, structural_similarity_index_measure, peak_signal_noise_ratio
from torchmetrics.image.lpip import LearnedPerceptualImagePatchSimilarity

# Load parameters form command
parser = argparse.ArgumentParser()
parser.add_argument("--dataset_path", type=str,   default='my_hdf5_file_20210326_9.h5', help="Dataset_path")
parser.add_argument("--n_epochs",     type=int,   default=20,    help="Number of epochs of training")
parser.add_argument("--GAN_type",     type=int,   default=1,     help="Choose 0:real_GAN or 1:complex_GAN or 2:complex_UNet or real_UNet")
parser.add_argument("--eval_dataset_sampler",type=float,default=11.01,help="Eval_dataset_sampler start at 1 (default), otherwise batch_size-1")
parser.add_argument("--eval_dataset_size",type=int,default=1,    help="Eval_dataset_size = opt.eval_dataset_size*batch_size")
parser.add_argument("--convert",      type=int,   default=1,     help="0:input.to(torch.complex64) 1:input+input*1j")
parser.add_argument("--dis_iteration",type=int,   default=5,     help="When train generator once, train discriminator more times. If 0, dis is not trained")
parser.add_argument("--lr",           type=float, default=1e-4,  help="Adam learning rate for generator, default 0.0001")
parser.add_argument("--lr_dis",       type=float, default=1e-4,  help="Learning rate for discriminator,  default 0.0001")

parser.add_argument("--dataset_size", type=int,   default=-1,    help="Size of the dataset, -1:useless, others:dataset_size")
parser.add_argument("--batch_size",   type=int,   default=32,    help="Size of the batches")
parser.add_argument("--b1",           type=float, default=0.5,   help="Adam: decay of 1st order momentum of gradient")
parser.add_argument("--b2",           type=float, default=0.999, help="Adam: decay of 2nd order momentum of gradient")
parser.add_argument("--img_size",     type=int,   default=64,    help="Resolution of output image 128x128, 64x64, or 32x32")
parser.add_argument("--loss_weight_g",type=float, default=0.8,   help="Weight of UNet img_loss in g_loss (from 0 to 1, default 0.8)")
parser.add_argument("--optimizer",    type=int,   default=0,     help="PyTorch Optimizer (Adam is better), 0:Adam, 1:SGD")
parser.add_argument("--offset_x",     type=int,   default=64,    help="Offset_x for cropping FOV")
parser.add_argument("--offset_y",     type=int,   default=64,    help="Offset_y for cropping FOV")
parser.add_argument("--save_graph"  , type=int,   default=0,     help="Save model graph in tensorboard 0:none 1:generator 2:discriminator")
parser.add_argument("--save_model",   type=int,   default=0,     help="Save model after training, 0:Disable, 1:Enable")
parser.add_argument("--drop_rate",    type=float, default=0.2,   help="DenseBlock dropout rate, default=0.2")
parser.add_argument("--UNet_channel_number",type=int,default=64, help="UNet_channel_number in Generator(UNet)")
parser.add_argument("--loss_function",type=int,   default=0,     help="Choose different loss_function")
parser.add_argument("--output_norm",  type=int,   default=0,     help="Add normalization[0,1] to output")
parser.add_argument("--speckle_size", type=int,   default=128,   help="Resolution of input speckle 256x256 or 128x128")
parser.add_argument("--epoch_change_loss", type=int, default=3,  help="Final several epochs will change loss to use LPIPS")
parser.add_argument("--lpips_net_type", type=str, default='vgg', help="Learned Perceptual Image Patch Similarity net_type:vgg,alex,squeeze")
parser.add_argument("--update_on_final_epoch", type=int,default=1,help="1:update parameters on final epoch, 0:not")

opt = parser.parse_args() # opt = parser.parse_args(args=["--GAN_type","1"])
if opt.dataset_path[-15:-3]=="normal_light": opt.offset_x, opt.offset_y = 32,32
max_epochs, batch_size = opt.n_epochs, opt.batch_size
dataset_path = f"/home/frank/speckle_data/{opt.dataset_path}"
opt_str = f"\nDataset-{opt.dataset_path}  LR-{opt.lr}  LR_dis-{opt.lr_dis}  Epoch-{opt.n_epochs}"
if opt. GAN_type  == 0: 
    if opt.dis_iteration != 0: opt_str = f"{opt_str} GAN-real_conv \n"
    if opt.dis_iteration == 0: opt_str = f"{opt_str} UNet-real_conv \n"
if opt. GAN_type  == 1: 
    if opt.dis_iteration != 0: opt_str = f"{opt_str} GAN-comp_conv \n"
    if opt.dis_iteration == 0: opt_str = f"{opt_str} UNet-comp_conv \n"
if opt.dis_iteration != 0: opt_str = f"{opt_str}g_loss = g_loss_adv * {1-opt.loss_weight_g:.1f} + g_loss_img * {opt.loss_weight_g:.1f}"
print(opt_str),print(textwrap.fill(f"{opt}", width=100))

def normalization(x):
    Min, Max = x.min(-2,keepdims=True)[0].min(-1,keepdims=True)[0], x.max(-2,keepdims=True)[0].max(-1,keepdims=True)[0]
    return (x-Min)/(Max-Min)

class DataSet2(torch.utils.data.Dataset): # Load data when training, only used for chunked dataset
    def __init__(self,dataset_path,dataset_sampler):
        self.speckle, self.image, self.dataset_sampler = h5py.File(dataset_path,'r')['speckle'], h5py.File(dataset_path,'r')['image'], dataset_sampler
    def __getitem__(self, index):
        speckle, image = torch.tensor(self.speckle [self.dataset_sampler[index]]), torch.tensor(self.image[self.dataset_sampler[index]])
        image = image[::128//64,::128//64] 
        a,b = opt.offset_x,opt.offset_y
        if opt.speckle_size == 128: return speckle[a:a+128,b:b+128].unsqueeze(0), image.unsqueeze(0)
        if opt.speckle_size == 256: return speckle[0:256,0:256].unsqueeze(0), image.unsqueeze(0)
    def __len__(self): return len(self.dataset_sampler)

def dataset_load_split2(dataset_path, batch_size = opt.batch_size, num_workers = 6):# Split dataset into train, and test
    eval_dataset_size = opt.eval_dataset_size*batch_size
    if opt.eval_dataset_sampler >= 10  and opt.eval_dataset_sampler < 100: # Train_set and test_set have time intervals
        train_size, interval = int(opt.eval_dataset_sampler-10)*1000, int(opt.eval_dataset_sampler *100 %100)
        eval_dataset_sampler = list(range(train_size+interval*500-eval_dataset_size,train_size+interval*500))
        if opt.dataset_size == -1: train_dataset_sampler = list(range(0, train_size))
        else: train_dataset_sampler = list(range(0, train_size, train_size//opt.dataset_size))
    if opt.eval_dataset_sampler >= 100 and opt.dataset_path[-7:-3]=='meta': # For meta surface results
        train_size, interval = int(opt.eval_dataset_sampler-100), int(opt.eval_dataset_sampler*100%100)
        # eval_dataset_size = eval_dataset_size*4 # why need to *4 -> may leads to better PCC results
        if train_size == 4:      train_dataset_sampler = list(range(0, 60000, 60000 // opt.dataset_size))
        if interval   == 0:       eval_dataset_sampler = list(range(60000, 60000+eval_dataset_size))
        if interval   in [1,2,3]: eval_dataset_sampler = list(range(60000+interval*20000-eval_dataset_size, 60000+interval*20000))
    print(f"train_dataset_sampler min-{min(train_dataset_sampler)} max-{max(train_dataset_sampler)} step-{train_dataset_sampler[1]-train_dataset_sampler[0]} amount-{len(train_dataset_sampler)}")
    print(f"eval_dataset_sampler min-{min(eval_dataset_sampler)} max-{max(eval_dataset_sampler)} step-{eval_dataset_sampler[1]-eval_dataset_sampler[0]} amount-{len(eval_dataset_sampler)}")
    train_dataset, eval_dataset, dataset = DataSet2(dataset_path, train_dataset_sampler), DataSet2(dataset_path, eval_dataset_sampler), {}
    dataset['train'] = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, num_workers=num_workers, shuffle=False)
    dataset['eval' ] = torch.utils.data.DataLoader( eval_dataset, batch_size=batch_size, num_workers=num_workers, shuffle=False)
    return dataset

class UNet(torch.nn.Module):
    def __init__(self, UNet_channel_number=opt.UNet_channel_number):
        class Real_to_Complex(torch.nn.Module): # Transform Real number to Complex number
            def forward(self, input):
                if opt.GAN_type == 1: 
                    if opt.convert == 0: return input.to(torch.complex64)
                    if opt.convert == 1: return input + 1j * input
                if opt.GAN_type == 0: return input
        class Complex_to_Real(torch.nn.Module): # Transform Complex number to Real number
            def forward(self, input):
                if opt.GAN_type == 1: return input.abs()
                if opt.GAN_type == 0: return input
        class Complex_conv2d(torch.nn.Module): # Complex Conv2d, perform Conv2d on complex input
            def __init__(self, in_channels, out_channels, kernel_size=3, stride=1, padding=1, dilation=1, groups=1, bias=True):
                super(Complex_conv2d, self).__init__()
                self.conv = torch.nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding, dilation, groups, bias)
                if opt.GAN_type == 1: self.conv = self.conv.to(torch.complex64)
            def forward(self, input): return self.conv(input)
        class Complex_ConvTranspose2d(torch.nn.Module):
            def __init__(self,in_channels, out_channels, kernel_size=4, stride=1, padding=0, output_padding=0, groups=1, bias=True, dilation=1, padding_mode='zeros'):
                super(Complex_ConvTranspose2d, self).__init__()
                self.conv_tran = torch.nn.ConvTranspose2d(in_channels, out_channels, kernel_size, stride, padding, output_padding, groups, bias, dilation, padding_mode)
                if opt.GAN_type == 1: self.conv_tran = self.conv_tran.to(torch.complex64)
            def forward(self, input): return self.conv_tran(input)
        class Complex_Sigmoid(torch.nn.Module):
            def __init__(self, inplace=False):
                super(Complex_Sigmoid,self).__init__()
                self.sigmoid = torch.nn.Sigmoid()
                if opt.GAN_type == 1: self.sigmoid = self.sigmoid.to(torch.complex64)
            def forward(self, input): return self.sigmoid(input)
        class Complex_ReLU(torch.nn.Module): # Complex ReLU, perform ReLU independently on real and imaginary part.
            def __init__(self, inplace=False):
                super(Complex_ReLU, self).__init__()
                self.ReLU = torch.nn.ReLU(inplace) # self.ReLU = torch.nn.LeakyReLU(0,inplace)
            def forward(self, input):
                if opt.GAN_type == 1: return self.ReLU(input.real) + 1j * self.ReLU(input.imag)
                if opt.GAN_type == 0: return self.ReLU(input)
        class Complex_batch_norm2d(torch.nn.Module): # Complex BatchNorm, perform BatchNorm independently on real and imaginary part.
            def __init__(self, num_features, eps=1e-5, momentum=0.1, affine=True):
                super(Complex_batch_norm2d, self).__init__()
                self.bn = torch.nn.BatchNorm2d(num_features, eps, momentum, affine, track_running_stats = False)
            def forward(self, input): 
                if opt.GAN_type == 1: return self.bn(input.real) + 1j * self.bn(input.imag)
                if opt.GAN_type == 0: return self.bn(input)
        class Complex_dropout2d(torch.nn.Module): # Complex Dropout, perform Dropout independently on real and imaginary part.
            def __init__(self, drop_rate, inplace=False):
                super(Complex_dropout2d,self).__init__()
                self.dropout = torch.nn.Dropout2d(drop_rate,inplace)
            def forward(self, input):
                if opt.GAN_type == 1: return self.dropout(input.real) + 1j * self.dropout(input.imag)
                if opt.GAN_type == 0: return self.dropout(input)        

        class DenseBlock(torch.nn.Module): # DenseLayer1 -> DenseLayer2 -> DenseLayer3 -> DenseLayer4
            def __init__(self, in_ch, out_ch, growth_rate=16, num_layer=4):
                super(DenseBlock, self).__init__()
                class DenseLayer(torch.nn.Module): # Conv2d
                    def __init__(self, in_ch, out_ch):
                        super(DenseLayer, self).__init__()
                        self.conv = torch.nn.Sequential(Complex_conv2d(in_ch, out_ch, 3, 1, 1), 
                        Complex_batch_norm2d(out_ch), Complex_ReLU(), Complex_dropout2d(opt.drop_rate))
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
                                
        class down(torch.nn.Module): # DenseBlock -> Conv2d
            def __init__(self, in_ch=1, out_ch=1, kernel_size=4, padding=1, stride=2):
                super(down, self).__init__()
                self.same = torch.nn.Sequential(DenseBlock(out_ch=out_ch, in_ch=in_ch))
                self.d = torch.nn.Sequential(Complex_conv2d(out_ch, out_ch, kernel_size, stride, padding), 
                    Complex_batch_norm2d(out_ch), Complex_ReLU())
            def forward(self, x):
                x_skip = self.same(x)
                return x_skip, self.d(x_skip)

        class up(torch.nn.Module): # ConvTranspose2d -> DenseBlock
            def __init__(self, in_ch=1, in_m_ch=1, out_ch=1, kernel_size=4, padding=1, stride=2):
                super(up, self).__init__()
                self.u = torch.nn.Sequential(Complex_ConvTranspose2d(in_ch, in_ch, kernel_size, stride, padding), 
                    Complex_batch_norm2d(in_ch), Complex_ReLU())
                self.h = torch.nn.Sequential(DenseBlock(out_ch=out_ch, in_ch=in_m_ch))
            def forward(self, x, x_skip): return self.h(torch.cat([self.u(x), x_skip], 1))

        class up_void(torch.nn.Module): 
            def __init__(self): super().__init__()
            def forward(self, x, x_skip): return x

        class up_void2(torch.nn.Module):
            def __init__(self, in_ch=1, in_m_ch=1, out_ch=1, kernel_size=4, padding=1, stride=2):
                super().__init__()
                self.u = torch.nn.Sequential(Complex_ConvTranspose2d(in_ch, in_ch, kernel_size, stride, padding), 
                    Complex_batch_norm2d(in_ch), Complex_ReLU())
                self.d = torch.nn.Sequential(Complex_conv2d(in_m_ch, out_ch, kernel_size, stride, padding), 
                    Complex_batch_norm2d(out_ch), Complex_ReLU())
            def forward(self, x, x_skip): return self.d(torch.cat([self.u(x), x_skip], 1))
                

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
        # if opt.speckle_size == 128: self.s1_up = up (UNet_channel_number, UNet_channel_number*2, 32)
        # if opt.speckle_size == 256: self.s1_up = up_void2(UNet_channel_number, UNet_channel_number*2, 32)
        # self.output = torch.nn.Sequential(Complex_conv2d(32, 1, kernel_size=3, stride=2, padding=1), Complex_Sigmoid())
        self.s1_up   = up (UNet_channel_number, UNet_channel_number*2, 32)
        if opt.speckle_size == 128: self.output = torch.nn.Sequential(Complex_conv2d(32, 1, kernel_size=3, stride=2, padding=1), Complex_Sigmoid())
        if opt.speckle_size == 256: self.output = torch.nn.Sequential(Complex_conv2d(32, 1, kernel_size=3, stride=4, padding=1), Complex_Sigmoid())
        self.Complex_to_Real = Complex_to_Real()
    def forward(self, x_s): #Input 128x128 or 256x256, Output 64x64
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
        self.UNet = UNet(opt.UNet_channel_number)
    def forward(self, speckle): #Input is 128*128 speckle, output is retrieved image
        if opt.output_norm == 1: return normalization(self.UNet(speckle))
        if opt.output_norm == 0: return self.UNet(speckle)

class Discriminator(torch.nn.Module):
    def __init__(self, dis_channel_number = 1):
        super(Discriminator, self).__init__()
        def discriminator_block(in_filters, out_filters, bn=True):  #each discriminator block
            block = [torch.nn.Conv2d(in_filters, out_filters, kernel_size=3, stride=2, padding=1),torch.nn.ReLU(inplace=False)]
            if bn: block.append(torch.nn.BatchNorm2d(out_filters, 0.8))
            return block
        self.conv_blocks = torch.nn.Sequential(*discriminator_block(1, dis_channel_number*2, bn=False), # Every layer will reduce resolution to 1/2
            *discriminator_block(dis_channel_number*2, dis_channel_number*4), 
            *discriminator_block(dis_channel_number*4, dis_channel_number*8), 
            *discriminator_block(dis_channel_number*8, dis_channel_number*8), # Discriminator doesn't need more filters
            *discriminator_block(dis_channel_number*8, 16)) # For opt.img_size == 32
        if opt.img_size == 64: 
            self.conv_blocks = torch.nn.Sequential(self.conv_blocks,*discriminator_block(16, 16)) # One more layer for opt.img_size == 64
        self.val_layer = torch.nn.Sequential(torch.nn.Linear(16, 1), torch.nn.Sigmoid()) # Output layers
    def forward(self, image): #Input is image (32x32, 64x64, 128x128), output is validity
        return self.val_layer(self.conv_blocks(image).reshape(image.shape[0],-1))

class com_loss(torch.nn.Module):
    def PCC(x,y): return pearson_corrcoef(x.reshape(x.shape[0],-1).t(), y.reshape(y.shape[0],-1).t())
    def MSE(x,y): return torch.mean((x-y).square(),[1,2,3])
    def MAE(x,y): return torch.mean((x-y).abs(),[1,2,3])
    def SSIM(x,y): return structural_similarity_index_measure(x,y,reduction='none')
    def PSNR(x,y): return peak_signal_noise_ratio(x.reshape(x.shape[0],-1),y.reshape(y.shape[0],-1),reduction='none',dim=[-1],data_range=1)
    def LPIPS(x,y): 
        lpips = LearnedPerceptualImagePatchSimilarity(net_type=opt.lpips_net_type,reduction='mean',normalize=True) # net_type:vgg,alex,squeeze
        results, lpips = torch.zeros(x.shape[0]).to(x.device), lpips.to(x.device) # Normalize by default False meaning input is [-1,1], otherwise [0,1]
        for i in range(x.shape[0]):
            a, b = normalization(x[i].unsqueeze(0).expand(-1,3,-1,-1)), normalization(y[i].unsqueeze(0).expand(-1,3,-1,-1))
            results[i]=lpips(a,b)
        return results
    def forward(self, x, y, epoch=0):
        if opt.loss_function == 0: return com_loss.MSE(x,y) - com_loss.PCC(x,y) # com_loss combine MSE and PCC
        if opt.loss_function == 1: return com_loss.MSE(x,y) - com_loss.SSIM(x,y) 


# Prepare PyTorch and TensorBoard
torch.cuda.synchronize(), torch.cuda.init(), torch.cuda.empty_cache()
torch.backends.cudnn.enabled = False # getCudnnDataTypeFromScalarType() not supported for ComplexFloat
torch.backends.cudnn.deterministic = True # Fix random seeds of cudnn to get reproducible results
torch.manual_seed(20), torch.cuda.manual_seed_all(20)
writer = SummaryWriter(comment='GAN') # TensorBoard writer
writer.add_text('Parameters',f'Option( {opt_str} )      Command( {opt} )')
tensor_board_path = f"{datetime.datetime.now().strftime('%b%d_%H-%M-%S')}"
print(f"TensorBoard path: {os.getcwd()}/runs/{tensor_board_path}_MateStationGAN") # TensorBoard_writer path_name
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
dataloader = dataset_load_split2(dataset_path)
image_loss, adversarial_loss = com_loss(), torch.nn.MSELoss() # com_loss combine MSE and PCC
generator, discriminator = Generator().to(device), Discriminator().to(device) # Initialize GAN
if opt.optimizer == 0: optimizer_G, optimizer_D = torch.optim.Adam(generator.parameters(), lr=opt.lr, betas=(opt.b1, opt.b2)), torch.optim.Adam(discriminator.parameters(), lr=opt.lr_dis, betas=(opt.b1, opt.b2))
scheduler_G, scheduler_D = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer_G,max_epochs), torch.optim.lr_scheduler.CosineAnnealingLR(optimizer_D,max_epochs)
with open(os.path.basename(__file__),'r') as f:  writer.add_text('Scipt', f"<pre>{f.read()}</pre>") # Save py file without Markdown format

global speckle, image, Gen_imgs

def generator_train(train=True, epoch=0):
    if train: generator.train(),discriminator.eval(), optimizer_G.zero_grad()
    else    : generator.eval (),discriminator.eval()
    gen_imgs = generator(speckle) # Generate images from speckles
    if opt.dis_iteration != 0:
        validity,valid_expected = discriminator(gen_imgs), discriminator(image) # Loss measures generator's ability to fool discriminator
        g_loss_adv = adversarial_loss(validity, valid_expected)
        g_loss_img = image_loss(gen_imgs, image, epoch).mean() # image_loss is Com_loss
        g_loss = g_loss_adv * (1-opt.loss_weight_g) + g_loss_img * opt.loss_weight_g # weight of UNet img_loss in g_loss (from 0 to 1, default 0.8)
    if opt.dis_iteration == 0: 
        g_loss = image_loss(gen_imgs, image, epoch).mean() # Only generator is used when opt.dis_iteration == 0
    if train:
        g_loss.backward(), optimizer_G.step()
    Gen_imgs = gen_imgs.detach()
    gen_imgs_mse,  gen_imgs_pcc  = com_loss.MSE (Gen_imgs, image).cpu(), com_loss.PCC (Gen_imgs, image).cpu()
    gen_imgs_ssim, gen_imgs_psnr = com_loss.SSIM(Gen_imgs, image).cpu(), com_loss.PSNR(Gen_imgs, image).cpu()
    if train: gen_imgs_lpips = torch.zeros(Gen_imgs.shape[0]) # LearnedPerceptualImagePatchSimilarity is time-consuming
    else: gen_imgs_lpips = com_loss.LPIPS(Gen_imgs, image).to('cpu') # opt.loss_function>=8 using LPIPS loss
    return Gen_imgs, g_loss, gen_imgs_mse, gen_imgs_pcc, gen_imgs_ssim, gen_imgs_psnr, gen_imgs_lpips

def discriminator_train(train=True, iteration=5):
    if opt.dis_iteration == 0:
        if train: optimizer_D.step()
        return torch.zeros(1),torch.zeros(image.shape[0],1),torch.zeros(image.shape[0],1)
    if train: generator.eval(),discriminator.train()
    else:     generator.eval(),discriminator.eval ()
    if not train: iteration = 1
    for j in range(iteration): # Train discriminator more times
        optimizer_D.zero_grad() #  Train Discriminator
        real_pred, fake_pred, fake_estimated = discriminator(image), discriminator(Gen_imgs), image_loss(Gen_imgs, image).unsqueeze(-1)
        d_loss = adversarial_loss(fake_pred, fake_estimated) # Loss for fake images
        if train: d_loss.backward(), optimizer_D.step() # Final batch is just for test, not train
    return d_loss, real_pred, fake_pred

def save_image_speckle(epoch,prefix=''):
    writer.add_images(f'{prefix}Gen_imgs', Gen_imgs, epoch, dataformats = 'NCHW')
    if epoch == 0: # Only save speckle & image in epoch 0
        writer.add_images(f'{prefix}Speckles' , speckle , epoch, dataformats = 'NCHW')
        writer.add_images(f'{prefix}Real_imgs', image   , epoch, dataformats = 'NCHW')

def unpack_tensor_results(Tensor_results, epoch=0, prefix='', train=True):
    d_loss, g_loss = torch.cat([i[0].reshape(1,1) for i in Tensor_results]), torch.cat([i[1].reshape(1,1) for i in Tensor_results])
    real_pred, fake_pred = torch.cat([i[2].cpu() for i in Tensor_results]), torch.cat([i[3].cpu() for i in Tensor_results])
    gen_imgs_mse, gen_imgs_pcc = torch.cat([i[4].cpu() for i in Tensor_results]), torch.cat([i[5].cpu() for i in Tensor_results])
    gen_imgs_ssim, gen_imgs_psnr = torch.cat([i[6].cpu() for i in Tensor_results]), torch.cat([i[7].cpu() for i in Tensor_results])
    gen_imgs_lpips = torch.cat([i[-1].cpu() for i in Tensor_results])
    if train:
        writer.add_scalar(f'{prefix}Train_D_loss', d_loss.mean().item(), epoch)
        writer.add_scalar('Train_G_loss', g_loss.mean().item(), epoch)
        writer.add_scalar(f'{prefix}Train_Gen_imgs PCC_mean', gen_imgs_pcc.mean().item(), epoch)
        writer.add_text  (f'{prefix}Train Generated images PCC', f'{gen_imgs_pcc[::200]}', epoch)
    else:
        writer.add_scalar(f'{prefix}Learning_rate_Generator', optimizer_G.param_groups[0]['lr'], epoch)
        writer.add_scalar(f'{prefix}Learning_rate_Discriminator', optimizer_D.param_groups[0]['lr'], epoch)
        writer.add_scalar(f'{prefix}D_loss', d_loss.mean().item(), epoch)
        writer.add_scalar(f'{prefix}G_loss', g_loss.mean().item(), epoch)
        writer.add_scalar(f'{prefix}Gen_imgs MSE_mean',  gen_imgs_mse  .mean().item(), epoch)
        writer.add_scalar(f'{prefix}Gen_imgs PCC_mean',  gen_imgs_pcc  .mean().item(), epoch)
        writer.add_scalar(f'{prefix}Gen_imgs SSIM_mean', gen_imgs_ssim .mean().item(), epoch)
        writer.add_scalar(f'{prefix}Gen_imgs PSNR_mean', gen_imgs_psnr .mean().item(), epoch)
        writer.add_scalar(f'{prefix}Gen_imgs LPIPS_mean',gen_imgs_lpips.mean().item(), epoch)
        writer.add_text  (f'{prefix}Discriminator real_pred & fake_pred', 
            f'real_pred:{real_pred}  \nfake_pred:{fake_pred}', epoch)
        writer.add_text  (f'{prefix}Generated images MSE-PCC-SSIM-PSNR-LPIPS',
            f'MSE:{gen_imgs_mse}  \nPCC:{gen_imgs_pcc}  \nSSIM:{gen_imgs_ssim}  \nPSNR:{gen_imgs_psnr}  \nLPIPS:{gen_imgs_lpips}', epoch)
    return d_loss, g_loss, real_pred, fake_pred, gen_imgs_mse, gen_imgs_pcc, gen_imgs_ssim, gen_imgs_psnr, gen_imgs_lpips

with tqdm(range(max_epochs)) as tepoch:
    for epoch in tepoch:
        tepoch.set_description(f"Epoch {epoch}")
        
        global speckle, image, Gen_imgs
        Tensor_results = []
        for i, (speckle,image) in (enumerate(dataloader['train'])): # Train
            speckle, image = normalization(speckle.to(device)), normalization(image.to(device))
            Gen_imgs, g_loss, gen_imgs_mse, gen_imgs_pcc, gen_imgs_ssim, gen_imgs_psnr, gen_imgs_lpips = generator_train(train=True,epoch=epoch) 
            d_loss, real_pred, fake_pred = discriminator_train(train=True,  iteration=opt.dis_iteration)
            s = f'[Gen_img PCC/SSIM:{gen_imgs_pcc.mean().item():.4f}/{gen_imgs_ssim.mean().item():.4f}] [D loss:{d_loss.item():.4f}]'
            tepoch.set_postfix_str(f"[Batch {i+1}] [G loss:{g_loss.item():.4f}] {s}")
            Tensor_results.append([d_loss, g_loss, real_pred, fake_pred, gen_imgs_mse, gen_imgs_pcc, gen_imgs_ssim, gen_imgs_psnr, gen_imgs_lpips])
        d_loss, g_loss, _, _, _, gen_imgs_pcc, gen_imgs_ssim, _, _ = unpack_tensor_results(Tensor_results,epoch,train=True)
        s = f'[Gen PCC/SSIM:{gen_imgs_pcc.mean().item():.6f}/{gen_imgs_ssim.mean().item():.6f}] [D loss: {d_loss.mean().item():.6f}]'
        tqdm.write(f'[Train epoch {epoch+1:04d} / {max_epochs:04d}]  [G loss: {g_loss.mean().item():.6f}] {s}')
        save_image_speckle(epoch=epoch, prefix=f'Train_')
        scheduler_G.step(), scheduler_D.step()

        Image_results, Tensor_results = [], []
        with torch.no_grad():
            for i, (speckle,image) in (enumerate(dataloader['eval'])): # Eval
                speckle, image = normalization(speckle.to(device)), normalization(image.to(device))
                Gen_imgs, g_loss, gen_imgs_mse, gen_imgs_pcc, gen_imgs_ssim, gen_imgs_psnr, gen_imgs_lpips = generator_train(train=False)
                d_loss, real_pred, fake_pred = discriminator_train(train=False, iteration=1)
                Image_results.append([Gen_imgs.cpu(), speckle.cpu(), image.cpu()])
                Tensor_results.append([d_loss, g_loss, real_pred, fake_pred, gen_imgs_mse, gen_imgs_pcc, gen_imgs_ssim, gen_imgs_psnr, gen_imgs_lpips])
        d_loss, g_loss, _, _, _, gen_imgs_pcc, gen_imgs_ssim, gen_imgs_psnr, gen_imgs_lpips = unpack_tensor_results(Tensor_results,epoch,train=False) 
        Gen_imgs, speckle, image = torch.cat([i[0] for i in Image_results]), torch.cat([i[1] for i in Image_results]), torch.cat([i[2] for i in Image_results])
        s = f'[Gen PCC/SSIM/PSNR/LPIPS:{gen_imgs_pcc.mean().item():.6f}/{gen_imgs_ssim.mean().item():.6f}/{gen_imgs_psnr.mean().item():.6f}/{gen_imgs_lpips.mean().item():.6f}]'
        tqdm.write(f'[Test  epoch {epoch+1:04d} / {max_epochs:04d}] [G loss: {g_loss.mean().item():.4f}] [D loss: {d_loss.mean().item():.6f}] {s}')
        save_image_speckle(epoch=epoch)
        
    if opt.save_model: torch.save({'generator':generator.state_dict(),'discriminator':discriminator.state_dict()}, f"runs/{tensor_board_path}_GAN.pt")
    if opt.eval_dataset_sampler >= 10:
        if opt.eval_dataset_sampler < 100:
            train_set = int(opt.eval_dataset_sampler-10)
            if train_set ==  1: interval = [1,5,10,15,20,25,30,35]
            if train_set ==  5: interval = [1,5,10,15,20,25,30]
            if train_set == 10: interval = [1,5,10,15,20]
            if train_set == 15: interval = [1,5,10]
        if opt.eval_dataset_sampler >= 100 and opt.dataset_path[-7:-3]=='meta': interval = [0,1,2,3] # For meta surface results

        for j in interval:
            if opt.eval_dataset_sampler < 100: eval_dataset_sampler = list(range(train_set*1000+j*500-opt.eval_dataset_size*opt.batch_size, train_set*1000+j*500))    
            if opt.eval_dataset_sampler >= 100 and opt.dataset_path[-7:-3] == 'meta': # eval_dataset_size = opt.eval_dataset_size*4 # why need to *4 ???
                if j == 0: eval_dataset_sampler = list(range(60000, 60000+opt.eval_dataset_size*opt.batch_size))
                if j in [1,2,3]: eval_dataset_sampler = list(range(60000+j*20000-opt.eval_dataset_size*opt.batch_size, 60000+j*20000))
            Image_results, Tensor_results, s = [], [], f"Interval = {j:02d} min "
            with torch.no_grad():
                for (speckle,image) in (torch.utils.data.DataLoader(DataSet2(dataset_path, eval_dataset_sampler), batch_size=opt.batch_size, num_workers=6, shuffle=False)):
                    speckle, image = normalization(speckle.to(device)), normalization(image.to(device))
                    Gen_imgs, g_loss, gen_imgs_mse, gen_imgs_pcc, gen_imgs_ssim, gen_imgs_psnr, gen_imgs_lpips = generator_train(train=False)
                    d_loss, real_pred, fake_pred = discriminator_train(train=False, iteration=1)                    
                    Image_results.append([Gen_imgs.cpu(), speckle.cpu(), image.cpu()])
                    Tensor_results.append([d_loss, g_loss, real_pred, fake_pred, gen_imgs_mse, gen_imgs_pcc, gen_imgs_ssim, gen_imgs_psnr, gen_imgs_lpips])
                Gen_imgs, speckle, image = torch.cat([i[0] for i in Image_results]), torch.cat([i[1] for i in Image_results]), torch.cat([i[2] for i in Image_results])
                _, _, _, _, _, gen_imgs_pcc, gen_imgs_ssim, gen_imgs_psnr, gen_imgs_lpips = unpack_tensor_results(Tensor_results, epoch=0, prefix=s, train=False) 
                save_image_speckle(epoch=0, prefix=s)
                print(f'{s}[Gen PCC:{gen_imgs_pcc.mean().item():.6f}] [Gen PSNR:{gen_imgs_psnr.mean().item():.6f}] [Gen SSIM:{gen_imgs_ssim.mean().item():.6f}] [Gen LPIPS:{gen_imgs_lpips.mean().item():.6f}]')
