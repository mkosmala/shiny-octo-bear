#!/usr/bin/env python

import sys
import csv

## MAIN ##
if len(sys.argv) < 6 :
    print ("format: create_manifest <image_list> <paired_image_list> <metadata> <output_file>")
    exit(1)

imagelistfilename = sys.argv[1]
pairedlistfilename = sys.argv[2]
unmasklistfilename = sys.argv[3]
metadatafilename = sys.argv[4]
outputfilename = sys.argv[5]

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
with open(outputfilename,'w') as outputfile:

    # write the header
    outputfile.write("image,subject_set,site,veg_type,location,latitude,longitude,elevation\n")
                     
    # read in the single images
    with open(imagelistfilename,'r') as imagefile:

        # ignore the header
        imagefile.readline()

        # record each image and its associated data
        for line in imagefile:

            line = line.rstrip()
            tokens = line.split(',')
            site = tokens[0]
            vegtype = tokens[1]
            image = tokens[3]
            subjset = vegtype+"_year"
            loc = metadata[site][5]
            lat = metadata[site][2]
            lon = metadata[site][3]
            ele = metadata[site][4]

            outline = image+","+subjset+","+site+","+vegtype+",\""+loc+"\","+lat+","+lon+","+ele+"\n"
            outputfile.write(outline)

    # read in the paired images
    with open(pairedlistfilename,'r') as imagefile:

        # ignore the header
        imagefile.readline()

        # record each (paired) image and its associated data
        for line in imagefile:

            line = line.rstrip()
            tokens = line.split(',')
            site = tokens[0]
            vegtype = tokens[1]
            season = tokens[2]
            image = tokens[7] 
            subjset = vegtype+"_pairs_"+season
            loc = metadata[site][5]
            lat = metadata[site][2]
            lon = metadata[site][3]
            ele = metadata[site][4]

            outline = image+","+subjset+","+site+","+vegtype+",\""+loc+"\","+lat+","+lon+","+ele+"\n"
            outputfile.write(outline)
    
    # read in the unmasked images
    with open(unmasklistfilename,'r') as unmaskfile:

        # ignore the header
        unmaskfile.readline()
       
        # record each image and its associated data
        for line in unmaskfile:

            line = line.rstrip()
            tokens = line.split(',')
            site = tokens[0]
            vegtype = tokens[2]
            workflow = tokens[3]
            image = tokens[4]
            subjset = vegtype+"_unmasked"
            loc = metadata[site][5]
            lat = metadata[site][2]
            lon = metadata[site][3]
            ele = metadata[site][4]

            outline = image+","+subjset+","+site+","+vegtype+",\""+loc+"\","+lat+","+lon+","+ele+"\n"
            outputfile.write(outline)


    
