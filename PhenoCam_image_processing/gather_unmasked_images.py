#!/usr/bin/env python

import sys
import csv
import operator

if len(sys.argv) < 5 :
    print ("format: gather_unmasked_images.py <images_file> <resized_dir> <workflow_sort_file> <output_file>")
    exit(1)
    
imagesfilename = sys.argv[1]
resizedir = sys.argv[2]
wfsortfilename = sys.argv[3]
outfilename = sys.argv[4]

# Read in the sorting file and put it all in a dictionary
with open(wfsortfilename,'r') as wfsortfile:

    # ignore header
    wfsortfile.readline()

    # create dictionary
    wfsorter = {}

    # fill dictionary
    for line in wfsortfile:
        line = line.rstrip()
        tokens = line.split(',')
        wfsorter[tokens[1]] = tokens[0]
        

# Open the images file and sort by filename. This will bring images with
# multiple masks next to one another
with open(imagesfilename,'r') as imagesfile:

    # ignore header
    imagesfile.readline()

    # read in all the rest as CSV
    imreader = csv.reader(imagesfile)

    # and sort
    sortedlist = sorted(imreader,key=operator.itemgetter(3))


# Now go through the list and only keep one copy of each image
with open(outfilename,'w') as outfile:

    # header
    outfile.write("site,date,veg_type,workflow,ummasked_image\n")

    lastim = ""
    lastwf = 0

    # go through all lines
    for row in sortedlist:
        im = row[3]
        wf = wfsorter[row[2]]

        printout = False

        # if it's not a duplicate image
        if im != lastim:
            printout = True
            
        # if it is a duplicate image, see if it needs to go in both workflows
        elif wf != lastwf:
            printout = True

        # write to file
        if printout:    

            # change the file name to reflect the resized image
            imagename = row[3]
            parts = imagename.split('/')
            imfilename = parts[-1]
            imyear = parts[-3]
            pathfilename = resizedir + row[0] + "/" + imyear + "/" + imfilename
            
            # write
            outfile.write(row[0]+","+row[1]+","+row[2]+","+wf+","+
                          pathfilename+"\n")
            

        lastim = im
        lastwf = wf
        





        

