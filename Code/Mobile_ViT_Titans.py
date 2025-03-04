'''
Authors: Zhao Qi @ Cimda, CityU  22/01/2025
Training & Testing ViT-Titans (based on Mobile ViT & Titans) for vision-based obstacle avoidance
Ref: "Vision Transformers for End-to-End Vision-Based Quadrotor Obstacle Avoidance" by Bhattacharya, et. al
ViT-for-quadrotor-obstacle-avoidance: https://github.com/anish-bhattacharya/ViT-for-quadrotor-obstacle-avoidance
Mobile_ViT_V2: https://github.com/xmu-xiaoma666/External-Attention-pytorch/blob/master/model/attention/MobileViTv2Attention.py
Titans: https://zhuanlan.zhihu.com/p/18869835273
'''

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import LSTM
import torch.nn.utils.spectral_norm as spectral_norm

class MixTransformerEncoderLayer(nn.Module):
    # Ref: https://github.com/anish-bhattacharya/ViT-for-quadrotor-obstacle-avoidance/blob/main/models/ViTsubmodules.py
    def __init__(self, in_channels, out_channels, patch_size, stride, padding, 
                 n_layers, reduction_ratio, num_heads, expansion_factor=8):
        super().__init__()
        self.patchMerge = OverlapPatchMerging(in_channels, out_channels, patch_size, stride, padding) # B N embed dim
        self._attn = nn.ModuleList([EfficientSelfAttention2(out_channels, reduction_ratio, num_heads) for _ in range(n_layers)])
        self._lNorm = nn.ModuleList([nn.LayerNorm(out_channels) for _ in range(n_layers)])

    def forward(self, x):
        B,C,H,W = x.shape
        x,H,W = self.patchMerge(x) # B N embed dim (C)
        for i in range(len(self._attn)):
            x = x + self._attn[i].forward(x, H, W) #BNC
            # x = x + self._ffn[i].forward(x, H, W) #BNC
            x = self._lNorm[i].forward(x) #BNC
        x = x.reshape(B, H, W, -1).permute(0, 3, 1, 2).contiguous() #BCHW
        return x

class NeuralLongTermMemory(torch.nn.Module): # Ref: https://zhuanlan.zhihu.com/p/18869835273
    def __init__(self, d_model, hidden_dim, num_layers, forgetting_factor, lr_alpha = 1e-4):
        super().__init__()
        print("[SETUP] Establishing model ViT_Titans - TitansMAL - NeuralLongTermMemory")
        self.num_layers, self.forgetting_factor = num_layers, forgetting_factor  # Paper parameter alpha
        self.layers = torch.nn.ModuleList()
        in_dim = d_model
        for i in range(num_layers):
            out_dim = hidden_dim if i < num_layers - 1 else d_model
            self.layers.append(torch.nn.Linear(in_dim, out_dim))
            in_dim = out_dim

        self.momentum_buffer = None  
        self.lr_alpha = lr_alpha
    
    def forward(self, x):
        out = x
        for i, layer in enumerate(self.layers):
            out = layer(out)
            if i < self.num_layers - 1: out = torch.nn.functional.silu(out)
        return out
    
    def update_memory(self, x, target=None): # Ref: https://zhuanlan.zhihu.com/p/18869835273
        if target is None: target = torch.zeros_like(x)
        if not x.requires_grad: x = x.detach().requires_grad_(True)
        if not target.requires_grad: target = target.detach().requires_grad_(True)
        pred  = self.forward(x)
        loss  = torch.nn.functional.mse_loss(pred, target).requires_grad_(True)
        grads = torch.autograd.grad(loss, self.parameters(), retain_graph=True, create_graph=False, allow_unused=True)
        if self.momentum_buffer is None: self.momentum_buffer = [torch.zeros_like(p) for p in self.parameters()]

        with torch.no_grad():
            for (param, g, m_buf) in zip(self.parameters(), grads, self.momentum_buffer):                
                if not g is None: m_buf.mul_(self.forgetting_factor).add_(g)
            
            for param, m_buf in zip(self.parameters(), self.momentum_buffer):
                param.data.mul_(1 - self.forgetting_factor) # Forget
                param.data.add_(m_buf, alpha= - self.lr_alpha) # Update

        return loss.item()

