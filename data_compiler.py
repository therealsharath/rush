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
    fighter_fight_list = fighter_fight_list.sort_values(by = 'fight_date', ascending=False)

    del fighter_fight_list['Unnamed: 0']

    return fighter_fight_list

def prepareData(fighter):
    fighter_data = fighters.loc[fighters['fighter_name'] == fighter].values.tolist()
    fighter_data = fighter_data[0]
    fighter_fights = compile_fights(fighter)
    return fighter_fights

def curr_stats(fighter, fights):
    return []

fight_final_data = []
#Main processor
for fighter in fighters.iterrows():
    fighter = fighter[1]
    fighter_fights = prepareData(fighter['fighter_name'])

    win_stk = 0
    lose_stk = 0
    draw_stk = 0
    counted = 0

    for idx, fight in fighter_fights.iterrows():
        if counted < 5:
            counted += 1
            if fight['winner'] == fighter['fighter_name']:
                win_stk += 1
                lose_stk = 0
                draw_stk = 0
            elif fight['winner'] == '':
                win_stk += 0
                lose_stk = 0
                draw_stk += 1
            else:
                win_stk = 0
                lose_stk += 1
                draw_stk = 0   
        fighter_fights = fighter_fights.drop(idx)
        stats_for_fight = curr_stats(fighter, fighter_fights)
        
    print(win_stk, lose_stk, draw_stk) 
    break

# "_85aaee9fc23ca61102952862a10b544c-scss" 