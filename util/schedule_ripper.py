from bs4 import BeautifulSoup
from pprint import pprint
from tabulate import tabulate

with open('/Users/pwallington/Library/Preferences/PyCharm2018.2/scratches/series schedule.html', 'r') as f:
    html = f.read()

soup = BeautifulSoup(html, features="html.parser")

sched_table = soup.body.find('table', attrs={'id': 'series_schedule_list_table'})


header = [x.text for x in sched_table.findAll('th')]
table_rows = [x.findAll('td') for x in sched_table.findAll('tr')[2::2]]
table_data = [[x.get('title') if x.get('title') else x.text for x in r] for r in table_rows]


print(tabulate(table_data, header))