class PersistentMemory(torch.nn.Module): # Ref: https://zhuanlan.zhihu.com/p/18869835273
    def __init__(self, num_slots, d_model):
        super().__init__()
        print("[SETUP] Establishing model ViT_Titans - TitansMAL - PersistentMemory")
        self.num_slots = num_slots
        self.memory = torch.nn.Parameter(torch.randn(num_slots))

    def forward(self, batch_size):
        pm = self.memory.expand(batch_size, self.num_slots).unsqueeze(0)
        return pm

class TitansMAL(torch.nn.Module): # Ref: https://zhuanlan.zhihu.com/p/18869835273
    def __init__(self, d_model, hidden_dim, lmm_layers, forgetting_factor, persistent_slots, lr_alpha = 1e-4):
        super().__init__() # Memory as a Layer (MAL)
        print("[SETUP] Establishing model ViT_Titans - TitansMAL")
        self.lmm = NeuralLongTermMemory(d_model+persistent_slots, hidden_dim, lmm_layers, forgetting_factor, lr_alpha)
        self.lmm_out = torch.nn.Linear(d_model+persistent_slots, 3)
        self.attn = EfficientSelfAttention2(3, reduction_ratio=1, num_heads=1)
        self.persistent_memory = PersistentMemory(num_slots=persistent_slots, d_model=d_model)
        self.persistent_slots  = persistent_slots

    def forward(self, x):
        x = x.unsqueeze(0)
        pm = self.persistent_memory(x.shape[1])
        x_with_pm = torch.cat([pm, x], dim=-1)
        out_lmm = self.lmm(x_with_pm)  # [batch_size, seq_len, d_model+persistend_slots]
        out_lmm = self.lmm_out(out_lmm)
        out  = self.attn(out_lmm,H=1,W=1)
        if self.persistent_slots != 0: loss = self.lmm.update_memory(x_with_pm, x_with_pm)
        
        out, out_lmm = out.squeeze(), out_lmm.squeeze()
        return out, out_lmm

class ViT_Titans(torch.nn.Module):
    def __init__(self, in_channels=1, inter_channels=16, out_channels=32, layers_a=2, layers_b=2, num_heads_a=1, num_heads_b=2,
        d_model=293, hidden_dim=3, lmm_layers=4, forgetting_factor=0.2, persistent_slots=16, lr_alpha=1e-6): 
        super().__init__()
        print("[SETUP] Establishing model ViT_Titans")
        self.encoder_blocks = torch.nn.ModuleList([MixTransformerEncoderLayer(in_channels=in_channels, out_channels=inter_channels, 
            patch_size=7, stride=4, padding=3, n_layers=layers_a, reduction_ratio=8, num_heads=num_heads_a),
            MixTransformerEncoderLayer(in_channels=inter_channels, out_channels=out_channels, 
            patch_size=3, stride=2, padding=1, n_layers=layers_b, reduction_ratio=4, num_heads=num_heads_b)])

        self.titans = TitansMAL(d_model, hidden_dim, lmm_layers, forgetting_factor, persistent_slots, lr_alpha)
        self.pxShuffle = torch.nn.PixelShuffle(upscale_factor=2)
        self.down_sample = torch.nn.Sequential(torch.nn.MaxPool2d(kernel_size=2, stride=2), torch.nn.Conv2d(24, 12, kernel_size=1, stride=2))

    def forward(self, X):
        if  X[2] is None: # Ref: https://github.com/anish-bhattacharya/ViT-for-quadrotor-obstacle-avoidance/blob/main/models/model.py
            X[2] = torch.zeros((X[0].shape[0], 4)).float().to(X[0].device)
            X[2][:, 0] = 1
        if  X[0].shape[-2] != 60 or X[0].shape[-1] != 90:
            X[0] = torch.nn.functional.interpolate(X[0], size=(60, 90), mode='bilinear')
        
        embeds = [X[0]]
        for block in self.encoder_blocks: embeds.append(block(embeds[-1]))
        out = embeds[1:] # out[1].shape: torch.Size([:, 32, 8, 12]); out[0].shape: torch.Size([:, 16, 15, 23])
        out = torch.cat([self.pxShuffle(out[1]), torch.nn.functional.pad(
            out[0], pad=(0, 1, 0, 1), mode='constant', value=0)], dim=1) # torch.Size([:, 24, 16, 24])
        out = self.down_sample(out) # torch.Size([:, 12, 4, 6])
        out = torch.cat([out.flatten(1), X[1]/10, X[2]], dim=1).float() # torch.Size([:, 293])
        out, h = self.titans(out) # torch.Size([:, 3])
        return out, h


