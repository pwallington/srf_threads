#!/usr/bin/python
# Set dates for the weekly threads
from datetime import date, timedelta
from pprint import pprint
import argparse
import json

track_tags = ["TRACK_SHORT_NAME", "TRACK_LONG_NAME", "TRACK_BANNER_IMG", "TRACK_MAP_IMG", "WR_LAP_TIME",
              "WR_DRIVER", "GUIDE_VIDEO_1", "GUIDE_VIDEO_2", "DEMO_VIDEO_1", "DEMO_VIDEO_2", "PREAMBLE", "TRACK_NOTES"]
week_tags = ["RACE_LENGTH"]

thread_template = 'template'

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

# Read the thread template
with open(thread_template, 'r') as f:
    template_str = f.read()

with open("schedules/{}s{}-schedule.json".format(args.year, args.season), 'r') as f:
    schedule = json.load(f)
    for week in schedule['weeks']:
        print("Found schedule wk", week['week'], '@', week['track_name'], week['track_layout'])
        if not (args.begin_week <= week['week'] <= args.end_week):
            print(" * Skipping")
            continue

        try:
            # Get track data
            track_spec = week['track_name'].replace(" ", "")
            if week['track_layout']:
                track_spec += ':' + week['track_layout'].replace(" ", "")
            track_file = './data/tracks_json/' + track_spec + '.json'
            with open(track_file, 'r') as tr_file:
                print(" * Loading track data file", track_file)
                tr_data = json.load(tr_file)
        except Exception:
            print(" * Error loading track data")
            continue

        week_file = template_str
        # Sub tag data into the template
        for tag in track_tags:
            week_file = week_file.replace("#%s#" % tag, tr_data[tag])
        for tag in week_tags:
            week_file = week_file.replace("#%s#" % tag, week[tag.lower()])

        # set up dates for the week
        import datetime
        wk_start = datetime.date.fromisoformat(week['start_date'])
        mon_before = wk_start - timedelta(1)
        sun_before = wk_start - timedelta(2)
        sat_follow = wk_start + timedelta(4)
        sun_follow = wk_start + timedelta(5)

        # sub in dates
        week_file = week_file.replace("#DATE_MON_BEFORE#", mon_before.isoformat())
        week_file = week_file.replace("#DATE_SUN_BEFORE#", sun_before.isoformat())
        week_file = week_file.replace("#DATE_SUN_FOLLOW#", sun_follow.isoformat())
        week_file = week_file.replace("#YEAR#", str(args.year))
        week_file = week_file.replace("#SEASON#", str(args.season))
        # N.B. preamble week_file.replace required BEFORE this line!
        week_file = week_file.replace("#WEEK_NUM#", str(week['week']))

        output_name = "{}/{}s{}w{:02} - {}".format(args.output_dir, args.year, args.season, week['week'], track_spec)
        with open(output_name, 'w') as output_file:
            output_file.write(week_file)

            print(" * Wrote %s" % output_name)

            import requests
            try:
                vrs = requests.get("https://virtualracingschool.appspot.com/datapacksInfo/forumCode?id=224830001&week="+str(week['week']))
                vrs.raise_for_status()
                output_file.write("\n\n\n#####################\n\n\n\n")
                output_file.write("VRS INFO:\n\n")
                output_file.write(vrs.text)
                print(" * Got VRS info")
            except Exception:
                print(" * Error getting VRS info")
