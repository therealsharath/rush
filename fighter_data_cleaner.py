import pandas as pd
from time import strptime

fighters = pd.read_csv("./data/raw_data/fighter_details.csv")

for i in range(len(fighters['dob'])):
    dob = fighters['dob'][i].split(',')
    if len(dob) == 3:
        dob[0] = str(strptime(dob[0], '%b').tm_mon)
        dob = "/".join(dob)
        fighters.loc[i, 'dob'] = dob

fighters.drop(fighters[fighters['reach'] == '--'].index, inplace=True)
fighters.to_csv("./data/processed_data/cleaned_fighter_details.csv")