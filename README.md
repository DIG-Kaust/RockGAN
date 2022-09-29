![LOGO](https://github.com/DIG-Kaust/RockGAN/blob/main/logo.png)  

Reproducible material for **A Wasserstein GAN with gradient penalty for 3D porous media generation. \
Corrales M.,  Izzatullah M., Hoteit H., and Ravasi M.** \
submitted to Second EAGE Subsurface Intelligence Workshop, 28-31 October 2022, Manama, Bahrain


## Project structure
This repository is organized as follows:

* :open_file_folder: **checkpoints**: folder containing the trained generator every two epochs for RockGAN and CRockGAN.
* :open_file_folder: **data**: folder containing data and instructions on how to retrieve the data.
* :open_file_folder: **figures**: folder containing the 3D figures of the results obtained.
* :open_file_folder: **notebooks**: set of jupyter notebooks reproducing the experiments in the paper (REV, Training for RockGAN and CRockGAN, and metrics by epochs).
* :open_file_folder: **rockgan**: package of the project.

## Notebooks
The following notebooks are provided:

- :orange_book: ``01_Representative_Elementary_Volume_REV.ipynb``: notebook performing Representative Elementary Volume for porosity and permeability to determine sub-volume size for data augmentation.
- :orange_book: ``02_Training_RockGAN.ipynb``: notebook performing Training of RockGAN.
- :orange_book: ``03_Training_CRockGAN.ipynb``: notebook performing Training of CRockGAN.
- :orange_book: ``04_Results_Minkowski_by_epochs.ipynb``: notebook performing comparison results of the Minkowski functionales by epochs (RockGAN VS CRockGAN).
- :orange_book: ``05_Results_TwoPointStat_by_epochs.ipynb``: notebook performing comparison results of the Two-point statistics by epochs (RockGAN VS CRockGAN).
- :orange_book: ``06_Results_Permeability_by_epochs.ipynb``: notebook performing comparison results of permeability by epochs (RockGAN VS CRockGAN).
- :orange_book: ``07_Results_3D_Visualization.ipynb``: notebook performing 3D visualization of the samples after training.


## Getting started :space_invader: :robot:
To ensure reproducibility of the results, we suggest using the `environment.yml` file when creating an environment.

Simply run:
```
./install_env.sh
```
It will take some time, if at the end you see the word `Done!` on your terminal you are ready to go. After that you can simply install your package:
```
pip install .
```
or in developer mode:
```
pip install -e .
```

Remember to always activate the environment by typing:
```
conda activate rockgan
```

**Disclaimer:** All experiments have been carried on a Intel(R) Xeon(R) CPU @ 2.10GHz equipped with a single NVIDIA GEForce RTX 3090 GPU. Different environment 
configurations may be required for different combinations of workstation and GPU.


**This notebook uses:**
Gostick J, Khan ZA, Tranter TG, Kok MDR, Agnaou M, Sadeghi MA, Jervis R. PoreSpy: A Python Toolkit for Quantitative Analysis of Porous Media Images. Journal of Open Source Software, 2019. doi:10.21105/joss.01296

