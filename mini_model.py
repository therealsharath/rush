import numpy as np
import pandas as pd

import tensorflow as tf

from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

df = pd.read_csv('./data/model_data/pr_model_data.csv')
df['bin_winner']  = np.where(df['winner'] == df['fighter_r'], 0, 1)
df = df.drop(columns=['fighter_r', 'fighter_b', 'winner', 'td_acc.1_r', 'td_acc.1_b'])

train, test = train_test_split(df, test_size=0.2)
train, val = train_test_split(train, test_size=0.2)

# A utility method to create a tf.data dataset from a Pandas Dataframe
def df_to_dataset(dataframe, shuffle=True, batch_size=32):
  dataframe = dataframe.copy()
  labels = dataframe.pop('bin_winner')
  ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
  if shuffle:
    ds = ds.shuffle(buffer_size=len(dataframe))
  ds = ds.batch(batch_size)
  return ds

batch_size = 5 # A small batch sized is used for demonstration purposes
train_ds = df_to_dataset(train, batch_size=batch_size)
val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)

numeric_colums = ['total_wins_r', 'total_losses_r', 'total_draws_r', 'total_nc_r', 'height_r', 'weight_r', 'reach_r', 'stance_r', 'dob_r', 'slpm_r', 'str_acc_r', 'sapm_r', 'str_def_r', 'td_avg_r', 'td_acc_r', 'td_def_r', 'td_acc.1_r', 'sub_avg_r', 'total_wins_b', 'total_losses_b', 'total_draws_b', 'total_nc_b', 'height_b', 'weight_b', 'reach_b', 'stance_b', 'dob_b', 'slpm_b', 'str_acc_b', 'sapm_b', 'str_def_b', 'td_avg_b', 'td_acc_b', 'td_def_b', 'td_acc_b', 'sub_avg_b']