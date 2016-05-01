import numpy
from skimage import data
from skimage import io
from skimage import transform
from skimage import color
from skimage import filters
import matplotlib.pyplot as plt

def computeProjMax(image,angle):
    max = 0
    rotImage = transform.rotate(image,angle)
    proj = rotImage.sum(axis=0)
    #print 'projection length:',proj.shape[0]
    lProj = proj[0:proj.shape[0]-1]
    rProj = proj[1:proj.shape[0]]
    diffProj = abs(rProj - lProj)
    #print 'curr angle:',angle
    #print 'curr max:',numpy.max(diffProj)
    #plt.plot(diffProj)
    #plt.show()
    return numpy.max(diffProj)

def computeBestAngle(image, angles):
    bestAngle = 0
    max = 0;
    for angle in angles:
        currMax = computeProjMax(image,angle)
        if(currMax>max):
            max = currMax
            bestAngle = angle
    if(0==max):
        bestAngle = 90
    return bestAngle


def averageFilter(proj,num):
    for i in range(0,proj.shape[0]-num):
        proj[i] = sum(proj[i:i+num])/num
    return proj

def getCenterPartB(proj):
    max = numpy.max(proj)
    threshold = 0.05*max
    upperBound = 0
    lowerBound = 0
    for u in range(0,proj.shape[0]):
        if(proj[u]>threshold):
            upperBound = u
            break

    for l in range(0,proj.shape[0]):
         l = proj.shape[0] - 1 - l
         if(proj[l]>threshold):
            lowerBound = l
            break

    upperBound = (int)(upperBound - 0.02*proj.shape[0])
    if(upperBound<0):
           upperBound = 0
    
    lowerBound = (int)(lowerBound + 0.02*proj.shape[0])
    if(lowerBound>proj.shape[0]):
        lowerBound = proj.shape[0]-1
    
    return [upperBound,lowerBound]

def getTextPart(proj,textCells,index):
    leftBound = 9999
    rightBound = 0
    threshold = 10
    for cell in textCells:
        currLeft = cell[index*2]
        currRight = cell[index*2+1]
        for l in range(0,currLeft):
            curr = currLeft - l
            if((proj[curr]>threshold) and (curr<leftBound)):
                leftBound = curr
        for curr in range(currRight,proj.shape[0]):
            if((proj[curr]>threshold) and (curr>rightBound)):
                rightBound = curr
    if(leftBound == 9999):
        leftBound = 0
    if(rightBound == 0):
        rightBound = proj.shape[0]-1
    if(leftBound>10):
        leftBound = leftBound - 10
    if(rightBound<(proj.shape[0]-10)):
        rightBound = rightBound + 10
    return [leftBound,rightBound]

def getCenterPart(proj):
    leftBound = 0
    rightBound = 0
    center = (int)(proj.shape[0]/2)
    for r in range(center,proj.shape[0]):
        if(proj[r] == 0):
            rightBound = r
            break

    for l in range(0,center):
        l = center-l
        if(proj[l] == 0):
            leftBound = l
            break

    leftBound = (int)(leftBound - 0.02*proj.shape[0])
    if(leftBound<0):
        leftBound = 0
    
    rightBound = (int)(rightBound + 0.02*proj.shape[0])
    if(rightBound>proj.shape[0]):
        rightBound = proj.shape[0]-1
    
    return [leftBound,rightBound]