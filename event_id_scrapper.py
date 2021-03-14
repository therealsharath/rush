import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

page = requests.get("http://ufcstats.com/statistics/events/completed?page=all")
parsed_content = bs(page.content, 'html.parser')
results = parsed_content.find_all('tr', class_='b-statistics__table-row')

event_id_data = {}
for result in results:
    event_id = result.findChildren('a')
    date = result.findChildren('span')
    location = result.findChildren('td', { "class": "b-statistics__table-col b-statistics__table-col_style_big-top-padding" })

    if len(event_id) > 0 and len(date) > 0 and len(location) > 0:    
        event_id_data[len(event_id_data) + 1] = [event_id[0]['href'].split('/')[-1], event_id[0].text.strip(), date[0].text.strip(), location[0].text.strip()]

event_ids = pd.DataFrame.from_dict(event_id_data, orient='index', columns=['event_id', 'event_name', 'date', 'location'])
event_ids.to_csv('./data/raw_data/event_extended_ids.csv')