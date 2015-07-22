#!/usr/bin/python

import panoptesPythonAPI
import csv
import os
import json
import sys
import codecs

# This script will upload subjects to a project. Note that subject sets should
# already exist.

# ------------------
# FILES WITH CONTENT
# ------------------

auth = "authentication.txt"
baseimagedir = "/home/margaret/processing/"

# -----------
# DEFINITIONS
# -----------

# projects to add subjects to
projname = "Season Spotter Questions"

# vegetation type lookup for metadata
veg_lookup = { "AG":"Agriculture",
               "DB":"Deciduous Broadleaf Forest",
               "DN":"Deciduous Needle-leaf Forest",
               "EB":"Evergreen Broadleaf Forest",
               "EN":"Evergreen Needle-leaf Forest",
               "GR":"Grassland",
               "MX":"Mixed Forest",
               "SH":"Shrubland",
               "TN":"Tundra",
               "WL":"Wetland" }


def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]


# ---
# Create and upload the subjects
# ---
def create_subjects(manifestfile,projid,token):
    
    # read the manifest
    #with codecs.open(manifestfile,'r',encoding='utf-8') as mfile:
    with open(manifestfile,'r') as mfile:
    
        # discard header and get csv object
        mfile.readline()
        mreader = unicode_csv_reader(mfile)

        # for each image
        for row in mreader:
            
            image = row[0]
            subjset = row[1]
            site = row[2]
            vegtype = row[3]
            loc = row[4]
            lat = row[5]
            lon = row[6]
            ele = row[7]

            # convert vegtype abbreviation to full name
            vegdesc = veg_lookup[vegtype]
            
            # check to see if the subject set(s) exists; error if not
            subjsetnum = panoptesPythonAPI.get_subject_set(projid,subjset,token)
            if subjsetnum == -1:
                print "SubjectSet " + subjset + " does not exist. Subject " + image + " not uploaded."

            else:
                # create the metadata object
                meta = """ "#Filename": \"""" + image + """\",
                           "Camera": \"""" + site + """\",
                           "Vegetation type": \"""" + vegdesc + """\",
                           "Location Name": \"""" + loc + """\",
                           "Latitute": \"""" + lat + """\",
                           "Longitude": \"""" + lon + """\",
                           "Elevation": \"""" + ele + """\" """
 
                # create the subject
                print "Adding Subject: " + image
                imagepath = baseimagedir + image
                subjid = panoptesPythonAPI.create_subject(projid,meta,imagepath,token)
                print "   ID: " + subjid

                # add it to the subject set(s)
                print "Linking Subject " + image + " to Subject Set " + subjset
                panoptesPythonAPI.add_subject_to_subject_set(subjsetnum,subjid,token)
        
    return


########
# MAIN #
########

if len(sys.argv) < 2 :
    print ("format: upload_AMOS_subjects <manifest>")
    exit(1)

manifestfile = sys.argv[1]

# get token
with open(auth,'r') as authfile:
    areader = csv.reader(authfile,delimiter=',')
    row = areader.next()
    username = row[0]
    password = row[1]

token = panoptesPythonAPI.get_bearer_token(username,password)

# get project ID
projid = panoptesPythonAPI.get_projectid_from_projectname(projname,username,token)
if projid==-1:
    print "Could not find project " + projname + ". No subjects uploaded."
    exit(0)

# create and upload the subjects
create_subjects(manifestfile,projid,token)

