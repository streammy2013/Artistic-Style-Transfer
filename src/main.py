import argparse
from os.path import basename, splitext
import torch.utils.data
import torchvision.datasets as datasets
from skimage import transform
from scipy import misc

from StyleCNN import *
from utils import *
from preprocess import *

parser = argparse.ArgumentParser()
parser.add_argument('--style_img', default='styles/matisse.jpg', help="The name of original style image.", type=str)
parser.add_argument('--content_img', default='contents/content1.jpg', help="The name of original content image.", type=str)
parser.add_argument('--color_preserve', default=False, help='Whether to preserve color', type=bool)
parser.add_argument('--preserve_mode', default='chol', help="The method to preserve color. It can be chosen from chol, pca, and lum", type=str)
parser.parse_args()
args = parser.parse_args()

# CUDA Configurations
dtype = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor

num_epochs = 50
imsize = 512
def main():
    output_name = gen_path(args.style_img, args.content_img)
    output_path = "outputs/"
    if args.color_preserve:
        if args.preserve_mode == 'lum':
            lum_style, lum_content = luminance_only(args.style_img, args.content_img, output_name, output_path)
            content = image_loader(lum_content).type(dtype)
            style = image_loader(lum_style).type(dtype)
        else:
            color_transfer_style = color_transfer(args.style_img, args.content_img, args.preserve_mode, output_name, output_path)
            style = image_loader(color_transfer_style).type(dtype)
            content = image_loader(args.content_img).type(dtype)
    else:
        style = image_loader(args.style_img).type(dtype)
        content = image_loader(args.content_img).type(dtype)

    if args.color_preserve and args.preserve_mode=='lum':
        pastiche = image_loader(lum_content).type(dtype)
        data = lum_extract(np.random.randn(imsize, imsize, 3)).transpose(2,0,1)
        tensor = torch.from_numpy(data).type(dtype)
        tensor.unsqueeze_(0)
        pastiche.data = tensor
    else:
        pastiche = image_loader(args.content_img).type(dtype)
        pastiche.data = torch.randn(pastiche.data.size()).type(dtype)
    
    style_cnn = StyleCNN(style, content, pastiche)
    
    L = []
    for i in range(num_epochs):
        pastiche, loss = style_cnn.train()
        L.append(loss.item())

        if i % 10 == 0:
            print("Iteration: %d" % (i))
            path = "%s_%d.jpg" % (output_name, i)
            if args.color_preserve:
                path = "%s_"%args.preserve_mode + path
            path = output_path + path
            pastiche.data.clamp_(0, 1)
            save_image(pastiche, path)
    plt.figure()
    plt.plot(range(num_epochs), L)
    plt.ylabel("Iteration")
    plt.savefig("loss.jpg")
    path = output_path + output_name
    if args.color_preserve:
        path += "_%s"%args.preserve_mode
    path += "_transfer_%depochs.jpg"%num_epochs
    pastiche.data.clamp_(0, 1)
    save_image(pastiche, path)

    if args.color_preserve and args.preserve_mode=='lum':
        original_content = misc.imread(args.content_img, mode="RGB").astype(float)/256
        transfer_output = misc.imread(path, mode="RGB").astype(float)/256
        original_content = transform.resize(original_content, (imsize, imsize))
        original_content = rgb2luv(original_content)
        original_content[:,:,0] = transfer_output.mean(2)
        output = luv2rgb(original_content)
        output[output<0] = 0
        output[output>1]=1   
        misc.imsave("%s/%s_lum_final.jpg"%(output_path, output_name), output)	     
    else:
        output = pastiche
        path = output_path + output_name
        if args.color_preserve:
            path += "_%s"%args.preserve_mode
        path += "_final.jpg"
        save_image(output, path) 	


main()