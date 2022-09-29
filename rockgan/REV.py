import torch
import openpnm as op
import porespy as ps
import numpy as np

def porosity(img):
    r"""
    Computes the porosity of a sample (image, real or generated).
    Here 0 values correspond to the voids, and 1 values correspond to the grains.
    
    Parameters
    ----------
    img: input array (4D -- #samples, xdim, ydim, zdim) corresponding to the pixels of the image.
    
    
    Returs
    ------
    porosity: float
              Returns the computed porosity, it is equal to the sum of voids (0), over
              the sum of the voids(0) and solids(1)
    """
    voids = torch.sum(torch.round(img)  == 0, dim=(-3,-2, -1))
    solids = torch.sum(torch.round(img)  == 1, dim=(-3,-2, -1))
    phi_computed = voids/(voids + solids)
    
    return phi_computed



def patches_3D(img, ks=128, stride=64):
    r"""
    Generates a number of subtaches of a 3D porous media.
    
    Parameters
    ----------
    img: input array (4D -- #samples, xdim, ydim, zdim) corresponding to the pixels of the image.
    ks: Kernel size of supatch dimension (the same in x,y, and z)
    stride: The separation sampling between the extracted cubes
    
    Returs
    ------
    patches: 4D array containing the subpatches generated (#subpatches, xdim, ydim, zdim)
    """
    kc, kh, kw = ks, ks, ks  # kernel size
    dc, dh, dw = stride, stride, stride  # stride
    patches = img.unfold(1, kc, dc).unfold(2, kh, dh).unfold(3, kw, dw)
    patches = patches.contiguous().view(-1, kc, kh, kw)
    
    return patches


def Permeability_OpenPNM(img, window_size=np.array([64, 128, 256, 400]), resolution= 1, stride=64):
    r"""
    Computes the Permeability using the OpenPNM workflow.
    
    Parameters
    ----------
    img: input 3D array (numpy) containg the 3D sample following the convention of porespy
            0's are grains, and 1's are the solids
    window_size: 1D array of the different subpatches dimension to test.         
    resolution: Voxel dimension of the sample in meters.
    settings: characteristics of the pores and throats. 
    stride: The separation sampling between the extracted cubes to be used in 'patches_3D'
    
    Returs
    ------
    perm_results: list of the permeability results per subpatches in mD
    """
    settings = {'pore_shape': 'pyramid',
                    'throat_shape': 'cuboid',
                    'pore_diameter': 'equivalent_diameter',
                    'throat_diameter': 'inscribed_diameter'}
    
    perm_results = []
    for j in window_size:
        Berea_patches = patches_3D(img, ks=j, stride=stride)
        n_patches = np.arange(0, len(Berea_patches.numpy()[:])-1, 1, dtype=int)
        print('Computing perm for window size:', j)
    
        k_mD = []
        snow = []
        for i in n_patches:
            try:
                #Extracting Network
                sample = Berea_patches[i].numpy()        
                snow = ps.networks.snow2(sample, voxel_size=resolution);   
                pn, geo = op.io.PoreSpy.import_data(snow.network, settings=settings);

                #Network health
                h = pn.check_network_health()
                op.topotools.trim(network=pn, pores=h['trim_pores'])

                #Adding phase
                water = op.phases.Water(network=pn)

                #conductance
                water.add_model(propname='throat.hydraulic_conductance',
                                model=op.models.physics.hydraulic_conductance.classic_hagen_poiseuille)


                #Stokes
                perm = op.algorithms.StokesFlow(network=pn, phase=water)
                perm.set_value_BC(pores=pn.pores('zmax'), values=0)
                perm.set_value_BC(pores=pn.pores('zmin'), values=101325)
                perm.run()
                water.update(perm.results())

                #Permeability
                Q = np.absolute(perm.rate(pores=pn.pores('zmin')))
                A = (sample.shape[0] * sample.shape[1]) * resolution**2
                L = sample.shape[2] * resolution
                mu = water['pore.viscosity'].max()
                delta_P = 101325 - 0

                K = Q * L * mu / (A * delta_P)
                K = K/0.98e-12*1000

                k_mD = np.concatenate((k_mD, K), axis=0)
                #print('--------- Completed perm for window size:', j)

                del snow, pn, geo, water, perm, sample, h, Q, A, L, mu, delta_P, K
            except Exception:
                    continue

        perm_results.append(k_mD)
    print('Done :D')
    return perm_results
