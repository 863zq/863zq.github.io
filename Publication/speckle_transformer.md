## Speckle transformer: direct classification through scattering media with limited information

**Author:** <u>Qi Zhao†</u>, Zhiyuan Wang†, Zhipeng Yu†, Tianting Zhong†, Haoran Li, Shengfu Cheng, Haofan Huang, Chi Man Woo, Huanhao Li\*, and Puxiang Lai\*

**Corresponding author:** Huanhao Li* (Bi-optoelectronic-integration and Medical Instrumentation Laboratory, Guangzhou Institute of Technology, Xidian University) lihuanhao@xidian.edu.cn

**Corresponding author:** Puxiang Lai* (Department of Biomedical Engineering, Hong Kong Polytechnic University) puxiang.lai@polyu.edu.hk

**[DOI: TBD/TBD](https://doi.org/)**

**Abstract:** Retrieving high-fidelity images from optical speckles remains challenging, especially when the information in speckles is severely insufficient. To address classification through scattering media under such constraints, we propose Speckle Transformer, a vision transformer-based model that directly classifies objects using raw speckle patterns without intermediate image retrieval. By leveraging inherent features within speckles to extract discriminative features, our approach achieves nearly 90% accuracy for classifying speckles encoded with different images, outperforming traditional retrieval-classification pipelines by up to five times even with extreme information sparsity (i.e., 1/1024 speckle regions of interest). In addition, we quantify speckle information capacity via information entropy analysis, demonstrating that classification accuracy correlates strongly with the information entropy of speckle autocorrelation. We not only overcome limitations of conventional methods but also establish a paradigm for real-time classification in scattering environments with constrained data.

![Algorithm](/Publication/speckle_transformer.jpg)

_Direct classification versus retrieval-classification. (a) The first row in each panel: Speckle Transformer accuracies (markedonthebottomofcorrespondingcroppedspeckles)fordecreasing speckle ROIs (full to 1/1024); The second row in each panel: Retrieval-classification accuracies (marked on the bottom of corresponding retrieved images) and Pearson correlation coefficients (PCC) (marked on the top of corresponding retrieved images) between retrieved images and ground truths. Note the widening performance gap as information decreases. (b) Classification accuracy curves confirming Speckle Transformer’s superiority under information scarcity. (c) Classification of partitioned MNIST images showing high spatial dependency regardless of method. The scale bars represent the size of speckles on the camera. The color bar indicates the normalized intensity of speckles or images._