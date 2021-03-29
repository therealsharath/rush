import pandas as pd

fights = pd.read_csv('./data/raw_data/combined_fights.csv')
cleaned_fights = []

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

    #Processing "of" stats
    if fight['r_sig_str'] != '---' and  fight['r_sig_str'] != '--':
        r_sig_str = fight['r_sig_str'].split()
        fight['r_att_sig_str'] = r_sig_str[0]
        fight['r_lan_sig_str'] = r_sig_str[2]
    else:
        fight['r_att_sig_str'] = '0'
        fight['r_lan_sig_str'] = '0'
    
    if fight['b_sig_str'] != '---' and  fight['b_sig_str'] != '--':
        b_sig_str = fight['b_sig_str'].split()
        fight['b_att_sig_str'] = b_sig_str[0]
        fight['b_lan_sig_str'] = r_sig_str[2]
    else:
        fight['b_att_sig_str'] = '0'
        fight['b_lan_sig_str'] = '0'

    fight.drop('r_sig_str')
    fight.drop('b_sig_str')

    #total strikes
    if fight['r_total_str'] != '---' and  fight['r_total_str'] != '--':
        r_total_str = fight['r_total_str'].split()
        fight['r_att_total_str'] = r_total_str[0]
        fight['r_lan_total_str'] = r_total_str[2]
    else:
        fight['r_att_total_str'] = '0'
        fight['r_lan_total_str'] = '0'
    
    if fight['b_total_str'] != '---' and  fight['b_total_str'] != '--':
        b_sig_str = fight['b_total_str'].split()
        fight['b_att_total_str'] = b_sig_str[0]
        fight['b_lan_total_str'] = r_sig_str[2]
    else:
        fight['b_att_total_str'] = '0'
        fight['b_lan_total_str'] = '0'

    #takedowns
    if fight['r_td'] != '---' and  fight['r_td'] != '--':
        r_total_str = fight['r_td'].split()
        fight['r_att_td'] = r_total_str[0]
        fight['r_lan_td'] = r_total_str[2]
    else:
        fight['r_att_td'] = '0'
        fight['r_lan_td'] = '0'
    
    if fight['b_td'] != '---' and  fight['b_td'] != '--':
        b_sig_str = fight['b_td'].split()
        fight['b_att_td'] = b_sig_str[0]
        fight['b_lan_td'] = r_sig_str[2]
    else:
        fight['b_att_td'] = '0'
        fight['b_lan_td'] = '0'

    #control
    r_ctrl_split = fight['r_ctrl'].split(':')
    r_ctrl = int(r_ctrl_split[0]) * 60
    r_ctrl += int(r_ctrl_split[1])
    fight['r_ctrl'] = str(r_ctrl)

    b_ctrl_split = fight['b_ctrl'].split(':')
    b_ctrl = int(b_ctrl_split[0]) * 60
    b_ctrl += int(b_ctrl_split[1])
    fight['b_ctrl'] = str(b_ctrl)

    #takedowns
    if fight['r_head'] != '---' and  fight['r_head'] != '--':
        r_total_str = fight['r_head'].split()
        fight['r_att_td'] = r_total_str[0]
        fight['r_lan_td'] = r_total_str[2]
    else:
        fight['r_att_td'] = '0'
        fight['r_lan_td'] = '0'
    
    if fight['b_td'] != '---' and  fight['b_td'] != '--':
        b_sig_str = fight['b_td'].split()
        fight['b_att_td'] = b_sig_str[0]
        fight['b_lan_td'] = r_sig_str[2]
    else:
        fight['b_att_td'] = '0'
        fight['b_lan_td'] = '0'

    print(fight['b_ctrl'])
    break
