import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

fight_ids = pd.read_csv("./data/raw_data/fight_ids.csv")

fight_raw_data = {}
fighter_ids = {}

for id in fight_ids['fight_id']:
    page = requests.get("http://ufcstats.com/fight-details/"+id)
    parsed_content = bs(page.content, 'html.parser')
    result = parsed_content.find('section', class_="b-statistics__section_details")

    #Getting fighters
    fighters = result.find_all('a', class_="b-link b-fight-details__person-link")
    fighter_R = fighters[0].text.strip()
    fighter_B = fighters[1].text.strip()

    #Storing fighter ids
    if fighters[0] not in fight_ids:
        fighter_ids[fighters[0]] = fighters[0]['href'].split('/')[-1]
    if fighters[1] not in fight_ids:
        fighter_ids[fighters[1]] = fighters[1]['href'].split('/')[-1]

    #Weight class
    weight_class = parsed_content.find('i', class_="b-fight-details__fight-title").text.strip().split()[0]

    #Key details
    key_details = parsed_content.find('div', class_="b-fight-details__content")
    
    method = ""
    last_round = 0
    stop_time = ""
    fight_format = ""
    referee = ""

    for i in key_details.find_all('i'):
        if not i.has_attr('class'):
            method = i.text
        elif i['class'][0] == 'b-fight-details__text-item':
            contents = i.text.split()
            if contents[0] == 'Round:':
                last_round = int(contents[1])
            elif contents[0] == "Time:":
                stop_time = contents[1]
            elif contents[0] == 'Time':
                fight_format = " ".join(contents[1:])
            elif contents[0] == 'Referee:':
                referee = " ".join(contents[1:])
    
    #Fighter-wise stats
    break
# fighter_ids = {key: value for key, value in sorted(fighter_ids.items())}