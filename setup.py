import os
from setuptools import setup, find_packages

def src(pth):
    return os.path.join(os.path.dirname(__file__), pth)

# Project description
descr = 'RockGAN'

setup(
    name="rockgan", # Choose your package name
    description=descr,
    long_description=open(src('README.md')).read(),
    keywords=['GAN',
              'deep learning',
              'porous-media'],
    classifiers=[
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Mathematics'
    ],
    author='Miguel Corrales, Muhammad Izzatulah ,Matteo Ravasi',
    author_email='miguel.corrales@kaust.edu.sa, muhammad.izzatulah@kaust.edu.sa, matteo.ravasi@kaust.edu.sa',
    install_requires=['numpy >= 1.22.3',
                      'torch >= 1.12.0',
                      'scipy >= 1.7.3',
                      'tqdm >= 4.64.0',
                      'porespy >= 2.0',
                      'setuptools >= 61.2.0',
                      'openpnm >= 2.8.0',
                      'scikit-image >= 0.19.0',
                      'scikit-learn >= 1.0.1',
                      'quantimpy >= 0.4.6'],
    packages=find_packages(exclude=['pytests']),
    use_scm_version=dict(root='.',
                         relative_to=__file__,
                         write_to=src('rockgan/version.py')),
    setup_requires=['setuptools_scm'],

)
