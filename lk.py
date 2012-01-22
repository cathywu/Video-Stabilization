import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as si
from PIL import Image
import deriv
import numpy.linalg as lin

def lk(im1, im2, window_size) :
    u = np.zeros(im1.shape)
    v = np.zeros(im2.shape)

    fx, fy, ft = deriv.deriv(im1, im2)
    halfWindow = np.floor(window_size/2)
    for i in range(int(halfWindow+1),int(fx.shape[0]-halfWindow)):
        for j in range(int(halfWindow+1),int(fx.shape[1]-halfWindow)):
            curFx = fx[i-halfWindow-1:i+halfWindow, 
                       j-halfWindow-1:j+halfWindow]
            curFy = fy[i-halfWindow-1:i+halfWindow, 
                       j-halfWindow-1:j+halfWindow]
            curFt = ft[i-halfWindow-1:i+halfWindow, 
                       j-halfWindow-1:j+halfWindow]
        
            curFx = curFx.flatten() 
            curFy = curFy.flatten() 
            curFt = -curFt.flatten() 
            
            A = np.vstack((curFx, curFy)).T
            U = np.dot(np.dot(lin.pinv(np.dot(A.T,A)),A.T),curFt)
            u[i,j] = U[0]
            v[i,j] = U[1]
    return (u,v)

def lk_point(im1, im2, i, j, window_size) :
    fx, fy, ft = deriv.deriv(im1, im2)
    halfWindow = np.floor(window_size/2)
    curFx = fx[i-halfWindow-1:i+halfWindow, 
               j-halfWindow-1:j+halfWindow]
    curFy = fy[i-halfWindow-1:i+halfWindow, 
               j-halfWindow-1:j+halfWindow]
    curFt = ft[i-halfWindow-1:i+halfWindow, 
               j-halfWindow-1:j+halfWindow]
    #curFx = curFx.T
    #curFy = curFy.T
    #curFt = curFt.T

    curFx = curFx.flatten() 
    curFy = curFy.flatten() 
    curFt = -curFt.flatten() 
    
    A = np.vstack((curFx, curFy)).T
    U = np.dot(np.dot(lin.pinv(np.dot(A.T,A)),A.T),curFt)
    return U[0], U[1]
        
if __name__ == "__main__":      
    x=165
    y=95
    win=50
    im1 = np.asarray(Image.open('flow1-bw-0.png'))
    print im1.shape
    #im2 = np.asarray(Image.open('flow2-bw-0.png'))
    #im2 = np.asarray(Image.open('upright.png'))
    im2 = np.asarray(Image.open('dleft.png'))
    print im2.shape
    u, v = lk(im1, im2, x, y, win)
    print u, v
    plt.imshow(im1, cmap='gray')
    plt.hold(True)
    plt.plot(x,y,'+r');
    plt.plot(x+u*3,y+v*3,'og')
    plt.show()
