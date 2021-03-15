import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

event_ids = pd.read_csv("./data/raw_data/event_extended_ids.csv")

fight_id_data = {}
count = 0
for id in event_ids['event_id']:
    page = requests.get("http://ufcstats.com/event-details/"+id)
    parsed_content = bs(page.content, 'html.parser')
    results = parsed_content.find_all('tr', class_='b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click')
    for result in results:
        fight_id = result['data-link']
        if len(fight_id) > 0:
            fight_id_data[len(fight_id_data) + 1] = fight_id.split('/')[-1]
    count += 1
    print(count)  

fight_ids = pd.DataFrame.from_dict(fight_id_data, orient='index', columns=['fight_id'])
fight_ids.to_csv('./data/raw_data/fights_ids.csv')
