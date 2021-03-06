'''
@author: Aamir Mustafa and Rafal K. Mantiuk
Implementation of the paper:
    Transformation Consistency Regularization- A Semi Supervised Paradigm for Image to Image Translation
    ECCV 2020

'''



from __future__ import print_function
import argparse
import torch
from PIL import Image
from torchvision.transforms import ToTensor

import numpy as np

# Training settings
parser = argparse.ArgumentParser(description='PyTorch Super Res Example')
parser.add_argument('--test_path', type=str, required=True, help='input test images to use')
#parser.add_argument('--input_image', type=str, required=True, help='input image to use')
parser.add_argument('--model', type=str, required=True, help='model file to use')
parser.add_argument('--output_folder', type=str, help='where to save the output image')
parser.add_argument('--cuda', default= True, help='use cuda')
opt = parser.parse_args()

print(opt)

model = torch.load(opt.model)
if opt.cuda:
    model = model.cuda()
    
import os
#test_path= 'dataset/BSD500/images/test'
test_path= opt.test_path
test_images= os.listdir(test_path)

for input_image in test_images:
    
    img = Image.open(test_path+ '/'+ input_image).convert('YCbCr')
    y, cb, cr = img.split()


    img_to_tensor = ToTensor()
    input_ = img_to_tensor(y).view(1, -1, y.size[1], y.size[0])

    if opt.cuda:
#    model = model.cuda()
        input_ = input_.cuda()

    out = model(input_)
    out = out.cpu()
#    print('out.shape', out.shape)
    out_img_y = out[0].detach().numpy()
    out_img_y *= 255.0
    out_img_y = out_img_y.clip(0, 255)
    out_img_y = Image.fromarray(np.uint8(out_img_y[0]), mode='L')

    out_img_cb = cb.resize(out_img_y.size, Image.BICUBIC)
    out_img_cr = cr.resize(out_img_y.size, Image.BICUBIC)
    out_img = Image.merge('YCbCr', [out_img_y, out_img_cb, out_img_cr]).convert('RGB')

#    print(input_image)
    out_img.save(opt.output_folder + '/' + input_image)
    
print('output images saved')
