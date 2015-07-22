#!/usr/bin/env python

import sys
import os
import subprocess
from PIL import Image, ImageFilter
import PIL.ImageOps


if len(sys.argv) < 5 :
    print ("format: process_image_tree_subsets <image_file> <crop_info_file> <image_output_dir> <output_file>")
    exit(1)
imagefilename = sys.argv[1]
cropinfofilename = sys.argv[2]
outputdir2 = sys.argv[3]
outputfilename = sys.argv[4]

# read in the cropping info to a dictionary
cropinfo = {}
with open(cropinfofilename,'r') as cropfile:

    # remove header
    cropfile.readline()

    for line in cropfile:
        line = line.rstrip()
        tokens = line.split(',')

        site = tokens[0]
        side = tokens[1]
        pixels = int(tokens[2])

        cropinfo[site] = (side,pixels)
        

# go through all the files
with open(imagefilename,'r') as imagefile, open(outputfilename,'w') as ofile:

    # remove header line
    imagefile.readline()

    # write header line
    ofile.write("site,date,image\n")

    # for each image file, process it
    for line in imagefile:

        #print line
        
        line = line.rstrip()
        tokens = line.split(',')

        site = tokens[0]
        idate = tokens[1]
        image = tokens[2]

        # get the image size and resize if necessary
        img = Image.open(image)
        imagewidth = img.size[0]
        imageheight = img.size[1]

        # check to see if we have cropping info; if not, don't crop
        if site in cropinfo:

            # crop images
            cropside,croppix = cropinfo[site]
            if cropside=="top":
                cropimg = img.crop((0,croppix,imagewidth,imageheight))
                
            elif cropside=="bottom":
                cropimg = img.crop((0,0,imagewidth,imageheight-croppix))
            
            elif cropside=="all":
                cropimg = img.crop((0,croppix,imagewidth,imageheight-croppix))
            
            else: # no cropping
                cropimg = img

        # no cropping
        else:
            cropimg = img
 
        # resize masked and unmasked images
        ready_unmasked_image = cropimg

        # create output filenames from output dir and image name
        # will store them by site and year
        innameparts = image.split('/')
        fileroot = innameparts[-1].split('.')
        filerootparts = fileroot[0].split('_')
        siteyear = filerootparts[0] + "/" + filerootparts[1] + "/"
        unmaskedoutfilename = outputdir2 + siteyear + fileroot[0] + "_cropped.jpg"

        # create directories if needed and save
        if not os.path.exists(outputdir2 + siteyear):
            os.makedirs(outputdir2 + siteyear)
        ready_unmasked_image.save(unmaskedoutfilename)
            
        # record the output file
        outline = site + "," + idate + "," + unmaskedoutfilename + "\n"
        ofile.write(outline)
                
        
        
