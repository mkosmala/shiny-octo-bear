#!/usr/bin/env python

import sys
import datetime
import re
import midday

# returns the date when given a string
# specify the index where the year begins when parsed
# and the parsing character
def get_date(imgstr,ind):
    parts = re.split("_|-",imgstr)
    retdate = datetime.date(int(parts[ind]),int(parts[ind+1]),int(parts[ind+2]))
    return retdate


# same but gets the time too
def get_datetime(imgstr,ind):
    parts = re.split("_|-|:",imgstr)
    retdt = datetime.datetime(int(parts[ind]),int(parts[ind+1]),int(parts[ind+2]),
                              int(parts[ind+3][0:2]),int(parts[ind+3][2:4]),int(parts[ind+3][4:6]))
    return retdt

def get_datetime2(dstr,tstr):
        
    # error handle for bad form of others
    if tstr == "24:00:00":
        tstr = "23:59:59"
    
    dparts = re.split("_|-",dstr)
    tparts = re.split(":",tstr)
    
    retdt = datetime.datetime(int(dparts[0]),int(dparts[1]),int(dparts[2]),
                              int(tparts[0]),int(tparts[1]),int(tparts[2]))
    return retdt

# return the metadata for a particular site and day or error that there is no ROI file
# there might be more than one!
def roilookup(roimeta,sitename,imgdatetime):
    
    matches = []
    for line in roimeta:
        tokens = line.split(',')
        if (tokens[0]==sitename):
            startdt = get_datetime2(tokens[4],tokens[5])
            enddt = get_datetime2(tokens[6],tokens[7])
            if (imgdatetime >= startdt and imgdatetime <= enddt):
                matches.append(line)
    return matches
    

## MAIN ##
if len(sys.argv) < 3 :
    print ("format: gather_midday_image_filenames_and_associated_ROIs <sites_file> <roi_file> <output_file>")
    exit(1)
sitefilename = sys.argv[1]
roifilename = sys.argv[2]
outfilename = sys.argv[3]

# get all the roi info and save it
with open(roifilename,'r') as roifile:
     roimeta = roifile.readlines()

# go through all the sites, get the midday images, and add roi metadata
with open(sitefilename,'r') as sitefile, open(outfilename,'w') as outfile:

    # outfile header
    outfile.write("site,date,veg_type,site_file,ROI_mask_file\n")

    for line in sitefile:
        line = line.rstrip()
        tokens = line.split(',')
        sitename = tokens[0]
        firstdate = get_date(tokens[1],0)
        lastdate = get_date(tokens[2],0)

        # get all the midday images for one site
        mdimglist = midday.getMidDayImageList(sitename,irFlag=False)

        # for each one, check to see if it's in the right date range
        for mdimg in mdimglist:
            if (mdimg!=""):
                mdimgdate = get_date(mdimg,1)
                if (mdimgdate >= firstdate and mdimgdate <= lastdate):

                    # if so, look up the proper ROI
                    mdimgdatetime = get_datetime(mdimg,1)
                    roiinfo = roilookup(roimeta,sitename,mdimgdatetime)

                    # if there's no ROI then presumably, it's not part of the
                    # dataset, but print message anyway
                    if len(roiinfo)==0:
                        print "No ROI available for " + sitename + ", " + str(mdimgdatetime)
                    else:
                        # output to file possibly multiple site-ROI pairs
                        for roi in roiinfo:
                            toks = roi.split(',')
                            outstr = (sitename+","+str(mdimgdate)+","+toks[1]+","+
                                      mdimg+","+toks[8])
                            outfile.write(outstr)
                          
                        
                    

