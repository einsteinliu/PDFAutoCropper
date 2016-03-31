import datetime
import numpy
import matplotlib.pyplot as plt
from skimage import data
from skimage import io
from skimage import viewer
from skimage import transform
from skimage import color
from skimage import filters
from os import listdir
from os.path import isfile, join

files = [f for f in listdir('poem') if isfile(join('poem', f))]

LONG_EDGE = 1000.0
for file in files:
    print join('poem',file)
    begin = datetime.datetime.now()
    oriImage = io.imread(join('poem',file),as_grey=True)
    len = 500
    if(oriImage.shape[0] > oriImage.shape[1]):
        len = oriImage.shape[0]
    else:
        len = oriImage.shape[1]
    ratio = 1
    image = 1.0 - oriImage
    if(len > LONG_EDGE):
        ratio = LONG_EDGE / len
    if(ratio != 1):
        image = transform.rescale(image,ratio)
    
    rohThetas = range(85,95)
    projs = transform.radon(image, theta=rohThetas, circle=False)
    projs = filters.sobel_h(projs)
    projs = projs.transpose()
    plt.ion()
    
    centerAngle = 0;
    max = 0
    for i in range(0, projs.shape[0]):
        proj = projs[i]
        currMax = numpy.max(proj)
        if(currMax>max):
            max = currMax
            centerAngle = float(rohThetas[i])
    print 'Center angle:',centerAngle
    fineThetas = numpy.linspace(centerAngle-0.5,centerAngle+0.5,20)
    projs = transform.radon(image, theta=fineThetas, circle=False)
    projs = filters.sobel_h(projs)
    projs = projs.transpose()
    bestAngle = 0;
    max = 0
    for i in range(0, projs.shape[0]):
        proj = projs[i]
        currMax = numpy.max(proj)
        if(currMax>max):
            max = currMax
            bestAngle = float(fineThetas[i])
    print 'Best angle:',bestAngle
    end = datetime.datetime.now()
    cost = 1000*(end-begin).total_seconds()
    print (cost)
    print ''