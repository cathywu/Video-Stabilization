import matplotlib.pyplot as plt
from SimpleCV import VirtualCamera

class Video:
    def __init__(self,path):
        self.capture = VirtualCamera(path,"video")
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
