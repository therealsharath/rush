import pandas as pd 

fighters = pd.read_csv('./data/raw_data/fighter_details.csv')
fights = pd.read_csv('./data/raw_data/combined_fights.csv')

def prepareData(fighter):
    fighter_data = fighters.loc[fighters['fighter_name'] == fighter].values.tolist()
    fighter_data = fighter_data[0]
    print(fighter_data)
    return fighter_data

prepareData('Khabib Nurmagomedov')