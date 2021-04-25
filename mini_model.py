import numpy as np
import pandas as pd

import tensorflow as tf

from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

df = pd.read_csv('./data/model_data/mini_model_data.csv')
df['bin_winner']  = np.where(df['winner'] == df['fighter_r'], 0, 1)
df = df.drop(columns=['fighter_r', 'fighter_b', 'winner'])

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
  
numeric_colums = ['total_wins_r', 'total_losses_r', 'total_draws_r', 'total_nc_r', 'height_r', 'weight_r', 'reach_r', 'dob_r', 'slpm_r', 'str_acc_r', 'sapm_r', 'str_def_r', 'td_avg_r', 'td_acc_r', 'td_def_r', 'sub_avg_r', 'total_wins_b', 'total_losses_b', 'total_draws_b', 'total_nc_b', 'height_b', 'weight_b', 'reach_b', 'dob_b', 'slpm_b', 'str_acc_b', 'sapm_b', 'str_def_b', 'td_avg_b', 'td_acc_b', 'td_def_b', 'sub_avg_b']

feature_columns = []
for header in numeric_colums:
  feature_columns.append(feature_column.numeric_column(header))

stance_r = feature_column.categorical_column_with_vocabulary_list(
      'stance_r', df.stance_r.unique())
stance_r_embedding = feature_column.embedding_column(stance_r, dimension=8)
feature_columns.append(stance_r_embedding)

stance_b = feature_column.categorical_column_with_vocabulary_list(
      'stance_b', df.stance_b.unique())
stance_b_embedding = feature_column.embedding_column(stance_b, dimension=8)
feature_columns.append(stance_b_embedding)

feature_layer = tf.keras.layers.DenseFeatures(feature_columns)
batch_size = 200
train_ds = df_to_dataset(train, batch_size=batch_size)
val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)

model = tf.estimator.BoostedTreesClassifier(
    feature_columns, batch_size, n_classes=2,
)

model.compile(optimizer='adam', loss=tf.keras.losses.BinaryCrossentropy(from_logits=True), metrics=['accuracy'])

model.fit(train_ds, validation_data=val_ds, epochs=10)

loss, accuracy = model.evaluate(test_ds)
print("Accuracy", accuracy)