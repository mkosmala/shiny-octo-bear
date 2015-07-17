#!/usr/bin/python

import panoptesPythonAPI
import csv
import os
import json

# This only needs to create workflows and (empty) subject sets.
# Most of the rest can easily be done from the Project Builder now.
# Subject uploads will be done in a separate script.

# ------------------
# FILES WITH CONTENT
# ------------------

linkfile = "subjectsets_and_workflows.csv"
workflow_dir = "workflows/"
auth = "authentication.txt"


# ------------------------------
# PROJECT NAME AND COLLABORATORS
# ------------------------------

project_simple = "Season Spotter Questions"
project_complex = "Season Spotter Image Marking"


#---
# Create the workflows
#---
def create_workflows(projids,token):
    #workflows = os.listdir(workflow_dir)
    with open(linkfile,'r') as lfile:

        # discard header
        lfile.readline()

        # keep track of workflows already done
        donewf = []

        # go through each line
        lreader = csv.reader(lfile,delimiter=',',quotechar='\"')
        for row in lreader:

            wfname = row[0]
            wfset = row[2]

            # do new workflows
            if wfname not in donewf:

                wf_path = workflow_dir + wfname + ".txt"
                with open(wf_path,'r') as wffile:
                    workflow = wffile.read().replace('\n', '')

                # add this workflow to the correct project
                wfproj = projids[0]
                if wfset == "complex":
                    wfproj = projids[1]
                        
                # and build it
                print "Building workflow " + wfname + " in project " + wfproj
                wfid = panoptesPythonAPI.create_workflow(wfproj,wfname,workflow,token)
                print "   ID: " + wfid

                # record that we've done this workflow
                donewf.append(wfname)

    return
    


# ---
# Create subject sets and link to workflows
# ---
def create_subject_sets(projids,token):

    with open(linkfile,'r') as lfile:
        
        # discard header
        lfile.readline()
        lreader = csv.reader(lfile,delimiter=',',quotechar='\"')

        # for each subject set 
        for row in lreader:
            
            # get the correct project
            proj = projids[0]
            if row[2]=="complex":
                proj = projids[1]

            # get the subject set and workflow names
            subjset = row[1]
            workflow = row[0]

            # check to see if the subject set(s) exists; create it if not
            ssid = panoptesPythonAPI.get_subject_set(proj,subjset,token)
            if ssid == -1:
                print "Building SubjectSet: " + subjset
                ssid = panoptesPythonAPI.create_empty_subject_set(proj,subjset,token)
                print "   ID: " + ssid
                     
            # get the workflow id
            wfid = panoptesPythonAPI.get_workflow(proj,workflow,token)

            # and link
            print "Linking subject set " + subjset + " to workflow " + workflow
            panoptesPythonAPI.link_subject_set_and_workflow(ssid,wfid,token)

    return


# ---
# Build a bare-bones project
# ---
def build_project_info(projtype):

    info = {}
    
    # simple
    if projtype == "simple":        
        info["display_name"] = project_simple

    # complex
    else:
        info["display_name"] = project_complex

    info["description"] = "default description"
    #info["primary_language"] = "en-us"
    info["primary_language"] = "en"
    info["private"] = False

    return info


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

# create a project for simple workflows
# check to see if it's already created. if not, create it
projid_simp = panoptesPythonAPI.get_projectid_from_projectname(project_simple,username,token)
if projid_simp==-1:
    print "Creating project: " + project_simple
    project_info = build_project_info("simple")
    projid_simp = panoptesPythonAPI.create_user_project(project_info,token)
else:
    print "Project already exists: " + project_simple
    exit(0)    
print "   ID: " + projid_simp

# create a project for complex workflows
# check to see if it's already created. if not, create it
projid_comp = panoptesPythonAPI.get_projectid_from_projectname(project_complex,username,token)
if projid_comp==-1:
    print "Creating project: " + project_complex
    project_info = build_project_info("complex")
    projid_comp = panoptesPythonAPI.create_user_project(project_info,token)
else:
    print "Project already exists: " + project_complex
    exit(0)    
print "   ID: " + projid_comp

# put the project ids together
projids = (projid_simp,projid_comp)

# add workflows
create_workflows(projids,token)

# add subject sets and link them to workflows
create_subject_sets(projids,token)

