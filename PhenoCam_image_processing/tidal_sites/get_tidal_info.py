#!/usr/bin/env python

import sys
import csv
import datetime
import json
import urllib2

if len(sys.argv) < 3:
    print ("format: get_tidal_info <site_list> <output_file>")
    exit(1)

sitelistfilename = sys.argv[1]
outfilename = sys.argv[2]

# go through all the sites
with open(sitelistfilename,'rb') as sitesfile, open(outfilename,'wb') as outfile:

    # ignore the header
    sitesfile.readline()

    # write the header
    outfile.write("site,date,tide_time,tide_type\n")

    sitereader = csv.reader(sitesfile)

    # for each site
    for row in sitereader:

        site = row[0]
        noaa = row[1]
        start_date = datetime.datetime.strptime(row[2],'%Y-%m-%d')
        stop_date = datetime.datetime.strptime(row[3],'%Y-%m-%d')
        start_year = int(row[2][0:4])
        stop_year = int(row[3][0:4])

        # get tidal info from NOAA
        # http://tidesandcurrents.noaa.gov/api/
        # only allowed to retrieve 1 year at a time

        # for each year
        for yr in range(start_year,stop_year+1):
            day1 = datetime.date(yr,1,1)
            day2 = datetime.date(yr,12,31)
            if yr==start_year:
                day1 = start_date
            if yr==stop_year:
                day2 = stop_date
                
            url = "http://tidesandcurrents.noaa.gov/api/datagetter?"

            request = ("station="+str(noaa)+
                       "&begin_date="+day1.strftime('%Y%m%d')+
                       "&end_date="+day2.strftime('%Y%m%d')+
                       "&product=high_low"+
                       "&datum=STND"+
                       "&time_zone=lst"+
                       "&units=metric"+
                       "&format=json"+
                       "&application=PhenoCam_Harvard_University")

            currURL = url+request

            print " "
            print currURL
            data = json.load(urllib2.urlopen(currURL))

            # parse the year's worth of data
            # in particular, we're just interested in low tides
            for dat in data['data']:
                tide_type = dat['ty']

                #if tide_type=='LL' or tide_type=='L':
                tide_time = datetime.datetime.strptime(dat['t'],'%Y-%m-%d %H:%M')

                outfile.write(site+","+
                              tide_time.strftime('%Y-%m-%d')+","+
                              tide_time.strftime('%H:%M')+","+
                              tide_type+"\n")





    
