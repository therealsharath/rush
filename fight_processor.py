import pandas as pd

fights = pd.read_csv('./data/raw_data/combined_fights.csv')
cleaned_fights = []
corners = ['r_', 'b_']

def of_cleaner(fight, title):
    for corner in corners:
        if fight[corner + title] != '---' and  fight[corner + title] != '--':
            title_split = fight[corner + title].split()
            fight[corner + 'att_' + title] = title_split[0]
            fight[corner + 'lan_' + title] = title_split[2]
        else:
            fight[corner + 'att_'+title] = '0'
            fight[corner + 'lan_'+title] = '0'

        del fight[corner + title]
    return fight

def pct_cleaner(fight, title):
    for corner in corners:
        if fight[corner + title] != '---' and  fight[corner + title] != '--':
            title_val = int(fight[corner + title][:-1])
            title_val /= 100
            fight[corner + title] = str(title_val)
        else:
            fight[corner + title] = '0'

    return fight

for idx, fight in fights.iterrows():
    try:
        #Winning corner
        if fight['winner'] == fight['fighter_r']:
            fight['winner_corner'] = 'r'
        else:
            fight['winner_corner'] = 'b'

        #total time and stoppage time in seconds
        st = fight['stoppage_time'].split(':')
        sec = int(st[0])
        sec *= 60
        sec += int(st[1])
        fight['stoppage_time'] = sec
        sec += (int(fight['last_round']) - 1) * 5 * 60
        fight['total_time'] = sec

        #maximum total time
        rounds = fight['fight_format'].split()[0]
        fight['maximum_scheduled_time'] = int(rounds) * 5 * 60

        fight = of_cleaner(fight, 'td')
        fight = of_cleaner(fight, 'sig_str')
        fight = of_cleaner(fight, 'total_str')
        fight = of_cleaner(fight, 'head')
        fight = of_cleaner(fight, 'body')
        fight = of_cleaner(fight, 'leg')
        fight = of_cleaner(fight, 'distance')
        fight = of_cleaner(fight, 'clinch')
        fight = of_cleaner(fight, 'ground')

        fight = pct_cleaner(fight, 'sig_str_pct')
        fight = pct_cleaner(fight, 'td_pct')

        #control
        for corner in corners:
            ctrl_split = fight[corner + 'ctrl'].split(':')
            ctrl = int(ctrl_split[0]) * 60
            ctrl += int(ctrl_split[1])
            fight[corner + 'ctrl'] = str(ctrl)
        
        del fight['Unnamed: 0']
        cleaned_fights.append(fight)
    except:
        print(fight['fight_id'])
        continue

pd.DataFrame(cleaned_fights).to_csv("./data/processed_data/cleaned_fight_details.csv")