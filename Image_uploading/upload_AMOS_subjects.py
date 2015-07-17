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
imagedir = "/home/margaret/AMOS/AMOS_images/"

# -----------
# DEFINITIONS
# -----------

# projects to add subjects to
projname = "Season Spotter Image Marking"
subjset = "AMOS_sample"



# ---
# Create and upload the subjects
# ---
def create_subjects(manifestfile,projid,token):
    
    # read the manifest
    with codecs.open(manifestfile,'r',encoding='utf-8') as mfile:

        # discard the BOM
        mfile.seek(2)
    
        # discard header and get csv object
        mfile.readline()
    
        # for each image
        mreader = csv.reader(mfile,delimiter=',',quotechar='\"')
        for row in mreader:

            print row
            
            image = row[0]
            cam = row[1]
            loc = row[2]
            lat = row[3]
            lon = row[4]
            
            # check to see if the subject set(s) exists; error if not
            subjsetnum = panoptesPythonAPI.get_subject_set(projid,subjset,token)
            if subjsetnum == -1:
                print "SubjectSet " + subjset + " does not exist. Subject " + image + " not uploaded."

            else:
                # create the metadata object
                meta = """ "Filename": \"""" + image + """\",
                           "Webcam": \"""" + cam + """\",
                           "Location Name": \"""" + loc + """\",
                           "Latitute": \"""" + lat + """\",
                           "Longitude": \"""" + lon + """\" """

                # convert to unicode in case of accents, umlauts, and the like
                # 'decode' is from str to unicode 
                #meta = to_unicode(rawmeta)

                # create the subject
                print "Adding Subject: " + image
                imagepath = imagedir + image
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

