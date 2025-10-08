<table>
  <tr>
    <td style="width:60%;"><img src="/Publication/PhD_thesis/PPT%20(1).JPG" width="100%"/></td>
    <td style="width:40%;">Dear Professors, thank you for joining the oral defense today. I am Zhao Qi from HK PolyU, Department of BME. And my supervisor is Prof. Lai. The title of my presentation is Understanding and manipulation of optical speckles.</td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(2).JPG" width="100%"/></td>
    <td style="width:60%;">First, let me give a brief self-introduction. My educational journey has been a continuous pursuit of knowledge. I got Bachelor’s degree from NWPU in EIE. Then I went to TBSI for Master’s degree in DS. Currently, I am pursuing a PhD at PolyU, BME. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(3).JPG" width="100%"/></td>
    <td style="width:60%;"> Before going into detailed research, I will give some background information. Due to non-ionizing, high resolution, structured & functional information, Optics have been widely applied in scientific research, including imaging, diagnosis, therapy, and anipulation. As shown in the figure, we can get clear images of cells using con-focal and two-photon. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(4).JPG" width="100%"/></td>
    <td style="width:60%;"> However, in deep tissues, scattering raises a significant challenge, leading to optical speckles with bright and dark spots, rather than clear images.  </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(5).JPG" width="100%"/></td>
    <td style="width:60%;"> As a result, a question arises: CAN we retrieve information from speckles? The answer is YES. Researchers in computational optics have discovered that, Speckles contain retrievable information, and we can build a transmission matrix model TM. The input wavefront information and output speckles can be related by TM.  </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(6).JPG" width="100%"/></td>
    <td style="width:60%;"> If the input wavefront is modulated, we can compensate for scattering to achieve optical focus through scattering media. Then, imaging through biological tissues is achieved through raster scanning. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(7).JPG" width="100%"/></td>
    <td style="width:60%;"> Based on TM models, researchers have developed wavefront shaping for overcoming speckles. One ease of implementation method is iterative wavefront shaping. Iterative wavefront shaping involves iteratively modulating the wavefront based on feedback signals. Another method is transmission matrix measurement. By projecting lots of patterns and recording output speckles, the transmission matrix can be derived. And we can derive the patterns to compensate for scattering. However, some challenges persist, such as the efficiency of algorithms and low hardware speed. As a result, real-time focusing in biological tissues is still difficult. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(8).JPG" width="100%"/></td>
    <td style="width:60%;"> The above-mentioned computational optics leverage the physical model TM. To move forward, with the development of deep learning, we can address more complex problems in scattering media. Here, we can use known speckle image pairs to train networks. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(9).JPG" width="100%"/></td>
    <td style="width:60%;"> Then, deep neural networks can extract various dimensions of features from speckles.  And the pre-trained neural networks can directly retrieve image information from speckles with high fidelity. These are brief background information about my research. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(10).JPG" width="100%"/></td>
    <td style="width:60%;"> Following the background, I will outline five studies related to Understanding and manipulation of speckles. The studies are categorized under three themes: Overcoming speckles, Understanding speckles, and Utilizing speckles. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(11).JPG" width="100%"/></td>
    <td style="width:60%;"> As for Overcoming speckles: a Parameter-free algorithm for iterative wavefront shaping is proposed for optical focusing. The algorithms address the challenges of time-consuming and experience-dependent parameter tuning process. This research set the foundation for the following research.  </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(12).JPG" width="100%"/></td>
    <td style="width:60%;"> As for Understanding speckles, the studies are divided into three sections: The first one is to utilize GAN for image retrieval from speckles in non-stationary scattering media. This is an extension of the focusing capabilities developed in iterative wavefront shaping. Although WFS can achieve imaging through scattering media, raster scanning takes a long time. Deep learning can directly retrieve images from speckles, but its adaptability is still limited. This research emphasizes the adaptability to new scattering medium statuses, for long-term image retrieval from decorrelated speckles. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(12).JPG" width="100%"/></td>
    <td style="width:60%;"> Another research is to explore delocalized information in speckles and propose a basic theory of speckle-related research. Lots of research has been focused on retrieving information from speckles. But some basic theories have NOT been explored, such as how information is distributed in speckles, and the conditions under which images can be retrieved from speckles. In this research, we utilize deep learning and information entropy to explore the delocalized information in speckles. And we propose that, only if speckle autocorrelation entropy is greater than image autocorrelation entropy, information can be retrieved from speckles with high-fidelity. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(12).JPG" width="100%"/></td>
    <td style="width:60%;"> The third research synthesizes the previous research, and proposes direct classification through scattering media. We have mentioned that, information in speckles may NOT be enough for image retrieval, and then classification accuracy is lower due to blurry retrieved images. Here, we propose Speckle Transformer for direct classification based on speckles to achieve higher accuracy and bypass image retrieval before classification. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(13).JPG" width="100%"/></td>
    <td style="width:60%;"> As for the final research, the focus is transferred from overcoming speckles to utilizing speckles: Due to their inherent randomness, we propose to use speckles as ciphertexts in cryptosystems. We introduce a plain yet highly efficient speckle-based cryptosystem, for encrypted face recognition. A piece of scattering ground glass is utilized as a physical secret key, for superior security, light-speed encryption, and low-cost. Overall, my research journey is from overcoming speckles, understanding speckles, to utilizing speckles. We believe these studies will significantly advance the fields of speckle imaging and biomedical optics. Following these outlines, I will delve into the details of these research. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(14).JPG" width="100%"/></td>
    <td style="width:60%;"> The first research is the Parameter-Free Algorithm for iterative Wavefront Shaping. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(15).JPG" width="100%"/></td>
    <td style="width:60%;"> Iterative WFS can overcome speckles and focus through scattering media. However, WFS relies heavily on feedback signals to optimize wavefronts. And the related algorithms contain lots of parameters to be tuned. The parameter tuning process is time-consuming and dependent on specific samples and environments. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(16).JPG" width="100%"/></td>
    <td style="width:60%;"> In this research, we have developed a Parameter Free Algorithm PFA. PFA combines the concepts of genetic algorithm, bat algorithm, and dynamic mutation algorithm. And the crucial aspect of PFA is its ability to derive the dynamic mutation rate, which is in direct proportion to the wrong units that NEGATIVELY contribute to focus. According to TM, speckle U is the result of correct units and wrong units on DMD. And we want to get more CORRECT units. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(17).JPG" width="100%"/></td>
    <td style="width:60%;"> After analyzing U, we can derive the ratio of correct units C from focusing efficiency η eta. The dynamic mutation rate P is then related to η eta and the number of bats h. Then, P will be applied in the parameter-free algorithm. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(18).JPG" width="100%"/></td>
    <td style="width:60%;"> The flow chart of PFA is shown in the figure. First, all the candidate bats are randomly initialized. Then, all the bats are ranked and cross-fertilized. Next, the most important step is to derive the dynamic mutation rate P and dynamically mutate the new bats. Through iterative optimization, the solutions can be updated and we can finally focus through scattering media. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(19).JPG" width="100%"/></td>
    <td style="width:60%;"> The experimental setup is shown on the right. The source laser is expanded, and then modulated by a DMD. The modulated laser then passes through the scattering medium, ground glass. A camera captures the feedback signals to be utilized in PFA. Then, after lots of iterations, PFA derives the optimal DMD patterns and achieves focusing through scattering media. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(20).JPG" width="100%"/></td>
    <td style="width:60%;"> Next, PFA is evaluated in experiments. In Figure A, we demonstrate the focusing enhancement ratios. It’s clear that, Well-tuned parameters significantly outperform improperly tuned parameters. As a result, it’s important to tune parameters in other algorithms. However, the proposed PFA eliminates the need for parameter tuning, and achieves better focusing enhancement ratios than other algorithms. In Figure B, the intensity is shown, and PFA shows the highest focusing intensity. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(21).JPG" width="100%"/></td>
    <td style="width:60%;"> Furthermore, we test PFA using different scattering media, including ground glass and multimode fiber. As we can see, although the absolute enhancement ratios are not the same, the independence of performance on the number of bats is consistent. Overall, PFA not only shows better performance, but also avoids the time-consuming and experience-dependent parameter tuning process. And with the help of FPGA, real-time optical focusing through biological tissues will be possible in the future. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(22).JPG" width="100%"/></td>
    <td style="width:60%;"> Next, the focusing ability is extended to imaging. And we will talk about using neural networks to address image retrieval from spatiotemporally decorrelated speckles. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(23).JPG" width="100%"/></td>
    <td style="width:60%;"> Neural networks can be utilized to retrieve images from speckles. However, once the scattering medium is disturbed by environments, these methods may NOT work well. Because the initial and subsequent speckles lost correlation, and neural networks can NOT extract features from decorrelated speckles efficiently. Here, we propose a GAN-based framework to address speckle decorrelation. The optical setup remains largely unchanged, but we load face images onto SLM. The duration of each data group in experiments is up to 40 minutes. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(24).JPG" width="100%"/></td>
    <td style="width:60%;"> In Figure B, we evaluate the stability of speckles. Here, we calculated the Speckle Background PCC, SBP, by comparing captured background speckles with the initial background speckle. In these curves, SBP of six groups continuously decays with time due to perturbations. Lower SBP corresponds to a higher decorrelation from the initial state, and results in lower stability. For instance, the final SBP of Group 1 is 0.8846, indicating relatively stable conditions. While, the final SBP of Group 6 is 0.0139, indicating highly UNSTABLE conditions, because 0.0139 is less than 1/e. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(25).JPG" width="100%"/></td>
    <td style="width:60%;"> Then, the proposed Generative Adversarial Network GAN is shown in the figure. The GAN consists of a U-Net based generator to extract features from speckles. Here, the convolutions in U-Net are complex valued, in order to more accurately mimic the random scattering process. And a convolutional discriminator is designed to evaluate the retrieved images and help the generator to improve the retrieved images during training. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(26).JPG" width="100%"/></td>
    <td style="width:60%;"> Next, the GAN will be tested. Different from other research, we have separated the training and testing datasets with different time intervals delta_t, in order to ensure NO overlap between training and testing data acquisition. This strategy allows us to assess GAN’s performance under different degrees of decorrelation. As we can see, with a training dataset duration T of 30 minutes, Group 1 achieves high PCC over 0.95 with high fidelity. And with larger time intervals, PCC is lower due to higher decorrelation. As for Group 4, PCC is still greater than 0.90. As for highly non-stationary conditions in Group 6, performance deteriorates. And PCC is much lower, especially for delta_t of 10 min. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(27).JPG" width="100%"/></td>
    <td style="width:60%;"> More results are summarized in Figure C and D. We can see that, GAN can address decorrelated speckles to some extent, and shorter training durations and longer intervals will result in worse retrieved images. Furthermore, GAN is compared with other networks in Figure E. And GAN outperforms counterparts in retrieving images from decorrelated speckles. Overall, GAN shows spatiotemporal generalizability to adapt to NEW scattering medium statuses that are NOT present in the training data. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(28).JPG" width="100%"/></td>
    <td style="width:60%;"> To further validate the GAN, we tested it over longer periods. Here, we use a disordered metasurface as the scattering medium. The training data are collected on Day 1, the testing data are collected on Day 2, and the optical system is turned off for 37 hours between Day 1 and Day 2. The results show that, The trained network on Day 1 can retrieve images from speckles on Day 2. Overall, the proposed method will help the applications of speckle imaging in practical applications, such as imaging through biological tissues or imaging under bad weather conditions. Furthermore, new network structures, large models, and optical computing can be utilized to further improve the GAN. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(29).JPG" width="100%"/></td>
    <td style="width:60%;"> Just now, we have discussed training neural networks to retrieve information from speckles, but the theories about information in speckles need exploration. Next, we will delve into the basic theories about how information is delocalized in speckles and the conditions for information retrieval from speckles. </td>
  </tr>


  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(30).JPG" width="100%"/></td>
    <td style="width:60%;"> First, we compare ballistic imaging and speckles. In ballistic imaging, light travels along ballistic channels from the object plane to the image plane, and we can get clear images. Here, one pixel on the image plane corresponds to a single or an array of pixels on the object plane. And when ballistic light is blocked, the lost part can NOT be retrieved with trusted fidelity. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(31).JPG" width="100%"/></td>
    <td style="width:60%;"> However, when light encounters strong scattering, we just get optical speckles. Here, one pixel in speckles is associated with all the pixels in images, and one pixel in images is delocalized to all the pixels in speckles. Then, when some channels are blocked, photons can still pass through other channels, and information can still be retrieved from speckles. This delocalization phenomenon is very different from ballistic imaging. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(32).JPG" width="100%"/></td>
    <td style="width:60%;"> Next, we will explore the physical theory of delocalization. As for the transmission matrix model, through TM matrix multiplication, one element in speckle U results from all elements in image e, and one element in image e spreads to all elements in speckle U. As a result, it’s clear that, Image information E becomes delocalized in speckles U. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(33).JPG" width="100%"/></td>
    <td style="width:60%;"> Further analysis involves information entropy. Wavefronts are distorted by the scattering medium at the Fourier plane, we can derive that Speckle autocorrelation is the convolution of image autocorrelation and point spread function autocorrelation. From another point of view, the concept of entropy has been widely used in analyzing image information, and it has been introduced in research of optical scattering. Information entropy H is defined according to the intensity distribution of images, and a higher intensity variance indicates more information. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(34).JPG" width="100%"/></td>
    <td style="width:60%;"> And due to the nature of information, it is difficult to compensate for entropy loss using neural networks. Then, combining the autocorrelation relationship and information entropy, we propose that, The entropy of speckle autocorrelation should be greater than entropy of image autocorrelation, in order to retrieve information from speckles with high fidelity. In other words, speckles should include sufficient information; otherwise, the retrieved images are of low quality. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(35).JPG" width="100%"/></td>
    <td style="width:60%;"> To validate the proposed theory, we compare the experiments of ballistic imaging and speckles. First, training neural networks to retrieve information from partial images results in low-quality images. As shown in Figure C, PCC is just 0.6. Partial images lost some information, and the lost information can NOT be recovered by neural networks. Only the regions corresponding to partial images can be clearly retrieved, but other regions are just some common facial features, or artifacts. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(36).JPG" width="100%"/></td>
    <td style="width:60%;"> On the contrary, retrieving images from partial speckles shows much better results with PCC greater than 0.9. The retrieved face images keep detailed facial features such as eyes, mouths, and noses. In other words, partial speckles keep sufficient information about the whole faces to retrieve images. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(37).JPG" width="100%"/></td>
    <td style="width:60%;"> Next, we crop speckles into different regions of interests ROI, in order to examine entropy relationships between speckle autocorrelation and image autocorrelation. The entropy of the image autocorrelation is 10.94 bits. As for speckle ROIs of 256, 128, and 85, entropies of speckle autocorrelation are all greater than entropy of image autocorrelation. As for speckle ROIs of 64, entropy of speckle autocorrelation is very close. Overall, retrieved images are all satisfying, because speckles contain enough information to retrieve images with high fidelity. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(38).JPG" width="100%"/></td>
    <td style="width:60%;"> As for speckle ROIs of 51, entropy of speckle autocorrelation is lower than H[Auto(img)] entropy of the image autocorrelation. As for speckle ROIs of 42, 36, and 32, entropy of speckle autocorrelation is much lower. As a result, retrieved images are blurry, since information in speckles is NOT enough to retrieve images with high fidelity. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(39).JPG" width="100%"/></td>
    <td style="width:60%;"> Furthermore, the results are summarized in the curve. As we can see, when speckle autocorrelation entropy is more than image autocorrelation entropy on the left side, images retrieved from speckles show high fidelity, and PCC is greater than 0.9. Overall, we explore delocalized information in speckles from an entropy perspective. And we propose the necessary condition for retrieving delocalized information from speckles with high fidelity. And the theory can be applied in speckle-related applications, such as speckle imaging, speckle classification, and non-line-of-sight imaging. </td>
  </tr>


  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(40).JPG" width="100%"/></td>
    <td style="width:60%;"> Just now, we have proposed that, Insufficient speckle information leads to blurry retrieved images, and the subsequent classification or recognition tasks based on blurry retrieved images are challenging. To address this issue, we propose direct classification through scattering media. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(41).JPG" width="100%"/></td>
    <td style="width:60%;"> As for seeing through scattering media, sometimes we just need classification results, and retrieving clear target images is NOT necessary. Here, we introduce the Speckle Transformer, a vision transformer-based model to leverage the limited information in speckles and extract speckle features for direct classification through scattering media. Unlike conventional methods to retrieve images before classification, Speckle Transformer bypasses the need for image retrieval, and extracts features from the limited information in speckles for direct classification. The optical setup in Figure A involves loading digits onto SLM. And the structure of Speckle Transformer is shown in Figure B. The Transformer encoder incorporates multi-head attention and multi-layer perceptron to process the speckle data and extract speckle features for direct classification. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(42).JPG" width="100%"/></td>
    <td style="width:60%;"> Next, we compare classification based on retrieved images, and direct classification based on Speckle Transformer. As for full speckles and quarter speckles, the results show minimal differences. The reason is that, Speckles contain sufficient information for image retrieval, and retrieved images are easy to classify. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(43).JPG" width="100%"/></td>
    <td style="width:60%;"> However, as for smaller speckle ROI, including 1/64 and 1/256, direct classification based on Speckle Transformer results in higher accuracy than classification after retrieval, as shown in the figures and curves. The reason is that, when speckles contain insufficient information, images retrieved from these speckles are blurry. As a result, the retrieved images are difficult to classify. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(44).JPG" width="100%"/></td>
    <td style="width:60%;"> Overall, Speckle Transformer extracts speckle features for direct classification. And direct classification can utilize delocalized information for higher accuracies than classification after retrieval. In the future, Speckle Transformer can be applied in non-line-of-sight classifications and privacy-protected classifications. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(45).JPG" width="100%"/></td>
    <td style="width:60%;"> Until now, we primarily focus on overcoming speckles and retrieving information from speckles. From another point of view, due to the inherent randomness of speckles, speckles are actually an ideal candidate as ciphertexts, for securing private data in cryptosystems. Next, we will introduce a speckle-based optical cryptosystem. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(46).JPG" width="100%"/></td>
    <td style="width:60%;"> As we are all aware, face recognition applications are everywhere in public places. And face features are extracted and recognized for identification. However, face images contain private information. Since people can hardly change their appearance, if face recognition data were stolen, hackers might utilize these data. As a result, face image data should be secured by cryptosystems. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(47).JPG" width="100%"/></td>
    <td style="width:60%;"> In order to protect these data, software-based cryptosystems and hardware-based cryptosystems have been proposed. Software-based cryptosystems have been widely applied. The common key lengths range from dozens to hundreds, in order to balance between security and encryption speed. The limited key length is susceptible to quantum computing and optical computing. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(48).JPG" width="100%"/></td>
    <td style="width:60%;"> Hardware-based cryptosystems utilize physical secret keys and have much longer secret key lengths. Thus, hardware-based cryptosystems are more secure than software-based cryptosystems. As one representative, speckle-based cryptosystem does NOT involve computation during encryption, and light-speed encryption can be achieved. However, speckle-based cryptosystems are limited to simple-structured images, such as digits. The main difficulty here is to retrieve face images from speckles with high fidelity using transmission matrix models. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(49).JPG" width="100%"/></td>
    <td style="width:60%;"> In this research, we propose a speckle-based cryptosystem for encrypted face recognition. The diagram is mainly divided into encryption, decryption, and recognition. Next, we will go to more details. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(50).JPG" width="100%"/></td>
    <td style="width:60%;"> During encryption, face images are loaded onto SLM to modulate wavefronts. The modulated laser transmits through the scattering medium, and the optical speckles are captured by a camera. Here, the scattering medium is the physical secret key. And encryption can proceed at the speed of light. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(51).JPG" width="100%"/></td>
    <td style="width:60%;"> During decryption, a UNet-based neural network is designed to retrieve images from speckles. Before decryption, the neural network is trained with lots of image-speckle pairs from the same scattering medium, in order to achieve high-fidelity image retrieval for face recognition. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(52).JPG" width="100%"/></td>
    <td style="width:60%;"> Finally, the decrypted images can be further used in face recognition. In this research, we utilize an open-source Python face-recognition library. The algorithm encodes the face features into unique 128-dimension vectors. Then the distances between different face encodings are compared. If the distance is less than the pre-set threshold of 0.6, the two face images are recognized as the same person; otherwise, different people. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(53).JPG" width="100%"/></td>
    <td style="width:60%;"> Overall, in the speckle-based cryptosystem, face images are encrypted into speckles. Then speckles are decrypted by the pre-trained neural network, and the decrypted images are used for face recognition. The private data are encrypted into random speckles, and the physical secret key length is 17.2 gigabit. As a result, it is nearly impossible to crack speckle encryption by conventional computers. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(54).JPG" width="100%"/></td>
    <td style="width:60%;"> Then we experimentally test the cryptosystem. In the figure, plaintext, ciphertext, and decrypted images are shown. PCC between ground-truth and decrypted images are all greater than 0.9. The decrypted images are retrieved with high fidelity, and specific facial features are kept. However, if we use the wrong physical secret keys for encryption, the decrypted results are obscure. And the retrieved images can NOT be used for face recognition. As a result, the security of the cryptosystem can be guaranteed. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(55).JPG" width="100%"/></td>
    <td style="width:60%;"> Next, the retrieved face images are recognized. Face recognition results are shown in the figure. As we can see, decrypted images look very similar to ground truths and are recognized as MATCH. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(56).JPG" width="100%"/></td>
    <td style="width:60%;"> However, if the distance is greater than 0.6, the face recognition result is MISMATCH. Overall, the recognition accuracy is up to 98%. And this is the first demonstration of the speckle-based cryptosystem for encrypted face recognition, which shows high potential in practical applications. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(57).JPG" width="100%"/></td>
    <td style="width:60%;"> To summarize, my PhD research focus on overcoming speckles, understanding speckles, and utilizing speckles. The proposed parameter-free algorithm PFA overcomes optical speckles and avoids time-consuming parameter tuning process in iterative wavefront shaping. Then, the focusing ability of wavefront shaping is extended to image retrieval from speckles, and we propose GAN models to address spatiotemporally decorrelated speckles. To go deeper, we analyze the delocalized information in speckles from an entropy perspective, and propose the speckle sampling condition for image retrieval from speckles with high fidelity. Last but not the least, we utilize the inherent randomness of speckles and propose a speckle-based cryptosystems. Overall, these studies pave the way for speckle-related research and applications. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(58).JPG" width="100%"/></td>
    <td style="width:60%;"> As for future work, there are five studies. First, we plan to implement PFA on FPGA for real-time focusing through scattering media. And sophisticated algorithms for addressing speckle decorrelation will be developed. What’s more, to go further, we want to investigate the limits of delocalized information retrieval from speckles. As for the applications, speckle-based techniques can be integrated with others imaging modalities, such as MMF and photoacoustic. And speckle-based cryptosystems may be used for other types of sensitive data. Finally, the aim of these research is to apply optical imaging with greater penetration depths and higher resolutions. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(59).JPG" width="100%"/></td>
    <td style="width:60%;"> Finally, I am grateful for the support and guidance from supervisors, collaborators, lab members, and fundings. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(60).JPG" width="100%"/></td>
    <td style="width:60%;"> These are all my research. Thanks for your time and comments. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(61).JPG" width="100%"/></td>
    <td style="width:60%;"> Research outputs - First authored papers. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(62).JPG" width="100%"/></td>
    <td style="width:60%;"> Research outputs - Non-first authored papers. </td>
  </tr>


</table>



