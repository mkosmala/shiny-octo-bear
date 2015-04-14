#!/usr/bin/env python

import sys
import json
import urllib2

if len(sys.argv)<3:
    print ("format: get_site_image_lists <list_of_sites> <output_dir>")
    exit(1)
sitelistfilename = sys.argv[1]
outdirname = sys.argv[2]

sites = []
# load in all sites
with open(sitelistfilename,'r') as sitelistfile:
    # discard header
    sitelistfile.readline()
    for line in sitelistfile:
        line = line.rstrip()
        sites.append(line)

summaryfilename = outdirname + "AMOS_summary.csv"
with open(summaryfilename,'w') as summaryfile:

    # write header
    summaryfile.write("webcam,num_images\n")

    # for each site
    for site in sites:

        # create an output file
        outfilename = outdirname + "webcam_" + site + "_image_list.csv"
        with open(outfilename,'w') as outfile:

            # print header line
            outfile.write("date,time,filename,URL\n")

            # note the number of images once
            first_time = True

            # make the first request   
            fetching_data = True
            currURL = "http://amos14.cse.wustl.edu/REST/images/?webcam="+site+"&format=json"

            # fetch all the data
            while fetching_data:

                # get the data
                print "calling: " + currURL 
                data = json.load(urllib2.urlopen(currURL))

                # record the number of images
                if first_time:
                    summaryfile.write(site+","+str(data['count'])+"\n")
                    first_time = False

                # write image names and metadata to file
                for item in data['results']:
                    url = item['image_url']
                    url_bits = url.split('/')
                    url_filename = url_bits[-1]
                    date = (url_filename[0:4] + "-" + url_filename[4:6] +
                            "-" + url_filename[6:8])
                    time = (url_filename[9:11] + ":" + url_filename[11:13] +
                            ":" + url_filename[13:15])
                    
                    outfile.write(date+","+time+","+
                                  url_filename+","+
                                  url+"\n")

                # get next page
                if data['next']:
                    currURL = data['next']
                else:
                    fetching_data = False
                         
