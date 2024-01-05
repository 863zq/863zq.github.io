## Speckle-Based Optical Cryptosystem and its Application for Human Face Recognition via Deep Learning

> <u>Qi Zhao†</u>, Huanhao Li†, Zhipeng Yu†, Chi Man Woo, Tianting Zhong, Shengfu Cheng, Yuanjin Zheng, Honglin Liu,
> Jie Tian*, Puxiang Lai*
> 
> Jie Tian* (School of Medical Science and Engineering, Beihang University) tian@ieee.org
> 
> Puxiang Lai* (Department of Biomedical Engineering, Hong Kong Polytechnic University) puxiang.lai@polyu.edu.hk
> 
> [DOI: 10.1002/advs.202202407](https://doi.org/10.1002/advs.202202407)
> 
> _Face recognition has become ubiquitous for authentication or security purposes. 
> Meanwhile, there are increasing concerns about the privacy of face images, which are 
> sensitive biometric data and should be protected. Software-based cryptosystems are 
> widely adopted to encrypt face images, but the security level is limited by insufficient 
> digital secret key length or computing power. Hardware-based optical cryptosystems can 
> generate enormously longer secret keys and enable encryption at light speed, but most 
> reported optical methods, such as double random phase encryption, are less compatible 
> with other systems due to system complexity. In this study, a plain yet highly efficient 
> speckle-based optical cryptosystem is proposed and implemented. A scattering ground glass 
> is exploited to generate physical secret keys of 17.2 gigabit length and encrypt face images 
> via seemingly random optical speckles at light speed. Face images can then be decrypted from 
> random speckles by a well-trained decryption neural network, such that face recognition can 
> be realized with up to 98% accuracy. Furthermore, attack analyses are carried out to show 
> the cryptosystem's security. Due to its high security, fast speed, and low cost, the 
> speckle-based optical cryptosystem is suitable for practical applications and can inspire 
> other high-security cryptosystems._


![Algorithm](/Publication/speckle_based_cryptosystem.jpg)

_The flowchart of the proposed cryptosystem for face recognition. a) Speckle encryption: 
face images (plaintext) are loaded on a spatial light modulator (SLM) to generate the 
corresponding speckles (ciphertext) when coherent light reflected by the SLM transmits 
through a scattering medium, which serves as the unique physical secret key. The ciphertext 
is safely transferred and stored via the cloud. No face images need to be kept in the database 
after encryption. b) Learning-based decryption: a neural network is trained in advance to link 
the plaintext with the ciphertext. After training, new random speckle patterns (ciphertext) 
are directly fed into the neural network for decryption, and the decrypted face images are 
then utilized for face recognition. c) Face recognition: the camera-recorded face images are 
encoded to unique 128-dimensional vectors of each known face image. After decryption, the 
face encoding distances between the decrypted images and the known face encodings are computed: 
if the encoding distance is less than a pre-set threshold, the face recognition result is “Match” 
(the same person), otherwise it is “Mismatch” (different people). Plaintext image: Reproduced 
under terms of the CC-BY 2.0 license. Copyright 2015, Lawrence Lessig at Second Home London, 
by Innotech Summit, Flickr (https://www.flickr.com/photos/115363358@N03/18260388752/). The 
original image is cropped and converted to gray-scale._
