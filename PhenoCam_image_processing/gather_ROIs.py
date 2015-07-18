#!/usr/bin/env python

import sys
import os

# format:
# <infile> a list of sites to use
# <outfile> an ROI manifest
# <ROI dir> directory of ROI CSV files
if len(sys.argv) < 4 :
    print ("format: gather_ROIs <infile> <outfile> <ROI dir>")
    exit(1)

infilename = sys.argv[1]
outfilename = sys.argv[2]
roidir = sys.argv[3]

# get all the ROI TIFF and CSV files
allfiles = os.listdir(roidir)

# for each site
with open(infilename,'r') as infile, open(outfilename,'w') as outfile:

    # headers for outfile
    outfile.write("site,ROI_type,ROI_seq,ROI_shift_num,start_date,start_time,end_date,end_time,ROI_file\n")

    for line in infile:
        line = line.rstrip()

        tokens = line.split(',')
        site = tokens[0]
        
        # find the matching ROIs
        matchthis = site + "_"
        matchfiles = [s for s in allfiles if matchthis in s]

        # get the csv file(s)
        csvfiles = [s for s in matchfiles if 'roi.csv' in s]

        # for each ROI within each site
        for csvfile in csvfiles:
            
            # get info on the ROI from CSV file name
            print csvfile
            
            roi_info = csvfile.split('_')

            # only use ROIs with 2-letter types
            if len(roi_info[1])==2:

                roi_type = roi_info[1]
                roi_seqno = int(roi_info[2])
            
                # read the csv file
                #print "reading " + roidir+csvfile
                with open(roidir+csvfile,'r') as metafile:

                    # get the corresponding metadata
                    for csvline in metafile:
                        csvline = csvline.rstrip()
                
                        if (len(csvline)>0 and
                            csvline[0] != '#' and
                            csvline[0:5] != "start"):
                            meta = csvline.split(',')

                            #print csvline
                            #print meta
                            #print "----"

                            roi_shift = int((meta[4].split('_'))[3][0:2])

                            # print it to the file                
                            outline = (site+","+roi_type+","+
                                       str(roi_seqno)+","+str(roi_shift)+","+
                                       meta[0]+","+meta[1]+","+meta[2]+","+meta[3]+","+
                                       meta[4]+"\n")

                            outfile.write(outline)
                
                
            



