import pandas as pd

fights = pd.read_csv("./data/raw_data/extended_fights.csv")

for lr,st in zip(fights['last_round'], fights['stoppage_time']):
    st = st.split(":")
    min = int(st[0])
    min *= 60
    min += int(st[1])
    min += (int(lr) - 1) * 5 * 60
    print(min)
    

