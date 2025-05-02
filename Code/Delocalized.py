# Delocalized information in optical speckles: entropy analysis 
# and condition for high-fidelity information retrieval
import argparse, os, h5py, datetime, math, random
import torch, torchvision, pytorch_msssim, vit_pytorch
import pytorch_lightning as pl
from torchvision import transforms
from torchmetrics.functional import pearson_corrcoef, structural_similarity_index_measure, peak_signal_noise_ratio

def autocorrelation(spk): # Derive speckle autocorrelation
    # Ref https://github.com/qhzhang95/PEACE_Speckle/blob/main/1_read%20the%20raw%20image%20and%20calculate%20the%20autocorrelations.ipynb
    spk = (spk-spk.min())/(spk.max()-spk.min()) # Normalization
    at = torch.fft.fft2(spk).abs().pow(2)
    at = torch.fft.ifftshift(torch.fft.ifft2(at))/spk.shape[0]/spk.shape[1]
    at = (torch.abs(at)-torch.mean(spk)**2)/(torch.mean(spk**2)-(torch.mean(spk))**2)
    at = at - (torch.mean(at)).min() # subtract background
    return at
    
def entropy(x,bit=16): # Derive entropy of input
    x = torch.ceil(x*2**bit)
    _,count = torch.unique(x,return_counts=True)
    count   = count/count.sum()
    result  = -(count*torch.log2(count)).sum()
    return result

class Model(pl.LightningModule):
    def __init__(self, lr, in_dim, out_dim):
        super().__init__()
        self.lr, self.in_dim, self.out_dim = lr, in_dim, out_dim
        self.model = torch.nn.Linear(in_dim*in_dim, out_dim*out_dim).to(torch.complex64)
    def forward(self,x):
        x = x.reshape(-1, self.in_dim*self.in_dim).to(torch.complex64)
        x = self.model(x).abs().reshape(-1, 1, self.out_dim, self.out_dim)
        return x


