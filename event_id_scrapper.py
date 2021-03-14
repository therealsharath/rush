from re import T
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

page = requests.get("http://ufcstats.com/statistics/events/completed?page=all")
parsed_content = bs(page.content, 'html.parser')
results = parsed_content.find_all('a', class_='b-link b-link_style_black', href=True)

event_id_data = {}

for result in results:
    to_store = []
    to_store.append(result['href'].split('/')[-1])
    to_store.append(result.text.strip())
    event_id_data[len(event_id_data) + 1] = to_store

event_ids = pd.DataFrame.from_dict(event_id_data, orient='index', columns=['event_id', 'event_name'])
event_ids.to_csv('./data/raw_data/event_ids.csv')