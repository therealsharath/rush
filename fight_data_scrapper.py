import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

fight_ids = pd.read_csv("./data/raw_data/fight_ids.csv")

fight_raw_data = {}
fighter_ids = {}

for id in fight_ids['fight_id']:
    #Getting the stats page of every single fight
    page = requests.get("http://ufcstats.com/fight-details/"+id)
    parsed_content = bs(page.content, 'html.parser')
    result = parsed_content.find('section', class_="b-statistics__section_details")

    #Getting fighters and the winner
    fighters = result.find_all('a', class_="b-link b-fight-details__person-link")
    fighter_R = fighters[0].text.strip()
    fighter_B = fighters[1].text.strip()
    winner = "N/A"

    #Storing fighter ids
    if fighters[0] not in fight_ids:
        fighter_ids[fighters[0]] = fighters[0]['href'].split('/')[-1]
    if fighters[1] not in fight_ids:
        fighter_ids[fighters[1]] = fighters[1]['href'].split('/')[-1]

    #Winner
    result = parsed_content.find_all('div', class_="b-fight-details__persons clearfix")
    winner = result[0].find_all('div', class_="b-fight-details__person")
    if winner[0].find('i', class_="b-fight-details__person-status b-fight-details__person-status_style_green"):
        winner = fighter_R
    elif winner[1].find('i', class_="b-fight-details__person-status b-fight-details__person-status_style_green"):
        winner = fighter_B
    else:
        winner = "N/A"
    
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
                fight_format = " ".join(contents[2:])
            elif contents[0] == 'Referee:':
                referee = " ".join(contents[1:])
    
    #Individual Stats of fighters
    fighter_R_stats = []
    fighter_B_stats = []

    #Stats for each round
    rounds = {}

    #All stats
    table = parsed_content.find_all('td', class_="b-fight-details__table-col")
    for i in range(1,10):
        if len(table[i].text.split()) == 2:
            fighter_R_stats.append(table[i].text.split()[0])
            fighter_B_stats.append(table[i].text.split()[1])
        elif len(table[i].text.split()) == 6:
            fighter_R_stats.append(" ".join(table[i].text.split()[:3]))
            fighter_B_stats.append(" ".join(table[i].text.split()[3:]))
    
    #All stats per round
    for i in range(1, last_round + 1):
        start =  10 + (i - 1) * 10
        end = start + 10
        rounds[i] = {fighter_R : [], fighter_B : []}
        for j in range(start, end):
            if len(table[j].text.split()) == 2:
                rounds[i][fighter_R].append(table[j].text.split()[0])
                rounds[i][fighter_B].append(table[j].text.split()[1])
            elif len(table[j].text.split()) == 6:
                rounds[i][fighter_R].append(" ".join(table[j].text.split()[:3]))
                rounds[i][fighter_B].append(" ".join(table[j].text.split()[3:]))
    
    #Significant strikes
    start = 10 + (last_round * 10) + 1
    for i in range(start, start + 8):
        if len(table[i].text.split()) == 2:
            fighter_R_stats.append(table[i].text.split()[0])
            fighter_B_stats.append(table[i].text.split()[1])
        elif len(table[i].text.split()) == 6:
            fighter_R_stats.append(" ".join(table[i].text.split()[:3]))
            fighter_B_stats.append(" ".join(table[i].text.split()[3:]))
    
    #Significant strikes per round
    for i in range(1, last_round + 1):
        round_start =  (start + 9) + (i - 1) * 9
        for j in range(round_start, round_start + 8):
            if len(table[j].text.split()) == 2:
                rounds[i][fighter_R].append(table[j].text.split()[0])
                rounds[i][fighter_B].append(table[j].text.split()[1])
            elif len(table[j].text.split()) == 6:
                rounds[i][fighter_R].append(" ".join(table[j].text.split()[:3]))
                rounds[i][fighter_B].append(" ".join(table[j].text.split()[3:]))
    break


# fighter_ids = {key: value for key, value in sorted(fighter_ids.items())}