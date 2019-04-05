#!/usr/bin/python
# Set dates for the weekly threads
from datetime import date, timedelta
from pprint import pprint
from re import sub
import argparse
import json

thread_template = 'template'
wk1_start = date(2019, 3, 12)  # TUESDAY

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help="Schedule file to read")
parser.add_argument('-y', '--year', help="Year", type=int, default=2019)
parser.add_argument('-s', '--season', help="Season", type=int, default=2)
parser.add_argument('-b', '--begin_week', help="Week to begin at", type=int, default=1)
parser.add_argument('-e', '--end_week', help="Week to end at", type=int, default=12)
parser.add_argument('-o', '--output_dir', help="Directory to write files into")

args = parser.parse_args()

if not args.output_dir:
    args.output_dir = './{}s{}'.format(args.year, args.season)

print("Active options:")
pprint(args)

with open("schedules/{}s{}-schedule.json".format(args.year, args.season), 'r') as f:
    schedule = json.load(f)
    for week in schedule['weeks']:
        print("Found schedule wk", week['week'], '@', week['track_name'], week['track_layout'])

exit()

# Read the thread template
with open(thread_template, 'r') as f:
    template_str = f.read()

for i in range(args.begin_week, args.end_week + 1):
    week_file = template_str

    # Get track data and sub it in
    notes = 0
    with open("data/tracks_json/%s" % schedule[i], 'r') as tr_file:

        for line in tr_file.readlines():

            if notes == 0:
                # print(line)
                (tag, value) = line.strip().split(' : ')
                # print ("Found tag: %s with value: %s" % (tag, value))
                if tag == "TRACK_NOTES":
                    notes = 1
                else:
                    week_file = sub("#%s#" % tag, value, week_file)
            else:
                week_file = sub("(?=#TRACK_NOTES#)", line, week_file)
    week_file = sub("#TRACK_NOTES#", '', week_file)

    # set up dates for the week
    wk_start = wk1_start + (i - 1) * timedelta(7)
    mon_before = wk_start - timedelta(1)
    sun_before = wk_start - timedelta(2)
    sat_follow = wk_start + timedelta(4)
    sun_follow = wk_start + timedelta(5)

    # week_file = sub("#SATURDAY_TRACK#",  			saturdays[i], week_file)
    week_file = sub("#DATE_MON_BEFORE#", mon_before.isoformat(), week_file)
    # week_file = sub("#DATE_SAT_FOLLOW#", sat_follow.isoformat(), week_file)
    week_file = sub("#DATE_SUN_BEFORE#", sun_before.isoformat(), week_file)
    week_file = sub("#DATE_SUN_FOLLOW#", sun_follow.isoformat(), week_file)
    week_file = sub("#YEAR#", str(args.year), week_file)
    week_file = sub("#SEASON#", str(args.season), week_file)
    # N.B. preamble sub required BEFORE this line!
    week_file = sub("#WEEK_NUM#", str(i), week_file)

    output_name = "{}/{}s{}w{:02} - {}".format(args.output_dir, args.year, args.season, i, schedule[i])
    with open(output_name, 'w') as output_file:
        output_file.write(week_file)
        print("Wrote %s" % output_name)
