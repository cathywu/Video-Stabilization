#!/usr/bin/python

#import utilities as util
import matplotlib.pyplot as plt
from SimpleCV import Image
import SimpleCV as scv
from SimpleCV import cv
import lk
import numpy as np
import time

#DATA_PATH = "/home/cathywu/Dropbox/UROP/wearable/data/exp001/compressed/iphone4s-1920r_30f_all_auto.avi"
DATA_PATH = "/home/cathywu/Dropbox/UROP/wearable/data/exp001/compressed/firefly_fw_640r_60f_320s.avi"

lk_params = dict( winSize  = (10, 10), 
                  maxLevel = 3, 
                  criteria = (cv.CV_TERMCRIT_EPS | cv.CV_TERMCRIT_ITER, 20, 0.03),
                  derivLambda = 0.0 )    
class Video:
    def __init__(self,path):
        self.capture = scv.VirtualCamera(path,"video")
        self.im = None
    def step(self,stepsize=1,scale=0.50):
        for i in range(stepsize-1):
            self.capture.getImage()
        self.im = self.capture.getImage().copy().scale(scale)
        return self.get_image()
    def show(self):
        plt.figure()
        plt.show()
        plt.imshow(self.im,cmap="gray")
    def get_image(self):
        return self.im
    def save(self):
        pass

class Flow:
    def __init__(self,im1,im2,win=10):
        self.im1 = im1
        self.im2 = im2
        self.win = win
        print time.time(),
        (self.u, self.v) = self.compute_flow()
        print time.time()
        (self.vert, self.hor) = self.estimate_camera_motion()
    def compute_flow(self):
        # lucas kanade
        #[http://ascratchpad.blogspot.com/2011/10/optical-flow-lucas-kanade-in-python.html]
        # FIXME quite slow to compute, ~3 sec per frame
        return lk.lk(self.im1,self.im2,self.win)
        return (u,v)
    def estimate_camera_motion(self):
        return np.average(self.u)*120*160/108/148,np.average(self.v)*120*160/108/148
    def adjust(self,x=0,y=0):
        #TODO remove this mess of hardcode case handling
        temp = self.im2.copy()
        if int(x) == 0:
            if y >= 0:
                temp[:,int(y):] = self.im2[:,:-int(y)]
            else:
                temp[:,:-int(y)] = self.im2[:,int(y):]
        elif int(y) == 0:
            if x >= 0:
                temp[int(x):,:] = self.im2[:-int(x),:]
            else:
                temp[:-int(x),:] = self.im2[int(x):,:]
        elif x >= 0 and y >= 0:
            temp[int(x):,int(y):] = self.im2[:-int(x),:-int(y)]
        elif x < 0 and y < 0:
            temp[:int(x),:int(y)] = self.im2[-int(x):,-int(y):]
        elif x >= 0 and y < 0:
            temp[int(x):,:int(y)] = self.im2[:-int(x),-int(y):]
        elif x < 0 and y >= 0:
            temp[:int(x),int(y):] = self.im2[-int(x):,:-int(y)]
        else:
            print "Error: unhandled case (%s,%s)" % (x,y)
        return temp 
    def show_im1(self):
        plt.imshow(self.im1,cmap='gray')
    def show_im2(self):
        plt.imshow(self.im2,cmap='gray')
    def show_adjust(self,x=0,y=0):
        plt.imshow(self.adjust(x,y),cmap='gray')

def next_flow():
    plt.clf()
    win=10
    im1 = np.asarray(vid.step(30).getGrayscaleMatrix())
    im2 = np.asarray(vid.step(6).getGrayscaleMatrix())
    f = Flow(im1,im2)
    print 'im1'
    f.show_im1()
    plt.show()
    raw_input()
    print 'im2'
    f.show_im2()
    raw_input()
    plt.show()
    print "Estimate of camera motion -- x: %s y: %s" % (f.hor,f.vert)
    print 'im adjusted'
    f.show_adjust(f.hor,f.vert)
    return f

def plot_flow():
    im1 = vid.step()
    hor = []
    vert = []
    for i in range(200):
        im2 = vid.step()
        f = Flow(im1,im2)
        print (f.hor,f.vert)
        hor.append(f.hor)
        vert.append(f.vert)
        im1 = im2.copy()
    return (hor,vert)

if __name__ == "__main__":
    vid = Video(DATA_PATH)
    #(hor,vert) = plot_flow()
    #plt.figure()
    #plt.plot(hor)
    #plt.hold()
    #plt.plot(vert)
    #plt.show()
    vid.step(stepsize=172)
    f = next_flow()

