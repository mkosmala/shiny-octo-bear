#!/usr/bin/env python

import sys, os
import glob
from math import fabs
import  argparse
import datetime
import time

STARTDIR = "/data/archive"

##########################################################################################

def fn2date(sitename, filename, irFlag=False):
    """
    Function to extract the date from a "standard" filename based on a
    sitename.  Here we assume the filename format is the standard:

          sitename_YYYY_MM_DD_HHNNSS.jpg

    So we just grab components from fixed positions.  If irFlag is 
    True then the "standard" format is:

          sitename_IR_YYYY_MM_DD_HHNNSS.jpg

    """    
    
    if irFlag:
        prefix=sitename+"_IR"
    else:
        prefix=sitename

    # set start of datetime part of name
    nstart=len(prefix)+1
    
    # assume 3-letter extension e.g. ".jpg"
    dtstring=filename[nstart:-4]
    
    # extract date-time pieces
    try:
        year=int(dtstring[0:4])
        mon=int(dtstring[5:7])
        day=int(dtstring[8:10])
        hour=int(dtstring[11:13])
        mins=int(dtstring[13:15])
        sec=int(dtstring[15:17])
    except ValueError:
        print "Error extracting date from: {0}".format(filename)
        return None
    
    # return list
    return [year, mon, day, hour, mins, sec]

def fn2datetime(sitename, filename, irFlag=False):
    """
    Function to extract the date from a "standard" filename based on a
    sitename.  Here we assume the filename format is the standard:

          sitename_YYYY_MM_DD_HHNNSS.jpg

    So we just grab components from fixed positions.  If irFlag is 
    True then the "standard" format is:

          sitename_IR_YYYY_MM_DD_HHNNSS.jpg

    """    
    
    if irFlag:
        prefix=sitename+"_IR"
    else:
        prefix=sitename

    # set start of datetime part of name
    nstart=len(prefix)+1
    
    # assume 3-letter extension e.g. ".jpg"
    dtstring=filename[nstart:-4]
    
    # extract date-time pieces
    try:
        year=int(dtstring[0:4])
        mon=int(dtstring[5:7])
        day=int(dtstring[8:10])
        hour=int(dtstring[11:13])
        mins=int(dtstring[13:15])
        sec=int(dtstring[15:17])
    except ValueError:
        print "Error extracting datetime from: {0}".format(filename)
        return None
    
    # return list
    return datetime.datetime(year, mon, day, hour, mins, sec)

##################################################################################################

def getFirstImagePath(sitename, irFlag=False):
    """
    Find date of first image file for this site.

    irFlag just uses pattern matching ... could do a database check as
    well to verify that this camera has IR capability.  NOTE: need
    routine to get dbinfo for single site!
    """

    sitepath=os.path.join(STARTDIR,sitename)

    if irFlag:
        sitename = sitename + '_IR'

    pattern = "%s/[12][0-9][0-9][0-9]/[01][0-9]/%s_[12]*.jpg" % (sitepath,sitename,)
    imglist = glob.glob(pattern)
    imglist.sort()
    nimages = len(imglist)

    if nimages > 0:
        first_img = imglist[0]
    else:
        first_img = ""

    return first_img

##################################################################################################

def getLastImagePath(sitename, irFlag=False):
    """
    Find date of first image file for this site.

    irFlag just uses pattern matching ... could do a database check as
    well to verify that this camera has IR capability.  NOTE: need
    routine to get dbinfo for single site!
    """

    sitepath=os.path.join(STARTDIR,sitename)

    if irFlag:
        sitename = sitename + '_IR'
    pattern = "%s/[12][0-9][0-9][0-9]/[01][0-9]/%s_[12]*.jpg" % (sitepath,sitename,)

    imglist = glob.glob(pattern)
    imglist.sort()
    nimages = len(imglist)

    if nimages > 0:
        last_img = imglist[nimages-1]
    else:
        last_img = ""

    return last_img

##################################################################################################

def getDayImageList(sitename,year,month,day,irFlag=False):
    """
    Given a site, year, month and day return a list of archive image
    paths. If irFlag is True then get the IR images only.  We're just
    doing simple filename matching so if irFlag is True and this is
    not an IR camera an empty list will be returned.
    """
    
    # flag for debugging
    dbgFlg=False

    # need this to allow for uppercase letters in the site name
    namelen = len(sitename)

    # initialize a list of paths to return
    imgpaths = []
    
    # set path base
    yrstr="%2.2d" % (year,)
    mostr="%2.2d" % (month,)
    imdir = os.path.join(STARTDIR,sitename,yrstr,mostr)
    if dbgFlg:
        print "imdir: " + imdir
    
    # if image dir doesn't exist return empty list
    if not os.path.exists(imdir) :
        return imgpaths

    # grab filenames matching pattern
    if irFlag:
        fnpattern = '%s_IR_%4.4d_%2.2d_%2.2d_??????.jpg' % (sitename, year, month, day,)
    else:
        fnpattern = '%s_%4.4d_%2.2d_%2.2d_??????.jpg' % (sitename, year, month, day,)

    pattern = os.path.join(imdir,fnpattern)
    imlist = glob.glob(pattern)

    # sort list by time
    imlist.sort()
    
    return imlist

##################################################################################################

def getMiddayImage(sitename,year,month,day,irFlag=False):
    """
    Get the list of images for a particular day and return the
    one closest to midday.
    """
    
    imlist = getDayImageList(sitename, year, month, day, irFlag=irFlag)

    # check for empty list
    if len(imlist) == 0:
        return ""
    
    tmlist = []

    for impath in imlist:
        fname = os.path.basename(impath)
        date = fn2date(sitename,fname,irFlag=irFlag)
        hour = date[3] + date[4]/60. + date[5]/3600.
        fromnoon = fabs(hour - 12.)
        tmlist.append((fromnoon, impath,))

    # find one with lowest time
    sorted_tmlist = sorted(tmlist)

    return sorted_tmlist[0][1]

##################################################################################################

def getMidDayImageList(sitename, irFlag=False):
    """
    Get List of Mid-day images for this site.
    """

    midDayList=[]

    # get date of first image
    firstPath = getFirstImagePath(sitename, irFlag=irFlag)
    firstDT = fn2datetime(sitename, os.path.basename(firstPath),irFlag=irFlag)
    firstDate = firstDT.date()
    
    # get last image path
    lastPath = getLastImagePath(sitename, irFlag=irFlag)
    lastDT = fn2datetime(sitename,os.path.basename(lastPath),irFlag=irFlag)
    lastDate = lastDT.date()

    # for each date get the mid-day image
    myDate=firstDate
    while myDate <= lastDate:
        year = myDate.year
        month = myDate.month
        day = myDate.day
        middayimg = getMiddayImage(sitename,year,month,day,irFlag=irFlag);

        midDayList.append(middayimg)
        
        myDate = myDate + datetime.timedelta(days=1)

    return midDayList


if __name__ == "__main__":

    """
    As a test of the functions above create a list of the
    midday images for a site.
    """
    
    parser = argparse.ArgumentParser()
    parser.add_argument("sitename",help="phenocam site name")
    parser.add_argument("-v","--verbose",help="verbose output",
                    action="store_true")

    args = parser.parse_args()

    verbose=args.verbose
    sitename=args.sitename
    
    if verbose:
        print "Site name: {0}".format(sitename)
        print "Archive Directory: {0}".format(STARTDIR)

    # 
    # get midday images for this site
    mdimglist = getMidDayImageList(sitename,irFlag=False)
    mdlistlen = len(mdimglist)
    
    for i, img in enumerate(mdimglist):
        if img != "":
            print img


