import pandas as pd 
from datetime import date, datetime
from dateutil.relativedelta import *

df = pd.read_csv('./data/model_data/pr_model_data.csv')
del df['Unnamed: 0']
corners = ['r', 'b']

def ft_to_in(ft):
    ft = ft.split("'")
    ft = int(ft[0][0]) * 12 + int(ft[1][:-1])
    return str(ft)


for corner in corners:
    #height
    df['height_' + corner] = df['height_' + corner].map(lambda a: ft_to_in(a))

    #reach
    df['reach_' + corner] = df['reach_' + corner].map(lambda a: a[:-1])

    #dob
    idx = df[df['dob_' + corner] == '--,'].index
    df.drop(idx, inplace = True)
    df['dob_' + corner] = df['dob_' + corner].map(lambda a: relativedelta(datetime.utcnow().date(), datetime.strptime(a + " 01:55:19", '%m/%d/%Y %H:%M:%S')).years)

    #pcts
    df['str_acc_' + corner] = df['str_acc_' + corner].map(lambda a: float(a[:-1])/100.0)
    df['str_def_' + corner] = df['str_def_' + corner].map(lambda a: float(a[:-1])/100.0)
    df['td_acc_' + corner] = df['td_acc_' + corner].map(lambda a: float(a[:-1])/100.0)
    df['td_def_' + corner] = df['td_def_' + corner].map(lambda a: float(a[:-1])/100.0)


compiled_data = df.to_csv('./data/model_data/mini_model_data.csv')