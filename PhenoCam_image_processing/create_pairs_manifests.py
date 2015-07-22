#!/usr/bin/env python

import sys
import csv

## MAIN ##
if len(sys.argv) < 4 :
    print ("format: create_paris_manifests <image_list> <metadata> <output_file_stem>")
    exit(1)

imagelistfilename = sys.argv[1]
metadatafilename = sys.argv[2]
outputfilestem = sys.argv[3]

# create output file names
dbspringoutfn = outputfilestem + "_DB_spring.csv"
dbfalloutfn = outputfilestem + "_DB_fall.csv"
dnspringoutfn = outputfilestem + "_DN_spring.csv"
dnfalloutfn = outputfilestem + "_DN_fall.csv"


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

# open the output files
with open(dbspringoutfn,'w') as dbspringoutfile, open(dbfalloutfn,'w') as dbfalloutfile, open(dnspringoutfn,'w') as dnspringoutfile, open(dnfalloutfn,'w') as dnfalloutfile:

    # write the headers
    dbspringoutfile.write("image,subject_set,site,veg_type,location,latitude,longitude,elevation\n")
    dbfalloutfile.write("image,subject_set,site,veg_type,location,latitude,longitude,elevation\n")
    dnspringoutfile.write("image,subject_set,site,veg_type,location,latitude,longitude,elevation\n")
    dnfalloutfile.write("image,subject_set,site,veg_type,location,latitude,longitude,elevation\n")
    
    # read in the unmasked images
    with open(imagelistfilename,'r') as imagefile:

        # ignore the header
        imagefile.readline()
       
        # record each image and its associated data
        for line in imagefile:

            line = line.rstrip()
            tokens = line.split(',')
            site = tokens[0]
            vegtype = tokens[1]
            season = tokens[2]
            image = tokens[7]
            loc = metadata[site][5]
            lat = metadata[site][2]
            lon = metadata[site][3]
            ele = metadata[site][4]

            subjset = vegtype + "_pairs_" + season

            outline = image+","+subjset+","+site+","+vegtype+",\""+loc+"\","+lat+","+lon+","+ele+"\n"

            if subjset=='DB_pairs_spring':
                writefile = dbspringoutfile
            elif subjset=='DN_pairs_spring':
                writefile = dnspringoutfile
            elif subjset=='DB_pairs_fall':
                writefile = dbfalloutfile
            elif subjset=='DN_pairs_fall':
                writefile = dnfalloutfile
            else:
                print "Error!"
                exit(1)
            
            writefile.write(outline)


    
