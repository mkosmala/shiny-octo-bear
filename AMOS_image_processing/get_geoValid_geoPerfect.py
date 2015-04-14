import json
import urllib2
import datetime

tags = ['geoValid','geoPerfect']
cams = []

# fetch all geoValid and/or geoPerfect cameras
for tag in tags:
    fetching_data = True
    currURL = 'http://amos.cse.wustl.edu/REST/tags/.json?page_size=5000&tag='+tag
    while fetching_data:
        print 'fetching tag data from',currURL
        tag_data = json.load(urllib2.urlopen(currURL))

        for t in tag_data['results']:
            print 'fetching camera from',t['webcam']
            webcam_data = json.load(urllib2.urlopen(t['webcam']))
            webcam_data['tag'] = tag
            cams.append(webcam_data)

        if tag_data['next']:
            '...next page!'
            currURL = tag_data['next']
        else:
            fetching_data = False

# nicely format the data and print it out
output = open('geoValid_geoPerfect_cams.txt','w')
output.write('tag,id,latitude,longitude,start_date,end_date\n')

for cam in cams:
    # use the years_captured and days_since_captured fields to compute start_date and end_date
    now = datetime.datetime.now()
    start_date = now - datetime.timedelta(days=cam['years_captured']*365.0)
    end_date = now - datetime.timedelta(days=cam['days_since_captured'])

    # note: casting lat/lon to str in case they are None
    output_line = '%s,%d,%s,%s,%s,%s\n'%(cam['tag'],cam['id'],str(cam['latitude']),str(cam['longitude']),start_date,end_date)
    output.write(output_line)

output.close()