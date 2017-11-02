#!/usr/bin/python
# Set dates for the weekly threads
from datetime import date, timedelta
from re import sub
import sys

thread_template = '../template'
year = 2017
season = 4
startweek = 1
endweek = 12
wk1_start = date(2017, 9, 12)

if (len(sys.argv) >= 2):
	year = int(sys.argv[1])
if (len(sys.argv) >= 3):
	season = int(sys.argv[2])
if (len(sys.argv) >= 4):
	startweek = int(sys.argv[3])
if (len(sys.argv) >= 5):
	endweek = int(sys.argv[4])

schedule = {}
with open("../{}s{}-schedule.txt".format(year, season), 'r') as f: 
	for line in f.readlines():
		print(line,)
		(num, track) = line.strip().split(' : ')
		# print ("Found schedule wk %s @ %s" % (num, track))
		schedule[int(num)] = track

# saturdays = {}
# with open("../{}s{}-saturdays.txt".format(year, season), 'r') as f: 
# 	for line in f.readlines():
# 		(num, track) = line.strip().split(' : ')
# 		# print ("Found saturdays wk %s @ %s" % (num, track))
# 		saturdays[int(num)] = track


# Read the thread template
with open(thread_template, 'r') as f: template_str = f.read()

for i in range (startweek, endweek+1):
	wkfile = template_str

	# Get track data and sub it in
	notes = 0
	with open("../data/%s" % schedule[i], 'r') as tr_file: 
		for line in tr_file.readlines():
				
				if (notes == 0):
					print(line,)
					(tag, value) = line.strip().split(' : ')
					# print ("Found tag: %s with value: %s" % (tag, value))
					if (tag == "TRACK_NOTES"):
						notes = 1
					else:
						wkfile = sub("#%s#" % tag, value, wkfile)
				else:
					wkfile = sub("(?=#TRACK_NOTES#)", line, wkfile)
	wkfile = sub("#TRACK_NOTES#", '', wkfile)

	# set up dates for the week
	wk_start = wk1_start+(i-1)*timedelta(7)
	mon_before = wk_start - timedelta(1)
	sun_before = wk_start - timedelta(2)
	sat_follow = wk_start + timedelta(4)
	sun_follow = wk_start + timedelta(5)

	# wkfile = sub("#SATURDAY_TRACK#",  			saturdays[i], wkfile)
	wkfile = sub("#DATE_MON_BEFORE#", mon_before.isoformat(), wkfile)
	# wkfile = sub("#DATE_SAT_FOLLOW#", sat_follow.isoformat(), wkfile)
	wkfile = sub("#DATE_SUN_BEFORE#", sun_before.isoformat(), wkfile)
	wkfile = sub("#DATE_SUN_FOLLOW#", sun_follow.isoformat(), wkfile)
	wkfile = sub(			"#YEAR#", 			   str(year), wkfile)
	wkfile = sub(		  "#SEASON#", 			 str(season), wkfile)
	# N.B. preamble sub required BEFORE this line!
	wkfile = sub(		"#WEEK_NUM#", 				  str(i), wkfile)

	output_name = "{}s{}w{:02} - {}".format(year, season, i, schedule[i])
	with open(output_name, 'w') as outputfile :
		outputfile.write(wkfile)
		print ("Wrote %s" % output_name)





