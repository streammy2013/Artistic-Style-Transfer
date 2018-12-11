import torchvision.transforms as transforms
from torch.autograd import Variable
import os
import numpy as np
from PIL import Image
from skimage import io, transform
import scipy.misc
import torch

imsize = 512

loader = transforms.Compose([
             transforms.Resize([imsize, imsize]),
             transforms.ToTensor()
         ])

unloader = transforms.ToPILImage()

def image_loader(image_name):
    image = Image.open(image_name)
    image_tensor = loader(image)
    image_tensor.unsqueeze_(0)
    image_variable = Variable(image_tensor)
    return image_variable
  
def save_image(input, path):
    image = input.data.clone().cpu()
    image = image.view(3, imsize, imsize)
    image = unloader(image)
    scipy.misc.imsave(path, image)

def rgb2luv(image):
    img = image.transpose(2,0,1).reshape(3,-1)
    luv = np.array([[.299, .587, .114],[-.147, -.288, .436],[.615, -.515, -.1]]).dot(img).reshape((3,image.shape[0],image.shape[1]))
    return luv.transpose(1,2,0)

def luv2rgb(image):
    img = image.transpose(2,0,1).reshape(3,-1)
    rgb = np.array([[1, 0, 1.139],[1, -.395, -.580],[1, 2.03, 0]]).dot(img).reshape((3,image.shape[0],image.shape[1]))
    return rgb.transpose(1,2,0)

def gen_path(style_path, content_path, config=None):
    style_name = os.path.basename(style_path)
    style_name = os.path.splitext(style_name)[0]

    content_name = os.path.basename(content_path)
    content_name = os.path.splitext(content_name)[0]

    output_name = "%s_%s"%(style_name, content_name)

    return output_name