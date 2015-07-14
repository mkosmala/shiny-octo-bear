#!/usr/bin/env python

import sys

if len(sys.argv) < 3 :
    print ("format: consolidate_site_years <infile> <outfile>")
    exit(1)

# assume the input file is sorted by site and then year
infilename = sys.argv[1]
outfilename = sys.argv[2]

with open(infilename,'rb') as infile, open(outfilename,'wb') as outfile:

    cursite = "none"

    for line in infile:
        line = line.rstrip()
        tokens = line.split(',')

        site = tokens[0]
        year = tokens[1]

        if site==cursite:
            lastyear = year
        else:
            # write the previous site
            if cursite!="none":
                outfile.write(cursite+","+firstyear+"_01_01,"+lastyear+"_12_31\n")
            
            # start the next site
            firstyear = year
            lastyear = year
            cursite = site

    # write the last site
    outfile.write(cursite+","+firstyear+"_01_01,"+lastyear+"_12_31\n")
    
