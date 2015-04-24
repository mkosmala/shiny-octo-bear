#!/usr/bin/env python
"""
script to create a yearly image using a single column from the
midday images from a particular site.

"""

import os, sys
import glob
from math import fabs
import datetime
import time
#from datetime import datetime, date, timedelta
from PIL import Image
import PIL.ImageOps
import numpy as np
import calendar
#import PhenoCamUtils as pcu
import matplotlib.pyplot as plt
import argparse

###############################################################################

def date2doy(year, month, day):
    """
    Convert calendar date into year and yearday.
    """
    year=int(year)
    month=int(month)
    day=int(day)
    thedate = datetime.date(year, month, day)
    return (year, thedate.timetuple()[7])


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
    toret = datetime.datetime(year, mon, day, hour, mins, sec)
    return toret

##################################################################################################

def getFirstImagePath(sitename, path, irFlag=False):
    """
    Find date of first image file for this site.

    irFlag just uses pattern matching ... could do a database check as
    well to verify that this camera has IR capability.  NOTE: need
    routine to get dbinfo for single site!
    """

    sitepath=os.path.join(path,sitename)

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

def getLastImagePath(sitename, path, irFlag=False):
    """
    Find date of first image file for this site.

    irFlag just uses pattern matching ... could do a database check as
    well to verify that this camera has IR capability.  NOTE: need
    routine to get dbinfo for single site!
    """

    sitepath=os.path.join(path,sitename)

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

def getDayImageList(sitename,year,month,day,path,irFlag=False):
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
    imdir = os.path.join(path,sitename,yrstr,mostr)
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

def getMiddayImage(sitename,year,month,day,path,irFlag=False):
    """
    Get the list of images for a particular day and return the
    one closest to midday.
    """
    
    imlist = getDayImageList(sitename, year, month, day, path, irFlag=irFlag)

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

def getMidDayImageList(sitename, path, irFlag=False):
    """
    Get List of Mid-day images for this site.
    """

    midDayList=[]

    # get date of first image
    firstPath = getFirstImagePath(sitename, path, irFlag=irFlag)
    firstDT = fn2datetime(sitename, os.path.basename(firstPath),irFlag=irFlag)
    firstDate = firstDT.date()
    
    # get last image path
    lastPath = getLastImagePath(sitename, path, irFlag=irFlag)
    lastDT = fn2datetime(sitename,os.path.basename(lastPath),irFlag=irFlag)
    lastDate = lastDT.date()

    # for each date get the mid-day image
    myDate=firstDate
    while myDate <= lastDate:
        year = myDate.year
        month = myDate.month
        day = myDate.day
        middayimg = getMiddayImage(sitename,year,month,day,path,irFlag=irFlag);

        midDayList.append(middayimg)
        
        myDate = myDate + datetime.timedelta(days=1)

    return midDayList


def resize_image(img):
    imagewidth = img.size[0]
    imageheight = img.size[1]

    # check sizing
    # calculate aspect ratio
    aspect = float(imagewidth)/float(imageheight)
    resize = False
    # normal, square, or tall&skinny
    if aspect<=1.35 and imageheight>600:
        newheight=600
        newwidth=int(600*float(imagewidth)/float(imageheight))
        resize = True
    # wide
    elif imagewidth>720:
        newwidth=720
        newheight=int(720*float(imageheight)/float(imagewidth))
        resize = True

    # resize image if necessary
    if resize:
        ready_image = img.resize((newwidth,newheight),PIL.Image.ANTIALIAS)
    else:
        ready_image = img

    return ready_image    




# --- MAIN ---

# set up argument processing
#parser = argparse.ArgumentParser()
#parser.add_argument("-v","--verbose",
#                    help="increase output verbosity",
#                    action="store_true",
#                    default=False)
#parser.add_argument("-c","--centerline",
#                    type=int,
#                    help="center line/column from image",
#                    default=None)

# positional arguments
#parser.add_argument("site",help="phenocam site name")
#parser.add_argument("year",help="year",type=int)

#args = parser.parse_args()


