import pandas as pd

fighters = pd.read_csv("./data/raw_data/fighter_ids.csv")
fighters.sort_values('fighter_name', inplace=True)
fighters.drop_duplicates(subset='fighter_name', keep='first', inplace=True)
fighters.to_csv("./data/processed_data/cleaned_fighter_ids.csv")
