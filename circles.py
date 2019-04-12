# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 14:12:53 2019

@author: mm
"""

import gui
from PyQt5 import QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QFileDialog
import os
import PyQt5.QtGui, PyQt5.QtCore
import cv2
import numpy as np
from PIL.ImageQt import ImageQt
from scipy import misc
from PyQt5 import QtGui
from PIL import Image ,  ImageDraw
import matplotlib.pyplot as plt
from math import sqrt,sin,cos,pi
from collections import defaultdict
from cannyed import cannyEdge
from mpl_toolkits.mplot3d import Axes3D

class ComputerVisionToolBox(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super(ComputerVisionToolBox, self).__init__()
        self.setupUi(self)
        
        self.pushButton_circles_load.clicked.connect(lambda: self.openFilec(self.pushButton_circles_load))
    def openFilec(self,bc):
        if bc.text() == 'Load Image':
            filename = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'), 'Image files (*.jpg *.png)')
            self.image=Image.open(filename[0])
            cv_image=np.asarray(self.image)
            pic = PyQt5.QtGui.QPixmap(filename[0])
            self.label_circles_input.setPixmap(pic)
            self.label_circles_input.setScaledContents(True)
            self.label_7.setText("{} x {}".format(pic.width(), pic.height()))
            self.label_6.setText("{}".format(filename[0]))
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            x4d=[]
            y4d=[]
            r4d=[]
            v4d=[]
            slicecanny=cannyEdge(cv_image,940,1200)
           
            xmax=slicecanny.shape[1]
            
            ymax=slicecanny.shape[0]
            rmin=18

            rmax=20
            points=[]
            acc=defaultdict(int)
            output_image = Image.new("RGB", self.image.size)
            output_image.paste(self.image)
            draw_result = ImageDraw.Draw(output_image)
            for r in range(rmin,rmax+1):
                for t in range(180):
                    points.append((r,int(r*cos(2*pi*t/180)),int(r*sin(2*pi*t/180))))
            for x in range (slicecanny.shape[1]):
                for y in range(slicecanny.shape[0]):
                    if(slicecanny.item(y,x) !=0):
                        for r,dx,dy in points:
                            xo=x-dx
                            yo=y-dy
                            if(xo>=0 and xo<=xmax and yo>=0 and yo<=ymax):
                                acc[(xo,yo,r)]+=1
                                
            circles=[]                
            for k,v in sorted(acc.items()):
                x, y, r = k
                if(v/100 >=0.85 and all((x - xc) ** 2 + (y - yc) ** 2 > r ** 2 for xc, yc,rc in circles)  ):
                    circles.append((x,y,r))
                    print(v , x, y, r)
                    
            for x, y, r in circles:
                draw_result.ellipse((x-r, y-r, x+r, y+r), outline=(255,0,0,2))
            for k,vt in sorted(acc.items()):
                xo, yo, r = k
                x4d.append(xo)
                y4d.append(yo)
                r4d.append(r)
                v4d.append(vt)
                
            img = ax.scatter(x4d, y4d, r4d, c=v4d, cmap=plt.hot())
            fig.colorbar(img)
            ax.set_xlabel('xo Label')
            ax.set_ylabel('yo Label')
            ax.set_zlabel(' radius')
            plt.savefig("plot3d.png")
            plt.show()
            
            output_image.save("result.png")
            pic2 = PyQt5.QtGui.QPixmap("result.png")
            self.label_circles_output.setPixmap(pic2)
            self.label_circles_output.setScaledContents(True)
            pic3 = PyQt5.QtGui.QPixmap("plot3d.png")
            self.label_circles_hough.setPixmap(pic3)
            self.label_circles_hough.setScaledContents(True)



def main():
    App = QtWidgets.QApplication(sys.argv)
    form = ComputerVisionToolBox()
    form.show()
    App.exec_()


if __name__ == '__main__':
    main()
         