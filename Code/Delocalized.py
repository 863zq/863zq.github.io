# Delocalized information in optical speckles: entropy analysis 
# and condition for high-fidelity information retrieval
import argparse, os, h5py, datetime, math, random
import torch, torchvision, pytorch_msssim, vit_pytorch
import pytorch_lightning as pl
from torchvision import transforms
from torchmetrics.functional import pearson_corrcoef, structural_similarity_index_measure, peak_signal_noise_ratio

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

class Model(pl.LightningModule):
    def __init__(self, in_dim, out_dim):
        super().__init__()
        self.lr, self.in_dim, self.out_dim, self.val_step_outputs, self.training_step_outputs = opt.lr, in_dim, out_dim, [], []
        if opt.model_choose == 1: 
            self.model = torch.nn.Linear(in_dim*in_dim, out_dim*out_dim).to(torch.complex64)
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


