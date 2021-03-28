import pandas as pd

df = pd.read_csv('Edelweiss/csv/NIFTY_29_Apr_2021.csv')
print(df.head())
column_names = ['StrikePrice', 'COI']
for column_name in column_names:
     mn = df[column_name].mean()
     sd = df[column_name].std()
     final_list = [x for x in df[column_name] if (x > mn - 2 * sd)]
     final_list = [x for x in final_list if (x < mn + 2 * sd)]
     list_of_outliers = list(set(df[column_name].values.tolist()) - set(final_list))
     print(list_of_outliers)