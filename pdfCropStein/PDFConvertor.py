import os
from os import listdir
from os.path import isfile, join

def pdfToImages(pdfFile,imageFolder):

    if not os.path.exists(imageFolder):
        os.mkdir(imageFolder)
    else:
        print imageFolder," already exists, please check it.."
        return

    ars = "\"C:\\Program Files\\gs\\gs9.19\\bin\\gswin64.exe\" -dNOPAUSE -sDEVICE=jpeg -r300 -o" + imageFolder + "\\" + imageFolder + "-%d.jpg " + pdfFile;

    os.system(ars)

    print "pdf converted, images saved in ",imageFolder
    return

def imagesToPDF(imageFolder, pdfFile):
    if(os.path.exists(pdfFile)):
       print pdfFile,"already exists, please check.."
       return

    files = [f for f in listdir(imageFolder) if isfile(join(imageFolder, f))]
  
    if(files.count>0):
        vor = len(files[0].split('-')[0]) + 1
        nach = len(files[0].split('.')[0])
        vorName = files[0][0:vor-1]
        min = 9999
        max = 0
        for i in range(0,len(files)):
            vor = len(files[i].split('-')[0]) + 1
            nach = len(files[i].split('.')[0])
            num = int(files[i][vor:nach])
            if(num>max):
                max = num
            if(num<min):
                min = num
        #ars = "convert "+ imageFolder + "\\*.jpg -adjoin " + pdfFile
        if((max-min)>50):
            start = min
            curr = min+50
        else:
            start = min
            curr = max

        fileIndex = 0
        
        allPDFfiles = []
        while(curr<=max):
           fileIndex = fileIndex + 1
           print "convert page ",str(start)," to ",str(curr)
           ars = "convert "
           for page in range(start,curr+1):
             file = vorName + "-" + str(page) + ".jpg"
             ars = ars + join(imageFolder,file) + " "
           ars = ars + imageFolder + str(fileIndex) + ".pdf"
           os.system(ars)
           allPDFfiles.append(imageFolder+str(fileIndex)+".pdf")
           start = curr + 1
           curr = start + 50

        fileIndex = fileIndex + 1
        print "convert page ",str(start)," to ",str(max)
        ars = "convert "
        for page in range(start,max+1):
            file = vorName + "-" + str(page) + ".jpg"
            ars = ars + join(imageFolder,file) + " "
        ars = ars + imageFolder + str(fileIndex) + ".pdf"
        allPDFfiles.append(imageFolder+str(fileIndex)+".pdf")
        os.system(ars)
        
        mergeArs = "gswin64 -dNOPAUSE -sDEVICE=pdfwrite -sOUTPUTFILE=" + pdfFile + " -dBATCH"
        for file in allPDFfiles:
            mergeArs = mergeArs + " " + file
        os.system(mergeArs)
        print "All images in ",imageFolder," converted to ",pdfFile
        return
