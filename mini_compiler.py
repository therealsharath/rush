import pandas as pd 
from datetime import datetime

fighters = pd.read_csv('./data/processed_data/cleaned_fighter_details.csv')
fights = pd.read_csv('./data/processed_data/cleaned_fight_details.csv')
del fighters['Unnamed: 0']
corners = ['r', 'b']
compiled_data = []
new_indices = ['fighter_r', 'fighter_b', 'winner', 'total_wins_r', 'total_losses_r', 'total_draws_r', 'total_nc_r', 'height_r', 'weight_r', 'reach_r', 'stance_r', 'dob_r', 'slpm_r', 'str_acc_r', 'sapm_r', 'str_def_r', 'td_avg_r', 'td_acc_r', 'td_def_r', 'td_acc.1_r', 'sub_avg_r', 'total_wins_b', 'total_losses_b', 'total_draws_b', 'total_nc_b', 'height_b', 'weight_b', 'reach_b', 'stance_b', 'dob_b', 'slpm_b', 'str_acc_b', 'sapm_b', 'str_def_b', 'td_avg_b', 'td_acc_b', 'td_def_b', 'td_acc.1_b', 'sub_avg_b']

for idx, fight in fights.iterrows():
    try:
        new_fight = [fight['fighter_r'], fight['fighter_b'], fight['winner']]
        for corner in corners:
            fig_r = fighters.loc[fighters['fighter_name'] == fight['fighter_' + corner]]
            fig_r = fig_r.values.tolist()
            if len(fig_r) > 0:
                fig_r = fig_r[0]
                del fig_r[:3]
                new_fight += fig_r
        
        if len(new_fight) == 39:
            compiled_data.append(new_fight)
    except:
        continue

print(len(compiled_data))
compiled_data = pd.DataFrame(compiled_data, columns=new_indices)
compiled_data.to_csv('./data/processed_data/pr_model_data.csv')