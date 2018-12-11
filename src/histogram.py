import matplotlib.pyplot as plt #importing matplotlib
from scipy import misc
from skimage import transform
imsize = 512
img = misc.imread("contents/content7.jpg", mode='RGB').astype(float)
img = transform.resize(img, (imsize, imsize))
print (img)
plt.figure()
plt.hist(img.ravel(), bins=256, range=(0, 256), fc='k', ec='k') 
plt.savefig("content_hist.jpg")

img = misc.imread("chol.jpg", mode='RGB')
plt.figure()
plt.hist(img.ravel(), bins=256, range=(0, 256), fc='k', ec='k') 
plt.savefig("chol_hist.jpg")

img = misc.imread("chol.jpg", mode='RGB')
plt.figure()
plt.hist(img.ravel(), bins=256, range=(0, 256), fc='k', ec='k') 
plt.savefig("pca_hist.jpg")
