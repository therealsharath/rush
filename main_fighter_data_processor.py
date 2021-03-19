import pandas as pd

fighter_ids = pd.read_csv("./data/processed_data/cleaned_fighter_ids.csv")
fighter_ids.drop('Unnamed: 0',axis=1,inplace=True)
fighter_ids.drop('Unnamed: 0.1',axis=1,inplace=True)

fights = pd.read_csv("./data/raw_data/extended_fights.csv")

for id in fighter_ids['fighter_name'][:2]:
    fights_r = fights.loc[fights['fighter_r'] == id]
    if not fights_r.empty:
        print(fights_r)

    fights_b = fights.loc[fights['fighter_b'] == id]
    if not fights_b.empty:
        print(fights_b)    
