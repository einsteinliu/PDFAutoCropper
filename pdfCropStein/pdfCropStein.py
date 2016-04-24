#!/usr/bin/python
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
from os import listdir
from os.path import isfile, join
from SteinTimer import SteinTimer
import SteinVision
import PDFConvertor
import TextDetector
import os

if(len(sys.argv) <= 2):
    imageFolder = "lightroom"
    files = [f for f in listdir(imageFolder) if isfile(join(imageFolder, f))]
    file = files[3]
    join(imageFolder,file)
    timer = SteinTimer()
    timer.start()
    oriImage = io.imread(join(imageFolder,file),as_grey=True)
    TextDetector.getTextBlock(transform.rescale(oriImage,0.3))
    timer.stop()
    print "all time cost:",timer.elapsed()
else:
    if("convert" == sys.argv[1]):
        print sys.argv
        if(".pdf" in sys.argv[2]):
            pdfFile = sys.argv[2]
            imageFolder = os.path.splitext(os.path.basename(pdfFile))[0]
            print "convert ",pdfFile," to ",imageFolder
            PDFConvertor.pdfToImages(pdfFile,imageFolder)
        else:
            imageFolder = sys.argv[2]
            pdfFile = imageFolder.replace(' ','') + ".pdf"
            PDFConvertor.imagesToPDF(imageFolder,pdfFile)
    elif(("crop" == sys.argv[1]) or ("split"==sys.argv[1])):
        imageFolder = sys.argv[2]
        startPage = ""
        if(len(sys.argv)==4):
            startPage = sys.argv[3]
        saveFolder = imageFolder + "_cropped"
        if(os.path.exists(saveFolder)):
            print saveFolder,"already exists, please check"
        else:
            os.mkdir(saveFolder)
        files = [f for f in listdir(imageFolder) if isfile(join(imageFolder, f))]
        LONG_EDGE = 1000.0
        
        n = 0
        for file in files:
            print join(imageFolder,file)
            begin = datetime.datetime.now()
            oriImage = io.imread(join(imageFolder,file),as_grey=True)

            if("crop" == sys.argv[1]):
                if(os.path.exists(saveFolder + "\\" + file)):
                                print saveFolder+"\\"+file," already exists.."
                                continue
                ratio = 1
                len = 1000
                if(oriImage.shape[0] > oriImage.shape[1]):
                    len = oriImage.shape[0]
                else:
                    len = oriImage.shape[1]

                if(len > LONG_EDGE):
                    ratio = LONG_EDGE / len
                if(ratio != 1):
                    image = transform.rescale(oriImage,ratio)

                image = 1.0 - image

                #####################################
                begin = datetime.datetime.now()
                rohThetas = range(87,93)
                centerAngle = SteinVision.computeBestAngle(image,rohThetas)
                fineThetas = []
                fineThetas.append(centerAngle)
                for i in range(1,11):
                    fineThetas.append(-0.05 * i + centerAngle)
                for i in range(1,11):
                    fineThetas.append(0.05 * i + centerAngle)
                bestAngle = SteinVision.computeBestAngle(image,fineThetas)
                end = datetime.datetime.now()
                cost = 1000 * (end - begin).total_seconds()
                print 'new proj method time:',cost
                print 'best angle:', bestAngle
                #####################################

                #rohThetas = range(87,93)
                #projs = transform.radon(image, theta=rohThetas, circle=False)
                #projs = projs.transpose()
                #lProjs = projs[0:6,0:projs.shape[1] - 1]
                #rProjs = projs[0:6,1:projs.shape[1]]
                #projs = rProjs - lProjs

                #centerAngle = 0
                #max = 0
                #for i in range(0, projs.shape[0]):
                #    proj = projs[i]
                #    #plt.plot(proj)
                #    #plt.show()
                #    #plt.waitforbuttonpress()
                #    #plt.close()
                #    currMax = numpy.max(proj)
                #    print currMax
                #    if(currMax > max):
                #        max = currMax
                #        centerAngle = float(rohThetas[i])

                #print 'Center angle:',centerAngle
                
                #fineThetas = []
                #fineThetas.append(centerAngle)
                #for i in range(1,11):
                #    fineThetas.append(-0.05 * i + centerAngle)
                #for i in range(1,11):
                #    fineThetas.append(0.05 * i + centerAngle)
                ##########################
                ##projs = transform.radon(image, theta=fineThetas, circle=False)
                ##projs = projs.transpose()
                ##lProjs = projs[0:22,0:projs.shape[1] - 1]
                ##rProjs = projs[0:22,1:projs.shape[1]]
                ##projs = rProjs - lProjs
                ##max = 0
                ##for i in range(0, projs.shape[0]):
                ##    proj = projs[i]
                ##    currMax = numpy.max(proj)
                ##    if(currMax > max):
                ##        max = currMax
                ##        centerAngle = float(fineThetas[i])

                ##end = datetime.datetime.now()
                ##cost = 1000 * (end - begin).total_seconds()
                ##print (cost),'finish'
                ##############################
                #centerAngles = []
                #centerAngles.append(centerAngle)
                #centerAngles.append(fineThetas[1])
                #centerAngles.append(fineThetas[11])

                #projs = transform.radon(image, theta=centerAngles, circle=False)
                #projs = projs.transpose()
                #lProjs = projs[0:3,0:projs.shape[1] - 1]
                #rProjs = projs[0:3,1:projs.shape[1]]
                #projs = rProjs - lProjs

                #max
                #lMax = numpy.max(projs[1])
                #cMax = numpy.max(projs[0])
                #rMax = numpy.max(projs[2])

                #fineAngles = []
                #bestAngle = 0
                #if (cMax > lMax) and (cMax > rMax):
                #    bestAngle = centerAngle
                #    max = cMax
                #elif lMax > cMax:
                #    fineAngles = fineThetas[2:11]
                #    bestAngle = fineThetas[1]
                #    max = lMax
                #else:
                #    fineAngles = fineThetas[12:21]
                #    bestAngle = fineThetas[11]
                #    max = rMax

                #k = numpy.array(fineAngles).shape[0]
                #for i in range(0, k):
                #    currAngle = [fineAngles[i]]
                #    proj = transform.radon(image, theta=currAngle, circle=False)
                #    lProj = proj[0:proj.shape[0] - 1,0]
                #    rProj = proj[1:proj.shape[0],0]
                #    proj = rProj - lProj
                #    currMax = numpy.max(proj)
                #    if(currMax > max):
                #        max = currMax
                #        bestAngle = float(currAngle[0])
                #    else:
                #        break

                #print 'Best angle:',bestAngle
                bestAngle -= 90
                #plt.ion()

                if(abs(bestAngle) > 0.2):
                    correctedImage = transform.rotate(oriImage,bestAngle)
                    bd = int(len * numpy.tan(abs(bestAngle * numpy.pi / 180.0))) + 1
                    correctedImage[0:bd + 1,0:correctedImage.shape[1]] = 1
                    correctedImage[correctedImage.shape[0] - bd:correctedImage.shape[0],0:correctedImage.shape[1]] = 1
                    correctedImage[0:correctedImage.shape[0],0:bd + 1] = 1
                    correctedImage[0:correctedImage.shape[0],correctedImage.shape[1] - bd:correctedImage.shape[1]] = 1
                else:
                    correctedImage = oriImage
   
                proj = (1.0 - correctedImage).sum(axis=0)
                lrBounds = SteinVision.getCenterPart(proj)

                proj = (1.0 - correctedImage).sum(axis=1)
                ulBounds = SteinVision.getCenterPartB(proj)

                ##cp = proj[bounds[0]:bounds[1]]
                #plt.plot(proj[ulBounds[0]:ulBounds[1]])
                ##plt.plot((1.0-correctedImage).sum(axis=0))
                #plt.show()
                #plt.waitforbuttonpress()
                ##plt.close()
                #sp = correctedImage.shape
                io.imsave(saveFolder + "\\" + file,correctedImage[ulBounds[0]:ulBounds[1],lrBounds[0]:lrBounds[1]])
                print 'image ',file,' saved'
            elif("split" == sys.argv[1]):
                n = n + 1
                file = imageFolder+"-"+str(n)+".jpg"
                io.imsave(saveFolder + "\\" + file,oriImage[0:oriImage.shape[0],0:oriImage.shape[1]/2])
                n = n + 1
                file = imageFolder+"-"+str(n)+".jpg"
                io.imsave(saveFolder + "\\" + file,oriImage[0:oriImage.shape[0],oriImage.shape[1]/2:oriImage.shape[1]])
                print 'image ',file,' saved'    
            
                #viewer = viewer.ImageViewer(correctedImage)
                #viewer.show()
    
            end = datetime.datetime.now()
            cost = 1000 * (end - begin).total_seconds()
            print (cost)
            print ''
