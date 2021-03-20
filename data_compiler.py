import pandas as pd 


def prepareData(fighter):
    fighters = pd.read_csv('./data/raw_data/fighter_details.csv')
    fighter_data = fighters.loc[fighters['fighter_name'] == fighter].values.tolist()
    fighter_data = fighter_data[0]
    print(fighter_data)
    return []

prepareData('Khabib Nurmagomedov')