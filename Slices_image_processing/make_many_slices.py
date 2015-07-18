#!/usr/bin/env python

import sys
import create_slice_image

if len(sys.argv) < 4 :
    print ("format: make_many_slices.py <slice_list> <images_dir> <output_dir>")
    exit(1)
slicefilename = sys.argv[1]
imagesdir = sys.argv[2]
outputdir = sys.argv[3]

with open(slicefilename,'r') as slicefile:

    # remove header
    slicefile.readline()

    # for each line, create a slice file
    for line in slicefile:

        line = line.rstrip()
        tokens = line.split(',')    

        site = tokens[0]
        year = tokens[1]

        print "Processing " + site + " for year " + year

        create_slice_image.create_one_slice(site,int(year),imagesdir,outputdir)
        
