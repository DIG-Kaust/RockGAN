import torch
import numpy as np
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.nn.utils   import spectral_norm 
from torchsummary import summary


        
class Generator(torch.nn.Module):
    def __init__(self, in_channel=1, out_channel=1):
        
        super(Generator, self).__init__()
        # channel_in = 16
        # H = 16
        # W = 16
        self.conv_net = torch.nn.Sequential(
            
            # dim: Bx16x16x16
            torch.nn.ConvTranspose3d(in_channels=in_channel, out_channels=2, kernel_size=4, stride=2, padding=1),
            torch.nn.GELU(),
            
            # dim: Bx32x32x32
            torch.nn.ConvTranspose3d(in_channels=2, out_channels=4, kernel_size=4, stride=2, padding=1),
            torch.nn.GELU(),
            
            # dim: Bx64x64x64
            torch.nn.ConvTranspose3d(in_channels=4, out_channels=8, kernel_size=4, stride=2, padding=1),
            torch.nn.GELU(),
            
            # dim: Bx128x128x128
            torch.nn.ConvTranspose3d(in_channels=8, out_channels=out_channel, kernel_size=3, stride=1, padding=1),
            torch.nn.Sigmoid()
        )
        
    def forward(self, z):
        # z dim: Bx16x16x16
        return self.conv_net(z)
    
    
class Discriminator(torch.nn.Module):
    def __init__(self, in_channel=1, out_channel=1):
        
        super(Discriminator, self).__init__()
        # channel_in = 128
        # H = 128
        # W = 128
        self.conv_net = torch.nn.Sequential(

            # dim: Bx64x64x64
            torch.nn.Conv3d(in_channels=in_channel, out_channels=32, kernel_size=4, stride=2, padding=1),
            torch.nn.InstanceNorm3d(32),
            torch.nn.LeakyReLU(0.2),
            
            # dim: Bx32x32x32
            torch.nn.Conv3d(in_channels=32, out_channels=16, kernel_size=4, stride=2, padding=1),
            torch.nn.InstanceNorm3d(16),
            torch.nn.LeakyReLU(0.2),
            
            # dim: Bx16x16x16
            torch.nn.Conv3d(in_channels=16, out_channels=8, kernel_size=4, stride=2, padding=1),
            torch.nn.InstanceNorm3d(8),
            torch.nn.LeakyReLU(0.2),
            
            # dim: Bx8x8x8
            torch.nn.Conv3d(in_channels=8, out_channels=4, kernel_size=4, stride=2, padding=1),
            torch.nn.InstanceNorm3d(4),
            torch.nn.LeakyReLU(0.2),
            
            # dim: Bx4x4x4
            torch.nn.Conv3d(in_channels=4, out_channels=2, kernel_size=4, stride=2, padding=1),
            torch.nn.InstanceNorm3d(2),
            torch.nn.LeakyReLU(0.2),
            
            # dim: Bx1x1x1
            torch.nn.Conv3d(in_channels=2, out_channels=out_channel, kernel_size=4, stride=2, padding=1),
        )
        
    def forward(self, z):
        # z dim: Bx128x128x128
        return self.conv_net(z)


def gradient_penalty(critic, real, fake, device="cpu"):
    """
    Gradient penalty for WGAN-GP
    Parameters
    ----------
    critic : :obj:`torch.nn.Module`
        Critic model of WGAN
    real : :obj:`torch.Tensor`
        Tensor of real data of size BxCxWxH
    fake : :obj:`torch.Tensor`
        Tensor of fake data of size BxCxWxH
    device : :obj:`str`
        Device to run the computation cpu or cuda
    Returns
    -------
    : :obj:`torch.Tensor`
        Scalar value of gradient penalty
    """

    BATCH_SIZE, C, H, W, D = real.shape
    beta = torch.rand((BATCH_SIZE, 1, 1, 1, 1)).repeat(1, C, H, W, D).to(device)
    interpolated_images = real * beta + fake.detach() * (1 - beta)
    interpolated_images.requires_grad_(True)

    # Calculate critic scores
    mixed_scores = critic(interpolated_images)

    # Take the gradient of the scores with respect to the images
    gradient = torch.autograd.grad(
        inputs=interpolated_images,
        outputs=mixed_scores,
        grad_outputs=torch.ones_like(mixed_scores),
        create_graph=True,
        retain_graph=True,
    )[0]
    gradient = gradient.view(gradient.shape[0], -1)
    gradient_norm = gradient.norm(2, dim=1)

    return torch.mean((gradient_norm - 1) ** 2)
