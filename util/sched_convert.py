#!/usr/bin/python

import json
import glob

for file_name in glob.glob('../*schedule.txt'):
    print(file_name)
    schedule = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            (num, track) = line.strip().split(' : ')
            schedule.append(track)
    print(json.dumps(schedule, indent=2))

    with open("{}.json".format(file_name[:-4]), 'w') as f_out:
        json.dump(schedule, f_out, indent=2)
