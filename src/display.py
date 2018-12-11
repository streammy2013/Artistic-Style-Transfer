from scipy import misc
display = misc.imread("lum_transfer.jpg", mode="RGB").astype(float)/256
tmp = display
print (display.mean(2).shape)
tmp[:,:,0] = display.mean(2)
tmp[:,:,1] = display.mean(2)
tmp[:,:,2] = display.mean(2)
misc.imsave("lum_output.jpg", tmp)