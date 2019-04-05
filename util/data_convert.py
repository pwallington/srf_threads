#!/usr/bin/python

import json
import os
import sys

somedir = '../data'
files = [f for f in os.listdir(somedir) if os.path.isfile(os.path.join(somedir, f))]

for file_name in files:
    print(file_name)

    notes = []
    data = {}

    try:
        with open(os.path.join(somedir, file_name), 'r') as tr_file:
            for line in tr_file.readlines():
                if not notes:
                    # print(line)
                    (tag, value) = line.strip().split(' : ')
                    # print ("Found tag: %s with value: %s" % (tag, value))
                    if tag == "TRACK_NOTES":
                        notes = ['']
                    else:
                        data[tag] = value
                else:
                    notes.append(line)
            data['TRACK_NOTES'] = ''.join(notes)

        with open("{}.json".format(file_name), 'w') as f_out:
            json.dump(data, f_out, indent=2)
            # print(json.dumps(data, indent=2))
    except Exception as e:
        print("Caught exception with file:", file_name, e, file=sys.stderr)

