from numpy import *
from imutils import *
from matplotlib import pyplot as plt
import sys
import os
import shutil
import cv2
import math

import glob

FOLDER_IMGS = "MIAS/"
IMG_INFO = "info.txt"
FOLDER_CROPPED = 'CROPPED/'
FOLDER_MARKED = 'MARKED/'

def getFilesFromFolder (folder):
    fileNames = os.listdir(folder)
    return fileNames

def readFile (filename):
    file = open(filename, 'r')
    lines = file.readlines()
    return lines

def getLineInfo (lines):
    linesOut = []
    for line in lines:
        line = line.split(" ")
        if (len(line) == 7 ):
            linesOut.append(line)
    return linesOut

def getDistinctClass(lines):
    output = set()
    for line in lines:
        output.add(line[2])
    return output

def makedir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def makeFolders(folder, labels):
    for label in labels:
        makedir(folder+label)

def markRegion(line):
    imgPath =  FOLDER_IMGS + line[0] + ".pgm"
    label = line[2]
    x = int(line[4])
    y = int(line[5])
    radius = int(line[6])

    img = cv2.imread(imgPath,0)
    imgCopy = img.copy()

    cv2.circle(imgCopy,(x,y), radius, (0,0,255))
    cv2.imwrite(FOLDER_MARKED + label + '\\' + line[0] +'.png', imgCopy)



def crop(line):
    imgPath =  FOLDER_IMGS + line[0] + ".pgm"
    label = line[2]
    x = int(line[4])
    y = int(line[5])
    radius = int(line[6])

    img = cv2.imread(imgPath,0)
    imgCopy = img.copy()

    regions = [(x+1 - radius, y - radius, 2*radius, 2*radius), (x - radius, y+1 - radius, 2*radius, 2*radius), (x-1 - radius, y - radius, 2*radius, 2*radius), (x - radius,y-1 - radius, 2*radius, 2*radius), (x-1 - radius, y-1 - radius, 2*radius, 2*radius), (x+1 - radius, y+1 - radius, 2*radius, 2*radius)]

    indice = 0
    for region in regions:
        nameOfFile = FOLDER_CROPPED + label + '\\' + line[0] + "_" + str(indice) +  "_" + ".png";
        crop_img = imgCopy[region[1]: region[1] + region[3], region[0]: region[0] + region[2]]
        outImg = cv2.resize(crop_img, (40, 40))
        outImg = cv2.equalizeHist(outImg)
        cv2.imwrite(nameOfFile, outImg)
        indice += 1

def compareValue(center, value):
	return (value >= center)

def getLbpMat(img, p, r):
    imgCopy = img.copy()
    w, h = imgCopy.shape[::-1]
    size = w, h
    imgCopy  = zeros(size, imgCopy.dtype)

    for i in arange(1, w - r):
        for j in arange(1, j - r):
            centerValue = img[i][j]
            for pValue in range(p):
                imgCopy[i,j] += int(compareValue(img[i-1, j], centerValue * pow(2.0, pValue)))

    return imgCopy

def getLbpHist(img, nBins, p):
    w, h = img.shape[::-1]
    vHist = [0]*256
    dNBins = (pow(2.0, p)) / nBins

    for i in range(w):
        for j in range(h):
            pixel = img[i][j]
            indice =  (pixel / dNBins)
            vHist[indice] = vHist[indice] + 1;


    return vHist

def saveLBPFeatures (img, p, r, label):
    imgCopy = img.copy()

    listLBPHist = []
    for p in arange(4, 8, 2*i):
        for r in arange(1, 2):
            matLBP = getLbpMat(imgCopy,p,r)
            nBins = (pow(2.0, p))/2
            histLBP = getLbpHist(imgCopy, nBins, p)
            listLBPHist.append(histLBP)



def cropRegion(line):
    imgPath =  FOLDER_IMGS + line[0] + ".pgm"
    label = line[2]
    x = int(line[4])
    y = int(line[5])
    radius = int(line[6])

    img = cv2.imread(imgPath,0)
    imgCopy = img.copy()

    w, h = imgCopy.shape[::-1]

    for i in arange(0, w - 2*radius, i + 2*radius):
        for j in arange(0, h - 2*radius, j + 2*radius):
            dist = sqrt(pow(x - j, 2.0) + pow(y - i, 2.0))

            if (dist > radius):
                square = (j, i, 2*radius, 2*radius)
                outImg = imgCopy[j: j+ 2*raius, i: i + 2*radius]

                outImg = cv2.resize(outImg, (40, 40))
                outImg = cv2.equalizeHist(outImg)
                cv2.imwrite(FOLDER_CROPPED+label + '\\' + line[0] +'.png', outImg)