def create_one_slice(sitename,outyear,imagesdir,outslicedir):

    verbose = False
    
    cl_col = None
    #if args.centerline:
    #    cl_col = args.centerline

    if verbose:
        print "site: {0}".format(sitename)
        print "year: {0}".format(outyear)
        if cl_col:
            print "column: {0}".format(cl_col)

    # get list of midday images for this site
    imglist = getMidDayImageList(sitename,imagesdir,irFlag=False)

    # set up yearly images
    nimage = len(imglist)
    img_first = imglist[0]
    fn_first = os.path.basename(img_first)
    dt_first = fn2datetime(sitename,fn_first)
    yr_first = dt_first.year

    img_last = imglist[nimage-1]
    fn_last = os.path.basename(img_last)
    dt_last = fn2datetime(sitename,fn_last)
    yr_last = dt_last.year

    # check requested year
    if (outyear < yr_first) or (outyear > yr_last):
        sys.stderr.write("no data for requested year: "+sitename+","+
                         str(outyear)+"\n")
        #sys.exit(1)
        return

    # figure out number of days in this year
    ndays_td = datetime.datetime(outyear+1, 1, 1, 0, 0, 0) - \
               datetime.datetime(outyear, 1, 1, 0, 0, 0)
    ndays = ndays_td.days

    # open output file for keeping track of doys with images
    outtxt_dir = outslicedir
    outtxt_name = "{0}_{1}_slice.txt".format(sitename, outyear)
    outtxt_path = os.path.join(outtxt_dir,outtxt_name)
    textout = open(outtxt_path,'w')

    # initialize image height
    nrow = 0

    # set up counter for this year
    icount = 0
    for imgpath in imglist:

        # imglist has a blank path for missing days
        if imgpath == '':
            continue

        # get image date info
        imgfile = os.path.basename(imgpath)
        imgdt = fn2datetime(sitename,imgfile)
        imgdate = imgdt.date()

        imgdoy = date2doy(imgdate.year, imgdate.month, imgdate.day)
        imgyear = imgdate.year

        # only look at this year's images
        if imgyear < outyear:
            continue
        elif imgyear > outyear:
            break

        # try to read in image
        try: 
            img = Image.open(imgpath)
            img.load()
        except:
            errstr1 = "Unable to open file: {0}\n".format(imgpath)
            errstr2 = "Skipping this file.\n"
            sys.stderr.write(errstr1)
            sys.stderr.write(errstr2)
            continue

        # initialize some things if this is the first image
        # we could read.
        if icount == 0:

            # ncol, nrow are the dimensions of this image
            [ncol, nrow] = img.size

            if verbose:
                print "first image: {0}".format(imgpath)
                print "size: {0} x {1}".format(ncol, nrow)

            
            # if cl_col is not set use middle of image
            if not cl_col:
                cl_col = int(float(ncol)/2.)
            
            # check that requested cl_col is within range
            if (cl_col < 0) or (cl_col > ncol):
                sys.stderr.write("requested centerline is out of range\n")
                sys.exit(1)

            # initialize output array 
            # Make it 4 pixels wide per day
            outarr = np.zeros((nrow, ndays*4, 3),dtype=np.int8)
            #outarr[0:nrow, 0:ncol, :] = (100, 0, 0)
        
        icount += 1

        # write doy to the text file
        textout.write(str(imgdoy[1])+"\n")

        # check if size has changed
        [nc, nr] = img.size
        if (nr != nrow) or (nc != ncol):
            sys.stderr.write("Warning: image size changed.\n")
        
        # read in 
        imarr = np.asarray(img)

        # make sure cl_col is still valid
        if cl_col > nc:
            # use mid column of this image
            midcol = nc/2
            colarr = imarr[:,midcol,:]
        else:
            colarr = imarr[:,cl_col,:]

        # insert column into output array
        #column_index = imgdoy[1]-1
        column_index = icount-1
        if nr < nrow:
            rowdiff = nrow - nr
            rowstart = rowdiff
            outarr[rowstart:nrow,column_index*4,:]=colarr[:,:]
            outarr[rowstart:nrow,column_index*4+1,:]=colarr[:,:]
            outarr[rowstart:nrow,column_index*4+2,:]=colarr[:,:]
            outarr[rowstart:nrow,column_index*4+3,:]=colarr[:,:]

        elif nr > nrow:
            rowdiff = nr - nrow
            rowstart = rowdiff
            outarr[:,column_index*4,:] = colarr[rowstart:nr+1,:]
            outarr[:,column_index*4+1,:] = colarr[rowstart:nr+1,:]
            outarr[:,column_index*4+2,:] = colarr[rowstart:nr+1,:]
            outarr[:,column_index*4+3,:] = colarr[rowstart:nr+1,:]

        else:
            outarr[0:nrow,column_index*4,:]=colarr[:,:]
            outarr[0:nrow,column_index*4+1,:]=colarr[:,:]
            outarr[0:nrow,column_index*4+2,:]=colarr[:,:]
            outarr[0:nrow,column_index*4+3,:]=colarr[:,:]

    # crop out the days that didn't have images
    #croparr = np.zeros((nrow, icount*4, 3),dtype=np.int8)
    croparr = outarr[0:nrow,0:icount*4,:]

    # make output image
    origimg = Image.fromarray(croparr,'RGB')

    # resize if necessary
    outimg = resize_image(origimg)

    # save this image
    #outimg_dir = os.path.join(STARTDIR,sitename,'ROI')
    outimg_dir = outslicedir
    outimg_name = "{0}_{1}_slice.png".format(sitename, outyear)
    outimg_path = os.path.join(outimg_dir,outimg_name)
    outimg.save(outimg_path)

    # close the text file
    textout.close()

    return

# okay stretch image so that x-axis is longer
# this is the time axis ...
#img_wide = outimg.resize((ndays*3,nrow/2), Image.NEAREST)

# set up tick marks and labels on month boundaries
#new_tick_locs = []
#new_tick_labels = []
#for imonth in range(1,13,1):
#    new_tick_locs.append(date2doy(outyear, imonth, 1)[1])
#    new_tick_labels.append(calendar.month_abbr[imonth])

# make figure with this image
#fig = plt.figure(figsize=(11,6))
#plt.imshow(img_wide,extent=[1,ndays,1,nrow],aspect=.2)
#xtics = plt.xticks(new_tick_locs, new_tick_labels)
#ax1 = plt.gca()
#ax1.xaxis.set_tick_params(direction='out')
# plt.grid(color='y',linewidth=1, linestyle='--')
#plt.xlabel('{0}'.format(outyear))
#plt.title('site: {0}  image size: {1}x{2}  cl_col: {3}'.format(sitename, 
#                                                nrow, ncol, cl_col))
# save figure to PNG file
#outname = '{0}_{1}_ci.png'.format(sitename, outyear)
#outpath = os.path.join(outimg_dir,outname)
#plt.savefig(outpath, orientation='landscape',dpi=150,transparent=True)



