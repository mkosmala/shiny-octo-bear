#!/usr/bin/env python

import sys
import os
import subprocess
from PIL import Image
import PIL.ImageOps


if len(sys.argv) < 6 :
    print ("format: process_image_files <image_file> <roi_dir> <masked_output_dir> <unmasked_output_dir> <output_file>")
    exit(1)
imagefilename = sys.argv[1]
roidir = sys.argv[2]
outputdir1 = sys.argv[3]
outputdir2 = sys.argv[4]
outputfilename = sys.argv[5]

# level of transparency (0=opaque,1=fully transparent)
transparency = 0.25

# go through all the files
with open(imagefilename,'r') as imagefile, open(outputfilename,'w') as ofile:

    # remove header line
    imagefile.readline()

    # write header line
    ofile.write("site,veg_type,date,masked_image\n")

    # initialize all black and white for the composite
    allblack = Image.new("RGB",(1296,960),"black")
    
    # for speed, keep track of mask properties
    mask = ""

    # for each image file, process it
    for line in imagefile:
        line = line.rstrip()
        tokens = line.split(',')

        image = tokens[3]
        newmask = roidir+tokens[4]

        # get the mask name
        masknameparts = tokens[4].split('_')
        maskname = masknameparts[1] + masknameparts[2]

        # get the image size and resize if necessary
        img = Image.open(image)
        imagewidth = img.size[0]
        imageheight = img.size[1]

        # check sizing
        # calculate aspect ratio
        aspect = float(imagewidth)/float(imageheight)
        resize = False
        # normal, square, or tall&skinny
        if aspect<=1.35 and imageheight>600:
            newheight=600
            newwidth=int(600*float(imagewidth)/float(imageheight))
            resize = True
        # wide
        elif imagewidth>720:
            newwidth=720
            newheight=int(720*float(imageheight)/float(imagewidth))
            resize = True
            
        # get the mask size and resize if necessary
        if newmask != mask:
            mask = newmask
            maskimg = Image.open(mask)
            maskwidth = maskimg.size[0]
            maskheight = maskimg.size[1]

            # check sizing
            if maskwidth != imagewidth or maskheight != maskheight: 
                print "Error: non-matching mask size. "
                print "Image = " + str(img.size) + ", Mask = " + str(maskimg.size)
                print line
                exit(1)

            # resize the merging mask if necessary
            if (allblack.size[0] != img.size[0] or
                allblack.size[1] != img.size[1]):
                allblack = Image.new("RGB",img.size,"black")

            # negate the mask and add transparency
            transimg = Image.blend(maskimg.convert("RGB"),allblack,transparency)
            invimg = PIL.ImageOps.invert(transimg.convert("L"))

        # apply the mask to the image
        outimg = Image.composite(img,allblack,invimg)

        # resize masked and unmasked images
        if resize:
            ready_masked_image = outimg.resize((newwidth,newheight),PIL.Image.ANTIALIAS)
            ready_unmasked_image = img.resize((newwidth,newheight),PIL.Image.ANTIALIAS)
        else:
            ready_masked_image = outimg
            ready_unmasked_image = img

        # create output filenames from output dir and image name
        # will store them by site and year
        innameparts = image.split('/')
        fileroot = innameparts[-1].split('.')
        filerootparts = fileroot[0].split('_')
        siteyear = filerootparts[0] + "/" + filerootparts[1] + "/"
        maskedoutfilename = outputdir1 + siteyear + fileroot[0] + "_masked_" + maskname + ".jpg"
        unmaskedoutfilename = outputdir2 + siteyear + fileroot[0] + "_unmasked.jpg"

        # create directories if needed and save
        if not os.path.exists(outputdir1 + siteyear):
            os.makedirs(outputdir1 + siteyear)  
        ready_masked_image.save(maskedoutfilename)

        if not os.path.exists(outputdir2 + siteyear):
            os.makedirs(outputdir2 + siteyear)
        ready_unmasked_image.save(unmaskedoutfilename)
            
        # record the masked file
        outline = tokens[0] + "," + tokens[2] + "," + tokens[1] + "," + maskedoutfilename + "\n"
        ofile.write(outline)
                
        
        
