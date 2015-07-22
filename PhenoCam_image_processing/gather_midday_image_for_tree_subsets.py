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

    #print imgstr
    #print ind
    
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
    print ("format: gather_midday_image_for_tree_subsets <sites_file> <output_file>")
    exit(1)
sitefilename = sys.argv[1]
outfilename = sys.argv[2]

# go through all the sites, get the midday images
with open(sitefilename,'r') as sitefile, open(outfilename,'w') as outfile:

    # remove header
    sitefile.readline()

    # outfile header
    outfile.write("site,date,site_file\n")

    for line in sitefile:
        line = line.rstrip()
        tokens = line.split(',')
        sitename = tokens[0]
        subset = tokens[2]
        firstdate = get_date(tokens[3],0)
        lastdate = get_date(tokens[4],0)

        # get all the midday images for one site
        mdimglist = midday.getMidDayImageList(sitename,irFlag=False)

        # for each one, check to see if it's got the right date
        for mdimg in mdimglist:

            try: 
                if (mdimg!=""):
                    mdimgdate = get_date(mdimg,1)

                    takeit = False

                    # evergreen: 15th of the month, every month
                    if subset=="E":
                        if mdimgdate.day==15:
                            takeit = True

                    # deciduous or mixed: 7th and 22nd of the month, May-Oct
                    else:
                        if ((mdimgdate.day==7 or mdimgdate.day==22) and
                            mdimgdate.month>4 and mdimgdate.month<11):
                            takeit = True

                    # take this image
                    if takeit:
                        outstr = sitename+","+str(mdimgdate)+","+mdimg+"\n"
                        outfile.write(outstr)

            except ValueError:
                print "error in processing: " + mdimg + "\n"
                
