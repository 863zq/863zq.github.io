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
    <td style="width:60%;"> As for the final research, the focus is transferred from overcoming speckles to utilizing speckles: Due to their inherent randomness, we propose to use speckles as ciphertexts in cryptosystems. We introduce a plain /pleɪn/ yet highly efficient speckle-based cryptosystem, for encrypted face recognition. A piece of scattering ground glass is utilized as a physical secret key, for superior security, light-speed encryption, and low-cost. Overall, my research journey is from overcoming speckles, understanding speckles, to utilizing speckles. We believe these studies will significantly advance the fields of speckle imaging and biomedical optics. Following these outlines, I will delve into the details of these research. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(14).JPG" width="100%"/></td>
    <td style="width:60%;"> The first research is the Parameter-Free Algorithm for iterative Wavefront Shaping. </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(15).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(16).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(17).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(18).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(19).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(20).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(21).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(22).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(23).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(24).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(25).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(26).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(27).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(28).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(29).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>


  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(30).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(31).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(32).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(33).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(34).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(35).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(36).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(37).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(38).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(39).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>


  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(40).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(41).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(42).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(43).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(44).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(45).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(46).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(47).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(48).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(49).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(50).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(51).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(52).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(53).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(54).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(55).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(56).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(57).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(58).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(59).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(60).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(61).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>

  <tr>
    <td style="width:40%;"><img src="/Publication/PhD_thesis/PPT%20(62).JPG" width="100%"/></td>
    <td style="width:60%;"> . </td>
  </tr>


</table>



