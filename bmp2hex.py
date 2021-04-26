from matplotlib.image import imread
from PIL import Image
import os

# read all the file from image folder 
dirs = os.listdir('./images/')
for files in dirs:
    file = './images/'+files;
    base = os.path.basename(file)
    fileName, fileType = os.path.splitext(base);
    # select bmp file
    if fileType == ".bmp":
        rgb = imread(file)
        img = rgb[:,:,0]
        width = img.shape[0]
        heigth = img.shape[1]
        cfile = open('./images/'+fileName + ".c","w+")
        hfile = open('./images/'+fileName + ".h","w+")
        hfile.write("#ifndef _"+fileName.upper()+"_INCLUDED_\n #define _"+fileName.upper()+"_INCLUDED_\n extern flash unsigned char "+fileName+"[];\n#endif")
        hfile.close()
        # define var that keep hex of bmp image
        string = "flash unsigned char "+fileName+"[]={\n"+hex(heigth)+", 0x00,\n"+hex(width)+", 0x00, \n#ifndef _GLCD_DATA_BYTEY_\n"
        counter = 0
        # horizental row
        for i in range(width):
            for j in range(int(heigth/8)):
                counter += 1 
                decNumber = 0 
                for bin in range(8):
                    if(img[i][j * 8 + bin] == 0):
                        decNumber += pow(2, bin)
                string += str(format(decNumber, "#04x")) + ", "
                if counter % 8 == 0:     
                    string += "\n"

        string += "#else\n"
        # vertical row
        for i in range(int(width/8)):
            for j in range(heigth):
                counter += 1 
                decNumber = 0 
                for bin in range(8):
                    if(img[i * 8 + bin][j] == 0):
                        decNumber += pow(2, bin)
                string += str(format(decNumber, "#04x")) + ", "
                if counter % 8 == 0:     
                    string += "\n"

        string += "#endif\n};"
        # write var string in c file
        cfile.write(string) 
        cfile.close()