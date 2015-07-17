#!/usr/bin/python

import panoptesPythonAPI
import csv
import os
import json

# This script will upload subjects to a project. Note that subject sets should
# already exist.

# ------------------
# FILES WITH CONTENT
# ------------------

auth = "authentication.txt"
linkfile = "subjectsets_and_workflows.csv"
#manifestfile = "beta_manifest.csv"
manifestfile = "beta_manifest_mini.csv"

# -----------
# DEFINITIONS
# -----------

# projects to add subjects to
proj = {'simple':'Season Spotter Questions',
        'complex':'Season Spotter Image Marking'}

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

# ---
# Create and upload the subjects
# ---
def create_subjects(projids,token):

    # create a dictionary of which project to use for each subject set
    ssproj = {}
    with open(linkfile,'r') as lfile:
        
        # discard header
        lfile.readline()

        # go through each line and add to dictionary
        lreader = csv.reader(lfile,delimiter=',',quotechar='\"')
        for row in lreader:
            ssproj[row[1]] = projids[0]
            if row[2]=="complex":
                ssproj[row[1]] = projids[1]
    
    # read the manifest
    with open(manifestfile,'r') as mfile:

        # discard header and get csv object
        mfile.readline()
    
        # for each image
        mreader = csv.reader(mfile,delimiter=',',quotechar='\"')
        for row in mreader:
            image = row[0]
            subjset = row[1]
            site = row[2]
            vegabbr = row[3]
            loc = row[4]
            lat = row[5]
            lon = row[6]
            ele = row[7]

            # get just the image name
            imagename = image.split('/')[-1]

            # look up the vegetation type
            if vegabbr in veg_lookup:
                vegtype = veg_lookup[vegabbr]
            else:
                vegtype = vegabbr

            # check to see if the subject set(s) exists; error if not
            subjsetnum = panoptesPythonAPI.get_subject_set(ssproj[subjset],subjset,token)
            if subjsetnum == -1:
                print "SubjectSet " + subjset + " does not exist. Subject " + imagename + " not uploaded."

            else:
                # create the metadata object
                meta = """ "Filename": \"""" + imagename + """\",
                           "Camera": \"""" + site + """\",
                           "Location": \"""" + loc + """\",
                           "Vegetation": \"""" + vegtype + """\",
                           "Latitute": \"""" + lat + """\",
                           "Longitude": \"""" + lon + """\",
                           "Elevation": \"""" + ele + """\" """

                # create the subject
                print "Adding Subject: " + image
                subjid = panoptesPythonAPI.create_subject(ssproj[subjset],meta,image,token)

                # add it to the subject set(s)
                print "Linking Subject " + image + " to Subject Set " + subjset
                panoptesPythonAPI.add_subject_to_subject_set(subjsetnum,subjid,token)
        
    return


########
# MAIN #
########

# get token
with open(auth,'r') as authfile:
    areader = csv.reader(authfile,delimiter=',')
    row = areader.next()
    username = row[0]
    password = row[1]

token = panoptesPythonAPI.get_bearer_token(username,password)

# get project IDs
projid_simp = panoptesPythonAPI.get_projectid_from_projectname(proj['simple'],username,token)
if projid_simp==-1:
    print "Could not find project " + proj['simple'] + ". No subjects uploaded."
    exit(0)

projid_comp = panoptesPythonAPI.get_projectid_from_projectname(proj['complex'],username,token)
if projid_comp==-1:
    print "Could not find project " + proj['complex'] + ". No subjects uploaded."
    exit(0)

# put the project ids together
projids = (projid_simp,projid_comp)

# create and upload the subjects
create_subjects(projids,token)

