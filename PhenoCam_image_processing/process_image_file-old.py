#!/usr/bin/env python

# until we get a python API, let's do this by command line

import sys
import subprocess
import PythonMagick 


if len(sys.argv) < 3 :
    print ("format: process_image_file <image_file> <roi_dir> <output_dir>")
    exit(1)
imagefilename = sys.argv[1]
roidir = sys.argv[2]
outputdir = sys.argv[3]

with open(imagefilename,'r') as imagefile:

    # remove header line
    imagefile.readline()

    # for speed, keep track of mask properties
    mask = ""

    # for each image file, process it
    for line in imagefile:
        line = line.rstrip()
        tokens = line.split(',')

        image = tokens[3]
        newmask = roidir+tokens[4]        

        # get the image size and resize if necessary
        img = PythonMagick.Image(image)
        imagewidth = img.size().width()
        imageheight = img.size().height()
        if imagewidth != 1296 or imageheight != 960: 
            # resize
            print "wrong size image!"
            exit(1)

        # get the mask size and resize if necessary
        if newmask != mask:
            mask = newmask
            maskimg = PythonMagick.Image(mask)
            maskwidth = maskimg.size().width()
            maskheight = maskimg.size().height()
            if maskwidth != 1296 or maskheight != 960: 
                # resize
                print "wrong size mask!"
                exit(1)

            # negate the mask and make the white part transparent
            maskimg.negate()
            maskimg.transparent(PythonMagick.Color("white"))

        # apply the mask to the image
        img.composite(maskimg,0,0,PythonMagick.CompositeOperator.DissolveCompositeOp)

        
                

# masking commands for ImageMagick
# the '50' can vary from 0 to 100 to control masking --
#   might want it a little darker
# ---
# convert ./dukehw_DB_0001_01.tif -negate temp1.tiff
# convert temp1.tiff -transparent white temp2.png
# composite -dissolve 50 ./temp2.png ./dukehw_2013_06_01_120111.jpg output.jpg




        
        

            # using ImageMagick directly
            #maskinfo = subprocess.check_output(["identify",mask])
            #masksize = maskinfo.split(' ')[2]
            #if masksize != "1296x960":
                # resize


        

        
        
