import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from time import strftime, strptime

event_ids = pd.read_csv("./data/raw_data/event_extended_ids.csv")

fight_id_data = {}
prev = 0

for event in event_ids.iterrows():
    try:
        id = event[1]['event_id']
        page = requests.get("http://ufcstats.com/event-details/"+id)
        parsed_content = bs(page.content, 'html.parser')
        results = parsed_content.find_all('tr', class_='b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click')
        for result in results:
            fight_id = result['data-link']
            if len(fight_id) > 0:
                fight_date = event[1]['date'].split()
                fight_date[0] = str(strptime(fight_date[0], '%B').tm_mon)
                fight_date[1] = fight_date[1][:-1]
                fight_date = "/".join(fight_date)
                fight_id_data[len(fight_id_data) + 1] = [fight_id.split('/')[-1], fight_date, event[1]['event_name'], event[1]['location']]
        if len(fight_id_data) - prev > 100:
            print(len(fight_id_data))
            prev = len(fight_id_data)
    except:
        print(event)
        continue

fight_ids = pd.DataFrame.from_dict(fight_id_data, orient='index', columns=['fight_id', 'fight_date', 'event_name', 'location'])
fight_ids.to_csv('./data/processed_data/extended_fight_ids.csv')
