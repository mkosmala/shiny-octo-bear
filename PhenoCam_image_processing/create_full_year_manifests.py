#!/usr/bin/env python

import sys
import csv

## MAIN ##
if len(sys.argv) < 4 :
    print ("format: create_full_year_manifests <image_list> <metadata> <output_file_stem>")
    exit(1)

imagelistfilename = sys.argv[1]
metadatafilename = sys.argv[2]
outputfilestem = sys.argv[3]

# create output file names
agoutfn = outputfilestem + "_AG.csv"
dnoutfn = outputfilestem + "_DN.csv"
enoutfn = outputfilestem + "_EN.csv"
shoutfn = outputfilestem + "_SH.csv"
dboutfn = outputfilestem + "_DB.csv"
eboutfn = outputfilestem + "_EB.csv"
groutfn = outputfilestem + "_GR.csv"

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
with open(agoutfn,'w') as agoutfile, open(dnoutfn,'w') as dnoutfile, open(enoutfn,'w') as enoutfile, open(shoutfn,'w') as shoutfile, open(dboutfn,'w') as dboutfile, open(eboutfn,'w') as eboutfile, open(groutfn,'w') as groutfile:

    # write the headers
    agoutfile.write("image,subject_set,site,veg_type,location,latitude,longitude,elevation\n")
    dnoutfile.write("image,subject_set,site,veg_type,location,latitude,longitude,elevation\n")
    enoutfile.write("image,subject_set,site,veg_type,location,latitude,longitude,elevation\n")
    shoutfile.write("image,subject_set,site,veg_type,location,latitude,longitude,elevation\n")
    dboutfile.write("image,subject_set,site,veg_type,location,latitude,longitude,elevation\n")
    eboutfile.write("image,subject_set,site,veg_type,location,latitude,longitude,elevation\n")
    groutfile.write("image,subject_set,site,veg_type,location,latitude,longitude,elevation\n")
    
    # read in the unmasked images
    with open(imagelistfilename,'r') as imagefile:

        # ignore the header
        imagefile.readline()
       
        # record each image and its associated data
        for line in imagefile:

            line = line.rstrip()
            tokens = line.split(',')
            site = tokens[0]
            vegtype = tokens[2]
            subjset = tokens[3]
            image = tokens[4]
            loc = metadata[site][5]
            lat = metadata[site][2]
            lon = metadata[site][3]
            ele = metadata[site][4]

            outline = image+","+subjset+","+site+","+vegtype+",\""+loc+"\","+lat+","+lon+","+ele+"\n"

            if subjset=='AG_full_year':
                writefile = agoutfile
            elif subjset=='DN_full_year':
                writefile = dnoutfile
            elif subjset=='EN_full_year':
                writefile = enoutfile
            elif subjset=='SH_full_year':
                writefile = shoutfile
            elif subjset=='DB_full_year':
                writefile = dboutfile
            elif subjset=='EB_full_year':
                writefile = eboutfile
            elif subjset=='GR_full_year':
                writefile = groutfile
            else:
                print "Error!"
                exit(1)
            
            writefile.write(outline)


    
