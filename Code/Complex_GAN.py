# codes for build Complex_GAN in "Extended Neural Network Generalizability 
# for High-fidelity Human Face Imaging from Spatiotemporally Decorrelated Speckles"

class UNet(torch.nn.Module):
    def __init__(self, UNet_channel_number=opt.UNet_channel_number):
        class Real_to_Complex(torch.nn.Module):
            def forward(self, input):
                return input + 1j * input
        class Complex_to_Real(torch.nn.Module):
            def forward(self, input):
                return input.abs()
        class Complex_conv2d(torch.nn.Module):
            def __init__(self, in_channels, out_channels, kernel_size=3, stride=1, padding=1, dilation=1, groups=1, bias=True):
                super(Complex_conv2d, self).__init__()
                self.conv = torch.nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding, dilation, groups, bias)
                self.conv = self.conv.to(torch.complex64)
            def forward(self, input): return self.conv(input)
        class Complex_ConvTranspose2d(torch.nn.Module):
            def __init__(self,in_channels, out_channels, kernel_size=4, stride=1, padding=0, output_padding=0, groups=1, bias=True, dilation=1, padding_mode='zeros'):
                super(Complex_ConvTranspose2d, self).__init__()
                self.conv_tran = torch.nn.ConvTranspose2d(in_channels, out_channels, kernel_size, stride, padding, output_padding, groups, bias, dilation, padding_mode)
                self.conv_tran = self.conv_tran.to(torch.complex64)
            def forward(self, input): return self.conv_tran(input)
        class Complex_Sigmoid(torch.nn.Module):
            def __init__(self, inplace=False):
                super(Complex_Sigmoid,self).__init__()
                self.sigmoid = torch.nn.Sigmoid()
                self.sigmoid = self.sigmoid.to(torch.complex64)
            def forward(self, input): return self.sigmoid(input)
        class Complex_ReLU(torch.nn.Module):
            def __init__(self, inplace=False):
                super(Complex_ReLU, self).__init__()
                self.ReLU = torch.nn.ReLU(inplace)
            def forward(self, input):
                return self.ReLU(input.real) + 1j * self.ReLU(input.imag)
        class Complex_batch_norm2d(torch.nn.Module):
            def __init__(self, num_features, eps=1e-5, momentum=0.1, affine=True):
                super(Complex_batch_norm2d, self).__init__()
                self.bn = torch.nn.BatchNorm2d(num_features, eps, momentum, affine, track_running_stats = False)
            def forward(self, input): 
                return self.bn(input.real) + 1j * self.bn(input.imag)
        class Complex_dropout2d(torch.nn.Module):
            def __init__(self, drop_rate, inplace=False):
                super(Complex_dropout2d,self).__init__()
                self.dropout = torch.nn.Dropout2d(drop_rate,inplace)
            def forward(self, input):
                return self.dropout(input.real) + 1j * self.dropout(input.imag)       

        class DenseBlock(torch.nn.Module):
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
                                
        class down(torch.nn.Module):
            def __init__(self, in_ch=1, out_ch=1, kernel_size=4, padding=1, stride=2):
                super(down, self).__init__()
                self.same = torch.nn.Sequential(DenseBlock(out_ch=out_ch, in_ch=in_ch))
                self.d = torch.nn.Sequential(Complex_conv2d(out_ch, out_ch, kernel_size, stride, padding), 
                    Complex_batch_norm2d(out_ch), Complex_ReLU())
            def forward(self, x):
                x_skip = self.same(x)
                return x_skip, self.d(x_skip)

        class up(torch.nn.Module):
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
        self.s1_up   = up (UNet_channel_number, UNet_channel_number*2, 32)
        if opt.speckle_size == 128: self.output = torch.nn.Sequential(Complex_conv2d(32, 1, kernel_size=3, stride=2, padding=1), Complex_Sigmoid())
        if opt.speckle_size == 256: self.output = torch.nn.Sequential(Complex_conv2d(32, 1, kernel_size=3, stride=4, padding=1), Complex_Sigmoid())
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
        self.UNet = UNet(opt.UNet_channel_number)
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
        if opt.img_size == 64: 
            self.conv_blocks = torch.nn.Sequential(self.conv_blocks,*discriminator_block(16, 16))
        self.val_layer = torch.nn.Sequential(torch.nn.Linear(16, 1), torch.nn.Sigmoid())
    def forward(self, image):
        return self.val_layer(self.conv_blocks(image).reshape(image.shape[0],-1))
