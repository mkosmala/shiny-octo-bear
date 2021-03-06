#!/usr/bin/env python

import sys
import datetime
import re

# pre-defined constants
# -----
# We will give the algorithm a two week buffer before sos and sof
# and a two week buffer after eos and eof.
#
# We will pair images at 1, 3, and 7 day offsets (ideally).
SOS_BUFFER = 14
EOS_BUFFER = 14
SOF_BUFFER = 14
EOF_BUFFER = 14
DATEDIFF = (1,3,7)

# returns the date when given a string
# specify the index where the year begins when parsed
def get_date(imgstr,ind=0):
    parts = re.split("_|-",imgstr)
    retdate = datetime.date(int(parts[ind]),int(parts[ind+1]),int(parts[ind+2]))
    return retdate

# return the line to output to file
def prepare_data(imagesfilename,site,season,datediff,date1,date2):

    #print site + "," + str(datediff) + "," + str(date1) + "," + str(date2)

    with open(imagesfilename,'r') as imagefile:

        # indicator of what we've found so far
        ind = 0 
        foundSite = False

        # look for the proper images
        while ind < 2:

            #print "while3"
            #print ind
            
            line = imagefile.readline().rstrip()

            # end of file
            if line=="":
                ind=3

            # keep going
            else:
        
                tokens = line.split(',')
    
                fsite = tokens[0]         
                fdate = tokens[1]
                fveg = tokens[2]
                fimage = tokens[4]

                #print line

                if fsite==site:
                    foundSite = True
                elif foundSite:
                    ind = 3

                # look for the right site
                if fsite==site and fveg=="DB":

                    # match the first 
                    if ind==0 and get_date(fdate)==date1:
                        image1 = fimage
                        ind = 1

                    # match second
                    elif ind==1 and get_date(fdate)==date2:
                        image2 = fimage
                        ind = 2

                # we won't find the image
                if fsite==site:
                    foundSite = True
                elif foundSite:
                    ind = 3

                

    # compose the data line
    retline = ""
    if ind == 2:
        retline = (site + "," + fveg + "," + season + "," +
               str(datediff) + "," + str(date1) + "," + str(date2) + "," +
               image1 + "," + image2 + "\n")

    #print retline

    return retline
   
            

## MAIN ##
if len(sys.argv) < 3 :
    print ("format: gather_pairs <transition_file> <masked_images_file> <output_file>")
    exit(1)
transitionsfilename = sys.argv[1]
imagesfilename = sys.argv[2]
outfilename = sys.argv[3]

# open the files
with open(transitionsfilename,'r') as transfile, open(outfilename,'w') as outfile:

    # discard input header
    transfile.readline()

    # write output header
    outfile.write("site,veg_type,season,datediff,date1,date2,image1,image2\n")

    # read each site-year transition dates
    for line in transfile:
        line = line.rstrip()
        tokens = line.split(',')
        site = tokens[0]
        siteyear = tokens[1]
        sos = get_date(tokens[2])
        eos = get_date(tokens[4])
        sof = get_date(tokens[5])
        eof = get_date(tokens[7])

        #print line

        # these are our window dates
        springstart = sos - datetime.timedelta(SOS_BUFFER)
        springend = eos + datetime.timedelta(EOS_BUFFER)
        fallstart = sof - datetime.timedelta(SOF_BUFFER)
        fallend = eof + datetime.timedelta(EOF_BUFFER)

        # for each date-differential, collect pairs
        for ddiff in DATEDIFF:

            #print "ddiff = " + str(ddiff)

            # spring
            date1 = springstart
            date2 = springstart + datetime.timedelta(ddiff)

            while date2 <= springend:

                #print "while1 " + str(date2) + ", " + str(springend)

                # write to file
                outline = prepare_data(imagesfilename,site,"spring",ddiff,date1,date2)

                #print outline
                
                outfile.write(outline)

                #print "  written"

                # move forward one day
                date1 = date1 + datetime.timedelta(1)
                date2 = date2 + datetime.timedelta(1)

                #print "  " + str(date2)
        
            # fall
            date1 = fallstart
            date2 = fallstart + datetime.timedelta(ddiff)

            while date2 <= fallend:

                #print "while2"

                # write to file
                outline = prepare_data(imagesfilename,site,"fall",ddiff,date1,date2)
                if outline != "":
                    outfile.write(outline)

                # move forward one day
                date1 = date1 + datetime.timedelta(1)
                date2 = date2 + datetime.timedelta(1)

    
