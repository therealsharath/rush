import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

fight_ids = pd.read_csv("./data/processed_data/extended_fight_ids.csv")

fight_raw_data = {}
count = 0

for row in fight_ids.iterrows():
    try:
        id = row[1]['fight_id']
        #Getting the stats page of every single fight
        page = requests.get("http://ufcstats.com/fight-details/"+id)
        parsed_content = bs(page.content, 'html.parser')
        result = parsed_content.find('section', class_="b-statistics__section_details")

        #Getting fighters and the winner
        fighters = result.find_all('a', class_="b-link b-fight-details__person-link")
        fighter_R = fighters[0].text.strip()
        fighter_B = fighters[1].text.strip()

        #Winner
        result = parsed_content.find_all('div', class_="b-fight-details__persons clearfix")
        winner = result[0].find_all('div', class_="b-fight-details__person")
        if winner[0].find('i', class_="b-fight-details__person-status b-fight-details__person-status_style_green"):
            winner = fighter_R
        elif winner[1].find('i', class_="b-fight-details__person-status b-fight-details__person-status_style_green"):
            winner = fighter_B
        else:
            winner = "N/A"
        
        #Championship fight or not
        championship_fight = False
        title = parsed_content.find('img', src="http://1e49bc5171d173577ecd-1323f4090557a33db01577564f60846c.r80.cf1.rackcdn.com/belt.png")
        if title:
            championship_fight = True
        else:
            championship_fight = False
        
        #Weight class
        weight_class = " ".join(parsed_content.find('i', class_="b-fight-details__fight-title").text.strip().split()[:-1])

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

        #All stats
        table = parsed_content.find_all('td', class_="b-fight-details__table-col")
        for i in range(1,10):
            if len(table[i].text.split()) == 2:
                fighter_R_stats.append(table[i].text.split()[0])
                fighter_B_stats.append(table[i].text.split()[1])
            elif len(table[i].text.split()) == 6 and any(i.isdigit() for i in table[i].text.strip()):
                fighter_R_stats.append(" ".join(table[i].text.split()[:3]))
                fighter_B_stats.append(" ".join(table[i].text.split()[3:]))    
        
        #Significant strikes
        start = 10 + (last_round * 10) + 3
        for i in range(start, start + 7):
            if len(table[i].text.split()) == 2:
                fighter_R_stats.append(table[i].text.split()[0])
                fighter_B_stats.append(table[i].text.split()[1])
            elif len(table[i].text.split()) == 6 and any(i.isdigit() for i in table[i].text.strip()):
                fighter_R_stats.append(" ".join(table[i].text.split()[:3]))
                fighter_B_stats.append(" ".join(table[i].text.split()[3:]))

        #Adding total fight data
        fight_stats = [id, fighter_R, fighter_B, winner, championship_fight, weight_class, method, last_round, stop_time, fight_format, referee]
        fight_stats.extend(fighter_R_stats)
        fight_stats.extend(fighter_B_stats)
        fight_stats.append(row[1]['fight_date'])
        fight_stats.append(row[1]['event_name'])
        fight_stats.append(row[1]['location'])
        fight_raw_data[len(fight_raw_data) + 1] = fight_stats

        if len(fight_raw_data) % 50 == 0:
            print(len(fight_raw_data))
            #Storing fight data
            fight_data = pd.DataFrame.from_dict(fight_raw_data, orient='index', columns=['fight_id', 'fighter_r', 'fighter_b', 'winner', 'title_fight', 'weight_class', 'win_by', 'last_round', 'stoppage_time', 'fight_format', 'referee', 'r_kd', 'r_sig_str', 'r_sig_str_pct', 'r_total_str', 'r_td', 'r_td_pct', 'r_sub_att', 'r_rev', 'r_ctrl', 'r_head', 'r_body', 'r_leg', 'r_distance', 'r_clinch', 'r_ground', 'b_kd', 'b_sig_str', 'b_sig_str_pct', 'b_total_str', 'b_td', 'b_td_pct', 'b_sub_att', 'b_rev', 'b_ctrl', 'b_head', 'b_body', 'b_leg', 'b_distance', 'b_clinch', 'b_ground', 'fight_date', 'event_name', 'location'])
            fight_data.to_csv('./data/raw_data/combined_fights.csv')
    except:
        print(id)
        continue

#Storing fight data
fight_data = pd.DataFrame.from_dict(fight_raw_data, orient='index', columns=['fight_id', 'fighter_r', 'fighter_b', 'winner', 'title_fight', 'weight_class', 'win_by', 'last_round', 'stoppage_time', 'fight_format', 'referee', 'r_kd', 'r_sig_str', 'r_sig_str_pct', 'r_total_str', 'r_td', 'r_td_pct', 'r_sub_att', 'r_rev', 'r_ctrl', 'r_head', 'r_body', 'r_leg', 'r_distance', 'r_clinch', 'r_ground', 'b_kd', 'b_sig_str', 'b_sig_str_pct', 'b_total_str', 'b_td', 'b_td_pct', 'b_sub_att', 'b_rev', 'b_ctrl', 'b_head', 'b_body', 'b_leg', 'b_distance', 'b_clinch', 'b_ground', 'fight_date', 'event_name', 'location'])
fight_data.to_csv('./data/raw_data/combined_fights.csv')