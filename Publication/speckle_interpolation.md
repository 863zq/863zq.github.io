## Learning-based super-resolution interpolation for sub-Nyquist sampled laser speckles

> Huanhao Li†, Zhipeng Yu†, <u>Qi Zhao†</u>, Yunqi Luo, Shengfu Cheng, Tianting Zhong,
> Chi Man Woo, Honglin Liu, Lihong V. Wang*, Yuanjin Zheng*, Puxiang Lai*
> 
> Lihong V. Wang* (Caltech Optical Imaging Laboratory, Andrew and Peggy Cherng Department of Medical Engineering, 
> California Institute of Technology) LVW@caltech.edu
> 
> Yuanjin Zheng* (School of Electrical and Electronics Engineering, Nanyang Technological University) yjzheng@ntu.edu.sg
>  
> Puxiang Lai* (Department of Biomedical Engineering, Hong Kong Polytechnic University) puxiang.lai@polyu.edu.hk
> 
> [DOI: 10.1364/PRJ.472512](https://doi.org/10.1364/PRJ.472512)
> 
> _Information retrieval from visually random optical speckle patterns is desired in many scenarios yet considered 
> challenging. It requires accurate understanding or mapping of the multiple scattering process, or reliable capability 
> to reverse or compensate for the scattering-induced phase distortions. In whatever situation, effective resolving 
> and digitization of speckle patterns are necessary. Nevertheless, on some occasions, to increase the acquisition 
> speed and/or signal-to-noise ratio (SNR), speckles captured by cameras are inevitably sampled in the sub-Nyquist 
> domain via pixel binning (one camera pixel contains multiple speckle grains) due to finite size or limited 
> bandwidth of photosensors. Such a down sampling process is irreversible; it undermines the fine structures 
> of speckle grains and hence the encoded information, preventing successful information extraction. To retrace 
> the lost information, super resolution interpolation for such sub-Nyquist sampled speckles is needed. In this 
> work, a deep neural network, namely SpkSRNet, is proposed to effectively upsample speckles that are sampled 
> below 1/10 of the Nyquist criterion to well resolved ones that not only resemble the comprehensive morphology 
> of original speckles (decompose multiple speckle grains from one camera pixel) but also recover the lost complex 
> information (human face in this study) with high fidelity under normal and low light conditions, which is 
> impossible with classic interpolation methods. These successful speckle super-resolution interpolation demonstrations 
> are essentially enabled by the strong implicit correlation among speckle grains, which is non-quantifiable but 
> could be discovered by the well-trained network. With further engineering, the proposed learning platform may 
> benefit many scenarios that are physically inaccessible, enabling fast acquisition of speckles with sufficient 
> SNR and opening up new avenues for seeing big and seeing clearly simultaneously in complex scenarios._

![Algorithm](/Publication/speckle_interpolation.jpg)

_Architecture of SpkSRNet is the combination of ResNeXt and PixelShuffle layers. nd0-sampled 
speckles with dimension of 252/n×252/n are input into the SpkSRNet for speckle super resolution 
(i.e., interpolation) processing (n=4, 8, 12, 18, 21, 28), with d0 sampled speckles (i.e.,
the original speckles with dimension of 252×252) as the target. For example, when the down 
sampling factor (n) is 12, the network is called 12d0-trained SpkSRNet, whose input dimension 
is 21×21 and output dimension is 252×252._
