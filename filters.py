#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 19:05:18 2019

@author: zuha
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
from scipy import signal
import numpy as np
from PIL.ImageQt import ImageQt
from scipy import misc
from PyQt5 import QtGui
class ComputerVisionToolBox(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super(ComputerVisionToolBox, self).__init__()
        self.setupUi(self)
        
        self.pushButton_filters_load.clicked.connect(lambda: self.openFile(self.pushButton_filters_load))
        

     
    def openFile(self,b):
         if b.text() == 'Load Image': 
             filename = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'), 'Image files (*.jpg *.png)')
             print(filename)
             pic = PyQt5.QtGui.QPixmap(filename[0])
             self.img= cv2.imread(filename[0])
             self.label_filters_input.setPixmap(pic)
             self.label_filters_input.setScaledContents(True)
             self.label_2.setText("{} x {}".format(pic.width(), pic.height()))
             self.label.setText("{}".format(filename[0]))
       
             
             qimage = QtGui.QImage(self.img, self.img.shape[1] ,self.img.shape[0], self.img.strides[0], QtGui.QImage.Format_RGB888)
    
             q = QtGui.QPixmap.fromImage(qimage)
             self.label_filters_output.setPixmap(q)
             self.label_filters_output.setScaledContents(True)

           
         type = str(self.comboBox.currentText())
         
         
         if type =="Prewitt":
            print("well")
            
         if type =="Sobel":
            print("hello")
            
         if type =="Laplacian":
            print("hello")
            
         if type =="DOG":
            print("hello")
            
         if type =="Box":
             img= self.box_filter(self.img,8)
             qimage = QtGui.QImage(img, img.shape[0], img.shape[1], QtGui.QImage.Format_Grayscale8)
             q = QtGui.QPixmap.fromImage(qimage)
             self.label_filters_input.setPixmap(q)

            
         if type =="Gaussian":
            print("hello")
            


             
             
    def applyFilter(self, filterType, image):
        pass
    
    def box_filter(self, img, w):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kern= np.ones((w,w)) / (w*w)
        smooth = signal.convolve2d(gray, kern, boundary='symm', mode='same')
        return smooth

#    def avgFilter(self,img):
#        filteredImg =img.copy()
#        for i in range(3):
#            avg_kernel = np.ones([3,3])/9
#            filteredImg[:,:,i] = signal.convolve2d(img[:,:,i], avg_kernel, 'same') 
#        return filteredImg
#    
    
#    def gaussian(self, img, kernlen , std):    
#        gkern1d = signal.gaussian(kernlen, std=std).reshape(kernlen, 1)
#        gkern2d = np.outer(gkern1d, gkern1d)
#        smooth_img = signal.convolve2d(gray, g, boundary='symm', mode='same')
#        return gkern2d
    
               

def main():
    App = QtWidgets.QApplication(sys.argv)
    form = ComputerVisionToolBox()
    form.show()
    App.exec_()


if __name__ == '__main__':
    main()
