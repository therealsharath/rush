import pandas as pd

fights = pd.read_csv('./data/raw_data/combined_fights.csv')
cleaned_fights = []
corners = ['r_', 'b_']

def of_cleaner(title):
    for corner in corners:
        if fight[corner + title] != '---' and  fight[corner + title] != '--':
            title_split = fight[corner + title].split()
            fight[corner + 'att_' + title] = title_split[0]
            fight[corner + 'lan_' + title] = title_split[2]
        else:
            fight[corner + 'att_'+title] = '0'
            fight[corner + 'lan_'+title] = '0'

        fight.drop(corner+title)

for idx, fight in fights.iterrows():
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

    of_cleaner('td')
    of_cleaner('sig_str')
    of_cleaner('total_str')
    of_cleaner('head')
    of_cleaner('body')

    #control
    r_ctrl_split = fight['r_ctrl'].split(':')
    r_ctrl = int(r_ctrl_split[0]) * 60
    r_ctrl += int(r_ctrl_split[1])
    fight['r_ctrl'] = str(r_ctrl)

    b_ctrl_split = fight['b_ctrl'].split(':')
    b_ctrl = int(b_ctrl_split[0]) * 60
    b_ctrl += int(b_ctrl_split[1])
    fight['b_ctrl'] = str(b_ctrl)

    print(fight)
    break
