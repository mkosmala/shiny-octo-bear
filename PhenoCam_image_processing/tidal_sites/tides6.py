import csv 
import datetime
from datetime import timedelta

def process_line(line):
	date, time, sunrise, sunset, height, tidebetween =line ###extracts the important values
	date2=datetime.datetime.strptime(date, "%m/%d/%y")
	time2=datetime.datetime.strptime(time, "%H:%M")
	sunrise2=datetime.datetime.strptime(sunrise, "%H:%M")
	sunset2=datetime.datetime.strptime(sunset, "%H:%M") ###changes dates and times into datetimes
	daylength=sunset2-sunrise2
	halfday=daylength//2
	noon=sunrise2+halfday ###defines the midpoint between sunrise and sunset on each day 
	return (date2, time2, noon, sunrise2, sunset2) 

reader=csv.reader(open("gcesapelo_lowtides.csv", "rbU")) ###reads in the tide files 
tides=[process_line(line) for line in reader] ###puts all the information in a list instead of in a file. can look at multiple at once 
	
first=tides[0][0]
last=tides[-1][0]

day=first ###the date for the first low tide
i=0 ###the index for the first low tide
while day<=last: ###for all the dates in the tides matrix
	if day!=tides[i][0]: ###that is, if there is no tide for that day
		print "wrong number of low tides for", day ###prints an error message for the appropriate date
		day=day+timedelta(days=1)

	else:
		if len(tides)>i+1 and tides[i][0]==tides[i+1][0]: ###that is, if there are two lowtides for a particular date
			###defines variables so I can use my previous program
			time2even=tides[i][1] ###is there a way to refer to variables in my matrix using their "names"?
			nooneven=tides[i][2]
			sunrise2even=tides[i][3]
			sunset2even=tides[i][4]
			time2odd=tides[i+1][1] 
			noonodd=tides[i+1][2]
			sunrise2odd=tides[i+1][3]
			sunset2odd=tides[i+1][4]

			###chooses the lowtide closest to noon
			if abs(time2even-nooneven)>abs(time2odd-noonodd):
				Time2=time2odd
				Sunrise2=sunrise2odd
				Sunset2=sunset2odd
				Noon=noonodd	
			else:
				Time2=time2even
				Sunrise2=sunrise2even
				Sunset2=sunset2even
				Noon=nooneven

			###adjusts the lowtide time closest to noon through a series of averages
			while Time2<Sunrise2+timedelta(hours=3) or Time2>Sunset2-timedelta(hours=3): 
				length=Noon-Time2
				halflength=length/2
				Time2=Time2+halflength
			print tides[i][0], Time2 ###prints the date and the adjusted lowtidetime

			day=day+timedelta(days=1)###moves to the next day
			i=i+2 ###moves to the row for the next day

		else: ###that is, if there is only one lowtide for a particular day
			###defines the appropriate values of the row of tides so I can use my previous algorithm
			Time2=tides[i][1] ###is there a way to refer to variables in my fake matrix using their "names"?
			Noon=tides[i][2]
			Sunrise2=tides[i][3]
			Sunset2=tides[i][4]

			###pushes the low tide time to sunny hours
			while Time2<Sunrise2+timedelta(hours=3) or Time2>Sunset2-timedelta(hours=3): 
				length=Noon-Time2
				halflength=length/2
				Time2=Time2+halflength
			print tides[i][0], Time2 ###prints the date and adjusted lowtidetime

			day=day+timedelta(days=1)###moves on to the next day
			i=i+1
