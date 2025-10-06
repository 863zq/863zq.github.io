## Understanding and manipulation of optical speckles

**Author:**  Zhao Qi

**Advisor:** [Prof. Puxiang Lai](https://www.polyu.edu.hk/bme/people/academic-and-teaching-staff/prof-puxiang-lai/) 

**Date:** 2024-10-19

**[PolyU Lib Link](https://theses.lib.polyu.edu.hk/handle/200/13418)**

**[PDF](https://863zq.github.io/Publication/PhD_thesis/PolyU%20Lib%207839-Zhao%20Qi.pdf)**

**[Viva](https://863zq.github.io/Publication/PhD_Viva.html)**

<!-- <strong>PDF:</strong>
<iframe src="https://863zq.github.io/Publication/PhD_thesis/PolyU%20Lib%207839-Zhao%20Qi.pdf"
        width="100%" height="500px" style="border:none;">
</iframe> -->

**Abstract:** Optical technologies have experienced significant advancements, leading to various scientific and technological applications. However, the endeavor to probe deeper into inhomogeneous media is hindered by the inherent challenge of optical scattering. Notably, at depths exceeding 1 mm beneath the skin, the multiple scattering phenomena transform potential imaging clarity into optical speckles. This thesis addresses the critical need for innovative methods to circumvent optical scattering and elucidate information concealed within optical speckles. It presents a comprehensive exploration of optical speckles, offering novel insights into overcoming, understanding, and utilizing optical speckles. The body of this thesis is methodically divided into five chapters, each contributing to the overarching narrative of advancing biomedical optics.

In Chapter 2, a parameter-free algorithm has been proposed for iterative wavefront shaping to overcome speckles, aiming to focus lasers through scattering media and setting the foundation for subsequent chapters. This innovative approach avoids the time-consuming and experience-dependent parameter tuning process, which is inevitable for existing iterative algorithms. Experimental validation, employing ground glass and multi-mode fibers, substantiates the algorithm’s efficacy. These results showcase its robust capability to achieve laser focusing across various scattering environments.

In Chapter 3, the focusing capabilities of iterative wavefront shaping are extended to image retrieval from speckles. We introduce a Generative Adversarial Network (GAN) to effectively tackle the challenge of spatiotemporal decorrelation in optical speckles, enabling the retrieval of images from speckles that have decorrelated to unknown statuses, rather than neglecting intervals between acquiring the training and test datasets as most other research. The GAN framework, not able for its broad generalizability, is trained to retrieve high-fidelity human face images from decorrelated speckles. The ability has been demonstrated even under conditions where the scattering medium has significantly decorrelated, such as after the optical system has been inactive for extended periods (up to 37 hours in experiments) before being reactivated. The experiments mark a significant stride in broadening the applications of learning-based methodologies in speckle imaging.

Chapter 4 further advances the theoretical understanding of speckles and delves into the information delocalization within optical speckles, employing learning-based models and information entropy for an in-depth analysis. The study also examines the speckle sampling condition for high-fidelity information retrieval from optical speckles, an important but previously unexplored research question. Experimental observations disclose a uniform dispersion of information among fully developed optical speckles, ensuring the integrity of information retrieval is maintained irrespective of the spatial positions of optical speckles. A theoretical framework emerges from a synthesis of physical models and empirical data, postulating that neural networks can be trained to retrieve information with high fidelity from optical speckles, provided the entropy of the speckle autocorrelation exceeds the entropy of the target autocorrelation.

Chapter 5 represents a synthesis of the practical algorithmic advancements and theoretical insights from the previous chapters. Speckle Transformer, a cutting-edge vision transformer-based model, has been designed to harness the delocalized information within optical speckles for target classification. The proposed model directly extracts speckle features for classification, surpassing traditional methods where classification follows information retrieval.

Chapter 6 signifies a departure from the primary focus on speckle imaging to embracing the natural randomness of optical speckles and exploring the utilization of optical speckles in the realm of security. An innovative speckle-based optical cryptosystem has been proposed to achieve a straightforward yet highly effective encryption mechanism. The proposed cryptosystem is distinguished by its robust security, rapid encryption, and cost-efficiency. Within this framework, a piece of ground glass serves as the physical secret key, enabling the encryption of face images through the scattering medium of seemingly chaotic optical speckles at the speed of light. Subsequently, these images are decrypted from the optical speckles using a pre-trained neural network, ensuring that the retrieved face images retain high fidelity and are recognizable by face recognition algorithms. To the best of our knowledge, this is the first demonstration of a speckle-based optical cryptosystem for face recognition.

In summary, these chapters illustrate a comprehensive journey from overcoming the challenges posed by scattering, understanding delocalized information in speckles, to harnessing the properties of optical speckles for diverse applications. Accordingly, this thesis significantly advances our comprehension of delocalized information within optical speckles and charts a new course for speckle-related research and applications. The research and experimental outcomes not only elucidate the underlying principles but also herald the advent of a transformative paradigm in deep tissue optics, which promises to extend penetration depths and augment resolution, thereby broadening the scope and efficacy of optical applications in biomedical research.


