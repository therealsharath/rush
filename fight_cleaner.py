import pandas as pd

fights = pd.read_csv("./data/raw_data/extended_fights.csv")
fighters = pd.read_csv("./data/processed_data/cleaned_fighter_details.csv")

cleaned_data = {}

for idx, fighter in fighters.iterrows():
    for idx, fight in fights.where(fights['fighter_r'] == fighter['fighter_name'], inplace=True):
        print(fight)
    
    for idx, fight in fights.where(fights['fighter_b'] == fighter['fighter_name'], inplace=True):
        print(fight)
    break
    #total fight time
    # st = row['stoppage_time'].split(":")
    # sec = int(st[0])
    # sec *= 60
    # sec += int(st[1])
    # sec += (int(row['last_round']) - 1) * 5 * 60    


    # r_data = row['r_sig_str'].split()
    # r_lan_str = r_data[0]
    # r_atpt_str = r_data[1]
