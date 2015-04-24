#!/usr/bin/env python

import sys
import os
import subprocess
from PIL import Image
import PIL.ImageOps

if len(sys.argv) < 5 :
    print ("format: glue_paried_images <images_file> <crop_info_file> <output_dir> <output_list_file>")
    exit(1)
imagefilename = sys.argv[1]
cropinfofilename = sys.argv[2]
outputdir = sys.argv[3]
outputfilename = sys.argv[4]

# read the crop info into a dictionary
cropinfo = {}
with open(cropinfofilename,'r') as cropinfofile:

    # remove header line
    cropinfofile.readline()

    # save each line to the dictionary
    for line in cropinfofile:
        line = line.rstrip()
        tokens = line.split(',')    
        cropinfo[tokens[0]+tokens[1]] = (tokens[2],tokens[3])
     
# go through all the files
with open(imagefilename,'r') as imagefile, open(outputfilename,'w') as ofile:

    # remove header line
    imagefile.readline()

    # write header line
    ofile.write("site,veg_type,season,datediff,date1,date2,reverse,image\n")

    # for each image file, process it
    for line in imagefile:
        line = line.rstrip()
        tokens = line.split(',')    

        site = tokens[0]
        vegtype = tokens[1]
        season = tokens[2]
        datediff = tokens[3]
        date1 = tokens[4]
        date2 = tokens[5]
        image1 = tokens[6]
        image2 = tokens[7]

        # open images
        img1 = Image.open(image1)
        img2 = Image.open(image2)

        # double-check image sizing
        if (img1.size[0] != img2.size[0] or
            img1.size[1] != img2.size[1]):
            print "Error: images are different sizes."
            print "Img1 = " + str(img1.size) + ", Img2 = " + str(img2.size)
            print line
            exit(1)

        # crop the data lines out of the images
        info = cropinfo[site+date1[0:4]]
        
        # crop off the top
        if (info[0]=="top"):
            cropdim = (0,int(img1.size[1]*float(info[1])),img1.size[0],img1.size[1])
        # crop off the bottom
        else:
            cropdim = (0,0,img1.size[0],int(img1.size[1]*(1-float(info[1]))))

        # crop
        img1 = img1.crop(cropdim)
        img2 = img2.crop(cropdim)

        # create canvases the height and double-width of the images
        # one canvas for the images chronologically
        # one canvas for the images reverse chronologically
        canvas1 = Image.new("RGBA",(img1.size[0]*2,img1.size[1]),None)
        canvas2 = Image.new("RGBA",(img1.size[0]*2,img1.size[1]),None)
        
        # paste on the first image
        canvas1.paste(img1,(0,0))
        canvas2.paste(img1,(img2.size[0]+1,0))
        
        # paste on the second image
        canvas1.paste(img2,(img1.size[0]+1,0))
        canvas2.paste(img2,(0,0))

        # shrink these images so they fit nicely
        newwidth = 720
        newheight = int(720*float(img1.size[1])/float(2*img1.size[0]))
        outimg1 = canvas1.resize((newwidth,newheight),PIL.Image.ANTIALIAS)
        outimg2 = canvas2.resize((newwidth,newheight),PIL.Image.ANTIALIAS)
        
        # create output file names
        # file name will be first image, date diff, and chronology
        # saved in directory based on site and year
        innameparts = image1.split('/')
        fileroot = innameparts[-1].split('.')
        newname1 = fileroot[0] + "_pair_diff" + datediff + ".jpg"
        newname2 = fileroot[0] + "_pair_diff" + datediff + "r.jpg"
        siteyear = innameparts[-3] + "_pairs/" + innameparts[-2] + "/"

        # create directory if needed and save
        if not os.path.exists(outputdir + siteyear):
            os.makedirs(outputdir + siteyear)  
        outimg1.save(outputdir + siteyear + newname1)
        outimg2.save(outputdir + siteyear + newname2)

        # write image file name to list
        outline1 = (site + "," + vegtype + "," + season + "," +
                    datediff + "," + date1 + "," + date2 +
                    ",0," + outputdir + siteyear + newname1 + "\n")
        outline2 = (site + "," + vegtype + "," + season + "," +
                    datediff + "," + date1 + "," + date2 +
                    ",1," + outputdir + siteyear + newname2 + "\n")
        ofile.write(outline1)
        ofile.write(outline2)
