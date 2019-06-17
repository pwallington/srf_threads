from bs4 import BeautifulSoup
from tabulate import tabulate
import json
from re import split

with open('/Users/pwallington/Library/Preferences/PyCharm2018.2/scratches/series schedule.html', 'r') as f:
    html = f.read()

soup = BeautifulSoup(html, features="html.parser")

sched_table = soup.body.find('table', attrs={'id': 'series_schedule_list_table'})


header = [x.text for x in sched_table.findAll('th')]
table_rows = [x.findAll('td') for x in sched_table.findAll('tr')[2::2]]
table_data = [[x.get('title') if x.get('title') else x.text for x in r] for r in table_rows]
styles = [r[3].get('style') for r in table_rows]
images = [x[x.find('(')+2:x.find(')')-1] for x in styles]

print(tabulate(table_data, header))
# print(json.dumps(table_data))
weeks = []
for row in table_data:
    week = {}
    for (key, col) in zip([x.lower().replace(' ', '_') for x in header], row):
        if key == 'options':
            opts = split('[\n\t]+', col)
            week['race_length'] = opts[1][12:]
            week['start'] = opts[2]
            week['cautions'] = opts[3]
            week['weather_date'] = ' '.join(opts[4].split(' ')[0:1])
            week['weather_scale'] = opts[4].split(' ')[2]
        elif key == 'track':
            if ' - ' in col:
                (week['track_name'], week['track_layout']) = col.rsplit(' - ', 1)
            else:
                (week['track_name'], week['track_layout']) = (col, '')
        elif col.isdigit():
            week[key] = int(col)
        else:
            week[key] = col
    weeks.append(week)

print(json.dumps(weeks, indent=2))
print(json.dumps([(x['track_name'], y) for (x,y) in zip(weeks, images)], indent=2))

