import numpy as np
import os
from PIL import Image
from scipy import misc
import scipy.linalg as la
from skimage import transform
import matplotlib.pyplot as plt

imsize = 512
def color_transfer(style, content, mode, output_name, output_path):
    """
    Input: style image path; content image path
    mode can be 'chol' for cholesky or 'pca' for eigenvalue decomposition
    """
    style_img = misc.imread(style, mode="RGB")
    content_img = misc.imread(content, mode='RGB')
    style_img = transform.resize(style_img, (imsize, imsize))
    content_img = transform.resize(content_img, (imsize, imsize))

    mu_s = np.zeros([1,3])
    mu_c = np.zeros([1,3])
    for i in range(3):
        mu_s[0][i] = style_img[:,:, i].mean()
        mu_c[0][i] = content_img[:,:, i].mean()

    sigma_s = cov(style_img, mu_s)
    sigma_c = cov(content_img, mu_c)

    if mode == 'chol':
        L_s = (la.cholesky(sigma_s)).T
        L_c = (la.cholesky(sigma_c)).T

        A = np.dot(L_c, la.inv(L_s))
    elif mode == 'pca':
        V_s, U_s = la.eigh(sigma_s)
        V_c, U_c = la.eigh(sigma_c)
        sigma_sqrt_s = U_s.dot(np.sqrt(np.diag(V_s))).dot(U_s.T)
        sigma_sqrt_c = U_c.dot(np.sqrt(np.diag(V_c))).dot(U_c.T)
        A = np.dot(sigma_sqrt_c, la.inv(sigma_sqrt_s))
    
    b = mu_c.T - np.dot(A, mu_s.T)
    res = lin_transform(style_img, A, b)
    output_name = output_path + '%s_%s.jpg'%(output_name, mode)
    misc.imsave(output_name, res)
    mu_res = np.zeros([1,3])
    for i in range(3):
        mu_res[0][i] = res[:,:, i].mean()
    print (mu_res)
    print (mu_c)
    return output_name

def cov(m, mu):
    sigma = np.zeros([3, 3])
    imsize = m.shape[0]
    for i in range(imsize):
        for j in range(imsize):
            tmp = m[i, j, :] - mu
            sigma += np.dot(tmp.T, tmp)
    sigma /= imsize * imsize
    return sigma

def lin_transform(m, A, b):
    imsize = m.shape[0]
    res = np.zeros([imsize, imsize, 3])
    for i in range(imsize):
        for j in range(imsize):
            res[i, j, :] = np.dot(A, m[i, j, :]) + b.T
    return res

def luminance_only(style, content, output_name, output_path):
    style_img = misc.imread(style, mode="RGB").astype(float)/256
    content_img = misc.imread(content, mode='RGB').astype(float)/256
    style_img = transform.resize(style_img, (imsize, imsize))
    content_img = transform.resize(content_img, (imsize, imsize))
    #print (style_img.shape)
    lum_style = lum_extract(style_img)
    lum_content = lum_extract(content_img)
    mu_s = lum_style.mean(0).mean(0)
    mu_c = lum_content.mean(0).mean(0)
    lum_style -= mu_s
    lum_style += mu_c

    lum_style[lum_style > 1] = 1
    lum_style[lum_style < 0] = 0

    lum_content[lum_content > 1] = 1
    lum_content[lum_content < 0] = 0

    #print (lum_style)
    style_output = output_path + '%s_%s_style.jpg'%(output_name, 'lum')
    misc.imsave(style_output, lum_style)

    content_output = output_path + '%s_%s_content.jpg'%(output_name, 'lum')
    misc.imsave(content_output, lum_content)

    return style_output, content_output


def lum_extract(image):
    img = image.transpose(2,0,1).reshape(3,-1)
    lum = np.array([.299, .587, .114]).dot(img).squeeze()
    img = np.tile(lum[None,:],(3,1)).reshape((3,image.shape[0],image.shape[1]))
    return img.transpose(1,2,0)


color_transfer("styles/vangogh.jpg", "contents/content7.jpg", "pca", "test", "")