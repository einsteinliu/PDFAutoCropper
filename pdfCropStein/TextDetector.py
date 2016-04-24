import sys
import datetime
import numpy
import matplotlib.pyplot as plt
from skimage import data
from skimage import io
from skimage import viewer
from skimage import transform
from skimage import color
from skimage import filters

def checkIsTextBlock(image):
    blackCenter = [0,0]
    whiteCenter = [0,0]
    blackPixels = 0
    whitePixels = 0
    for x in range(0,image.shape[0]):
        for y in range(0,image.shape[1]):
            if (1==image[x,y]):
                whiteCenter = [whiteCenter[0]+x,whiteCenter[1]+y]
                whitePixels = whitePixels + 1;
            else:
                blackCenter = [blackCenter[0]+x,blackCenter[1]+y]
                blackPixels = blackPixels + 1;
    if(0==blackPixels):
        blackCenter = -1
    else:
        blackCenter = [blackCenter[0]/blackPixels,blackCenter[1]/blackPixels]
    if(0==whitePixels):
        whiteCenter = -1
    else:
        whiteCenter = [whiteCenter[0]/whitePixels,whiteCenter[1]/whitePixels]
    print "White center:",whiteCenter
    print "Black center:",blackCenter
    print ""
    return True;

def detectAllTextBlock(image):
    cellSize = 1000
    currCellX = 0
    currCellY = 0
    textCells = []
    plt.ion()
    nextX = 0
    nextY = 0
    while(currCellX<image.shape[0]):
        currCellXEnd = currCellX + cellSize
        nextX = currCellXEnd
        if(currCellXEnd>image.shape[0]):
                currCellXEnd = image.shape[0]-1
        while(currCellY<image.shape[1]):    
            currCellYEnd = currCellY + cellSize
            nextY = currCellYEnd
            if(currCellYEnd>image.shape[1]):
                currCellYEnd = image.shape[1]-1
                nextY = 0
            print currCellX,":",currCellXEnd,"         ",currCellY,":",currCellYEnd
            if(checkIsTextBlock(image[currCellX:currCellXEnd,currCellY:currCellYEnd])):
                plt.imshow(image[currCellX:currCellXEnd,currCellY:currCellYEnd],cmap='Greys_r')
                plt.show();
                plt.waitforbuttonpress()
                plt.close()
                textCells.append([currCellX,currCellXEnd,currCellY,currCellYEnd])
            currCellY = nextY
            if(nextY == 0):
                break
        currCellX = nextX

    return textCells

def getTextBlock(image):
    detectAllTextBlock(image)
    return image


