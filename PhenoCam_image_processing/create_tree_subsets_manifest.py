#!/usr/bin/env python

import sys
import csv

## MAIN ##
if len(sys.argv) < 4 :
    print ("format: create_tree_subsets_manifest <image_list> <metadata> <output_file>")
    exit(1)

imagelistfilename = sys.argv[1]
metadatafilename = sys.argv[2]
outputfilename = sys.argv[3]

# read in the metadata file and create a dictionary to the site info
with open(metadatafilename,'r') as metadatafile:

    # initialize the dictionary
    metadata = {}

    # ignore the header
    metadatafile.readline()

    # get each site's data
    metadatareader = csv.reader(metadatafile,delimiter=',',quotechar='\"')
    for row in metadatareader:
        dictkey = row[0]
        metadata[dictkey] = row

# open the output file
with open(outputfilename,'w') as outfile:

    # write the headers
    outfile.write("image,site,location,latitude,longitude,elevation\n")
    
    # read in the unmasked images
    with open(imagelistfilename,'r') as imagefile:

        # ignore the header
        imagefile.readline()
       
        # record each image and its associated data
        for line in imagefile:

            line = line.rstrip()
            tokens = line.split(',')
            site = tokens[0]
            image = tokens[2]
            loc = metadata[site][5]
            lat = metadata[site][2]
            lon = metadata[site][3]
            ele = metadata[site][4]

            outline = image+","+site+",\""+loc+"\","+lat+","+lon+","+ele+"\n"

            outfile.write(outline)


    
