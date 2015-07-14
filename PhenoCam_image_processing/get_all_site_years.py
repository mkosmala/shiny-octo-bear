#!/usr/bin/env python

import sys
import os

if len(sys.argv) < 3 :
    print ("format: get_all_site_years <site dir> <outfile>")
    exit(1)

# base directory of all the sites
sitedir = sys.argv[1]
outfilename = sys.argv[2]

with open(outfilename,'wb') as outfile:

    # get all subdirectories (sites)
    allsites = next(os.walk(sitedir))[1]

    # for each site, get available years
    for site in allsites:

        years = next(os.walk(sitedir+site))[1]

        # print out each site and year
        for yr in years:

            # exclude 2015 and ROI directories
            if yr!="2015" and yr!="ROI":
                outfile.write(site+","+yr+"\n")
