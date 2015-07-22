#!/usr/bin/env python

import sys
import csv
import operator

if len(sys.argv) < 5 :
    print ("format: gather_full_year_images.py <images_file> <resized_dir> <veg_type_to_subj_set_file> <output_file>")
    exit(1)
    
imagesfilename = sys.argv[1]
resizedir = sys.argv[2]
vttssfilename = sys.argv[3]
outfilename = sys.argv[4]

# Read in the sorting file and put it all in a dictionary
with open(vttssfilename,'r') as vttssfile:

    # ignore header
    vttssfile.readline()

    # create dictionary
    vttss = {}

    # fill dictionary
    for line in vttssfile:
        line = line.rstrip()
        tokens = line.split(',')
        vttss[tokens[0]] = tokens[1]
        

# Open the images file and sort by filename. This will bring images with
# multiple masks next to one another
with open(imagesfilename,'r') as imagesfile:

    # ignore header
    imagesfile.readline()

    # read in all the rest as CSV
    imreader = csv.reader(imagesfile)

    # and sort
    sortedlist = sorted(imreader,key=operator.itemgetter(3))


# Now go through the list and spit out the relevent info
with open(outfilename,'w') as outfile:

    # header
    outfile.write("site,date,veg_type,subject_set,ummasked_image\n")

    # go through all lines
    for row in sortedlist:

        ss = vttss[row[2]]
                
        # change the file name to reflect the resized image
        imagename = row[3]
        parts = imagename.split('/')
        imfilename = parts[-1]
        imyear = parts[-3]
        pathfilename = resizedir + row[0] + "/" + imyear + "/" + imfilename[:-4] + "_unmasked.jpg"
            
        # write
        outfile.write(row[0]+","+row[1]+","+row[2]+","+ss+","+
                          pathfilename+"\n")
            






        

