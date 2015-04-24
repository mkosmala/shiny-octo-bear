#!/usr/bin/env python

import sys
from PIL import Image
import PIL.ImageOps


if len(sys.argv) < 4 :
    print ("format: resize_AMOS_images.py <list_file> <from_dir> <to_dir>")
    exit(1)
    
filelistfilename = sys.argv[1]
fromdir = sys.argv[2]
todir = sys.argv[3]

with open(filelistfilename,'r') as filelist:

    # remove header line
    filelist.readline()

    # go through all the files in the list and resize them
    for line in filelist:
        line = line.rstrip()

        img = Image.open(fromdir+line)
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

        # resize image if necessary
        if resize:
            ready_image = img.resize((newwidth,newheight),PIL.Image.ANTIALIAS)
        else:
            ready_image = img

        # save
        ready_image.save(todir+line)
        

        
