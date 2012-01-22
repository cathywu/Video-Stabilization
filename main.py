#!/usr/bin/python

#import utilities as util
import matplotlib.pyplot as plt
from SimpleCV import Image
import SimpleCV as scv
import lk
import numpy as np

#DATA_PATH = "/home/cathywu/Dropbox/UROP/wearable/data/exp001/compressed/iphone4s-1920r_30f_all_auto.avi"
DATA_PATH = "/home/cathywu/Dropbox/UROP/wearable/data/exp001/compressed/firefly_fw_640r_60f_320s.avi"

class Video:
    def __init__(self,path):
        self.capture = scv.VirtualCamera(path,"video")
        self.im = None
    def step(self,stepsize=1,scale=0.25):
        for i in range(stepsize-1):
            self.capture.getImage()
        self.im = np.asarray(self.capture.getImage().copy().scale(scale).getGrayscaleMatrix())
        return self.get_image()
    def show(self):
        plt.figure()
        plt.show()
        plt.imshow(self.im,cmap="gray")
    def get_image(self):
        return self.im

vid = Video(DATA_PATH)
vid.step(stepsize=31)

# lucas kanade
#[http://ascratchpad.blogspot.com/2011/10/optical-flow-lucas-kanade-in-python.html]
end = None
plt.figure()
plt.show()
while end != "q":
    plt.clf()
    win=10
    im1 = vid.step(30)
    im2 = vid.step(4)
    u,v = lk.lk(im1,im2,win)
    print u,v
    print u.max(),v.max()
    print u.min(),v.min()
    #plt.imshow((u**2+v**2)**0.5)
    plt.imshow(im1,cmap='gray')
    raw_input()
    plt.imshow(im2,cmap='gray')
    raw_input()
    plt.hold(True)
    plt.plot(np.nonzero(v>0.01)[1],np.nonzero(v>0.01)[0],'+b')
    plt.plot(np.nonzero(u>0.01)[1],np.nonzero(u>0.01)[0],'+r')
    plt.show()
    #plt.imshow(im1np, cmap='gray')
    #plt.hold(True)
    #plt.plot(x,y,'+r');
    #plt.plot(x+u*3,y+v*3,'og')
    #plt.show()
    end = raw_input("Continue...")

