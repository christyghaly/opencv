# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 22:18:23 2019

@author: mm
"""

#!/usr/bin/env python
# coding: utf-8



import cv2

import numpy as np
import matplotlib.pyplot as plt

from scipy import signal
from PIL import Image, ImageDraw
from collections import defaultdict





def non_max_suppression(img1, phs):
    M=img1.shape[0]
    N=img1.shape[1]
   # M, N = img1.shape

    print(img1)
    print(phs)
    for x in range(0, N ):
        for y in range(0, M ):
            mag = img1[y,x]
            if ((phs[y,x] == 0 or phs[y,x] == 4) and (img1[y, x-1] > mag or img1[y, x+1] > mag)
                    or (phs[y,x] == 1 and (img1[y - 1, x - 1] > mag or img1[y + 1, x + 1] > mag))
                    or (phs[y,x] == 2 and (img1[y-1, x] > mag or img1[y+1, x] > mag))
                    or (phs[y,x] == 3 and (img1[y - 1, x +1] > mag or img1[y + 1, x - 1] > mag))):
                img1[y, x] = 0

    imgnew=np.rint(img1).astype(int)
    print(imgnew)
        
    return imgnew




def edgeTracking4(img2,TL,TH):
    gnh = np.zeros((img2.shape[0], img2.shape[1]))
    gnl = np.zeros((img2.shape[0], img2.shape[1]))
    for x in range(img2.shape[1]):
        for y in range(img2.shape[0]):
            if img2[y][x]>=TH:
                gnh[y][x]=255
            elif img2[y][x]>=TL:
                gnl[y][x]=img2[y][x]

    def traverse(j, i):
        x = [-1, 0, 1, -1, 1, -1, 0, 1]
        y = [-1, -1, -1, 0, 0, 1, 1, 1]
        for k in range(8):
            if gnh[j+y[k]][i+x[k]]==0 and gnl[j+y[k]][i+x[k]]!=0:
                gnh[j+y[k]][i+x[k]]=255
                traverse(j+y[k], i+x[k])
                
    for i in range(1, img2.shape[1]-1):
        for j in range(1, img2.shape[0]-1):
            if gnh[j][i]:
                gnh[j][i]=255
                traverse(j, i)
    gnhnew=np.rint(gnh).astype(int)
    
    return gnhnew
    
    
                



def cannyEdge(image,TL,TH):
    #TL,TH define Tlow and Thigh values for double thresholding
    
    #Get image dimensions
    # y for rows and x for columns 

    
    #change rgb to gray scale
    gray_img = np.dot(image[...,:3], [0.299, 0.587, 0.114])
    
    #first step smoothing by 5x5 gaussian kernel with σ=1.4 
    gkern1d = signal.gaussian(5, 1.4).reshape(5, 1)
    gkern2d = np.outer(gkern1d, gkern1d)
    smoothed_img = signal.convolve2d(gray_img, gkern2d ,'same')
    
    #second step apply gradients by sobel operator
    sobel_window_h = np.array([[ -1 , 0 , 1 ] , [ -2 , 0 , 2 ] , [ -1 , 0 , 1 ]])
    sobel_window_v = sobel_window_h.transpose()
    filtered_h = signal.convolve2d( smoothed_img , sobel_window_h ,'same')
    filtered_v = signal.convolve2d( smoothed_img , sobel_window_v ,'same')
    filtered_img = np.sqrt(filtered_h **2 + filtered_v **2)
    phase = np.arctan2(filtered_h , filtered_v) * (180.0 / np.pi)

    # Assign phase values to nearest [ 0 , 45 , 90 ,  135 ]
    print(filtered_img.size)
    phase = ((45 * np.round(phase / 45.0)) + 180) % 180
    phase2=np.rint(phase).astype(int)

    suppressed_img = non_max_suppression(filtered_img, phase2)
    print(suppressed_img)

    final_img = edgeTracking4(suppressed_img,TL,TH)
  
    
    return final_img
    







