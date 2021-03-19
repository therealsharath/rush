import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

fighter_ids = pd.read_csv("./data/processed_data/cleaned_fighter_ids.csv")
fighter_ids.drop('Unnamed: 0',axis=1,inplace=True)
fighter_ids.drop('Unnamed: 0.1',axis=1,inplace=True)

fights = pd.read_csv("./data/raw_data/extended_fights.csv")

fighter_details = {}

# Format for fighter details
# [fighter_id, fighter_name, total_wins, total_losses, total_draws, total_nc, height, weight, reach, stance, dob, slpm, str_acc, sapm, str_def, td_avg, td_acc, td_def, td_acc, sub_avg]

for id,fighter in zip(fighter_ids['id'], fighter_ids['fighter_name']):
    try:
        page = requests.get('http://ufcstats.com/fighter-details/'+id)
        parsed_content = bs(page.content, 'html.parser')
        record = parsed_content.find('span', class_='b-content__title-record')
        
        wldnc = record.text.strip().split()
        total_wins = wldnc[1].split('-')[0]
        total_losses = wldnc[1].split('-')[1]
        total_draws = wldnc[1].split('-')[2]
        
        total_nc = 0
        if len(wldnc) > 2:
            total_nc = wldnc[2][1]

        stats = parsed_content.find_all('li', class_='b-list__box-list-item b-list__box-list-item_type_block')
        
        height = "".join(stats[0].text.split()[1:])
        weight = stats[1].text.split()[1]
        reach = stats[2].text.split()[1]
        stance = stats[3].text.split()[1]
        dob = stats[4].text.split()[1] + ',' + "".join(stats[4].text.split()[2:])
        slpm = stats[5].text.split()[1]
        str_acc = stats[6].text.split()[2]
        sapm = stats[7].text.split()[1]
        str_def = stats[8].text.split()[2]
        td_avg = stats[10].text.split()[2]
        td_acc = stats[11].text.split()[2]
        td_def = stats[12].text.split()[2]
        sub_avg = stats[13].text.split()[2]

        fighter_details[len(fighter_details) + 1] = [id, fighter, total_wins, total_losses, total_draws, total_nc, height, weight, reach, stance, dob, slpm, str_acc, sapm, str_def, td_avg, td_acc, td_def, td_acc, sub_avg]

        if len(fighter_details) % 50 == 0:
            print(len(fighter_details))
            fighter_data = pd.DataFrame.from_dict(fighter_details, orient='index', columns=['id','fighter_name','total_wins','total_losses', 'total_draws', 'total_nc', 'height', 'weight', 'reach', 'stance', 'dob', 'slpm', 'str_acc', 'sapm', 'str_def', 'td_avg', 'td_acc', 'td_def', 'td_acc', 'sub_avg'])
            fighter_data.to_csv('./data/raw_data/fighter_details.csv')
    except:
        print(id)
        continue

fighter_data = pd.DataFrame.from_dict(fighter_details, orient='index', columns=['id','fighter_name','total_wins','total_losses', 'total_draws', 'total_nc', 'height', 'weight', 'reach', 'stance', 'dob', 'slpm', 'str_acc', 'sapm', 'str_def', 'td_avg', 'td_acc', 'td_def', 'td_acc', 'sub_avg'])
fighter_data.to_csv('./data/raw_data/fighter_details.csv')