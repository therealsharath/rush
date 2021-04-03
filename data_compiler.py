import pandas as pd 
from datetime import datetime

fighters = pd.read_csv('./data/processed_data/cleaned_fighter_details.csv')
fights = pd.read_csv('./data/processed_data/cleaned_fight_details.csv')
corners = ['r', 'b']

def compile_fights(fighter):
    fighter_fight_list = []

    for corner in corners:
        fighter_fights = fights.loc[fights['fighter_' + corner] == fighter]
        if len(fighter_fights) > 0:
            for idx, fight in fighter_fights.iterrows():
                fight['fight_date'] = datetime.strptime(fight['fight_date'] + ' 00:00:00', '%m/%d/%Y %H:%M:%S')
                fighter_fight_list.append(fight)    
    
    fighter_fight_list = pd.DataFrame(fighter_fight_list)
    fighter_fight_list.sort_values(by = 'fight_date')

    del fight['Unnamed: 0']
    return fighter_fight_list

def prepareData(fighter):
    fighter_data = fighters.loc[fighters['fighter_name'] == fighter].values.tolist()
    fighter_data = fighter_data[0]

    fighter_fights = compile_fights(fighter)

    print(fighter_fights['fight_date'])
    return fighter_data

prepareData('Khabib Nurmagomedov')