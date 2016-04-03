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

    return bestAngle

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