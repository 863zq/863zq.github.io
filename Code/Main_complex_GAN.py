# Main file for "Extended Neural Network Generalizability for High-fidelity Human Face Imaging from Spatiotemporally Decorrelated Speckles"

# Complex conv from PyTorch 2.0 is used in generator(UNet)
# Add complex Relu and BatchNorm, add complex_dropout for Dense_block, add data-sampler for diffuser results
# GAN ref: https://github.com/eriklindernoren/PyTorch-GAN/blob/master/implementations/acgan/acgan.py
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
# parser.add_argument("--kaiming_normal",type=int,  default=0,   help="Apply kaiming_normal")
parser.add_argument("--epoch_change_loss", type=int, default=3,  help="Final several epochs will change loss to use LPIPS")
parser.add_argument("--lpips_net_type", type=str, default='vgg', help="Learned Perceptual Image Patch Similarity net_type:vgg,alex,squeeze")
parser.add_argument("--update_on_final_epoch", type=int,default=1,help="1:update parameters on final epoch, 0:not")

