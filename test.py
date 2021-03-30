import pandas as pd
import numpy as np
from common.sheetOperations import SheetOps
import warnings
warnings.filterwarnings("ignore")

obj = SheetOps()

no_of_past_candles = 20 #configurable
df = pd.read_csv('Investing/d_csv/TATASTEEL_5.csv')


slice = df.iloc[:no_of_past_candles]
print(len(slice.index))



def get_outliers(df, column_name):
    try:
        mn = df[column_name].mean()
        sd = df[column_name].std()
        final_list = [x for x in df[column_name] if (x > mn - 2 * sd)]
        final_list = [x for x in final_list if (x < mn + 2 * sd)]
        list_of_outliers = list(set(df[column_name].values.tolist()) - set(final_list))
        return list_of_outliers
        #return sorted(list_of_outliers, reverse=True)
    except Exception as e:
        print('Exception in getting list of outliers', e)
        return []

columns_to_write = ['datetime', 'symbol', 'pid', 'resolution', 'close',
                    'volume', 'per_change', 'volume_high_count', 'close_count', 'per_change_count']
slice = slice[columns_to_write]
outliers_close_rows = slice[slice.close_count.isin(get_outliers(slice, 'close_count'))]
outliers_volume_rows = slice[slice.volume_high_count.isin(get_outliers(slice, 'volume_high_count'))]
outliers_per_rows = slice[slice.per_change_count.isin(get_outliers(slice, 'per_change_count'))]

print(outliers_close_rows)
def write_sheet(write_list, l, position=-1):
    for wl in write_list:
        if position != -1 and len(l) == 0:
            wl[position] = ' '
        if position == -1 and len(l) != 0:
            for i in l:
                wl[i] = ' '
        obj.writeSheet('CIEnotifications', wl, 'InvestingNotify')

#all three
temp = pd.merge(outliers_close_rows, outliers_volume_rows, how='inner', on=columns_to_write)
ocr_ovr_opr = pd.merge(temp, outliers_per_rows, how='inner', on=columns_to_write)
#ocr_ovr_opr = pd.concat([outliers_close_rows, outliers_volume_rows, outliers_per_rows], axis=1, join='inner')
if len(ocr_ovr_opr) !=0:
    # write sheet
    write_list = ocr_ovr_opr.values.tolist()
    write_sheet(write_list, [], -2)
    for dt in ocr_ovr_opr['datetime']:
        outliers_close_rows.drop(outliers_close_rows[outliers_close_rows['datetime'] == dt].index, inplace=True)
        outliers_volume_rows.drop(outliers_volume_rows[outliers_volume_rows['datetime'] == dt].index, inplace=True)
        outliers_close_rows.drop(outliers_per_rows[outliers_per_rows['datetime'] == dt].index, inplace=True)

#any two
ocr_ovr = pd.merge(outliers_close_rows, outliers_volume_rows, how='inner', on=columns_to_write)
# ocr_ovr = pd.concat([outliers_close_rows, outliers_volume_rows], axis=1, join='inner')

if len(ocr_ovr) != 0:
    # write sheet
    write_list = ocr_ovr.values.tolist()
    write_sheet(write_list, [columns_to_write.index('per_change_count'),columns_to_write.index('per_change')], position=-1)
    for dt in ocr_ovr['datetime']:
        outliers_close_rows.drop(outliers_close_rows[outliers_close_rows['datetime'] == dt].index, inplace=True)
        outliers_volume_rows.drop(outliers_volume_rows[outliers_volume_rows['datetime'] == dt].index, inplace=True)


ocr_opr = pd.merge(outliers_close_rows, outliers_per_rows, how='inner', on=columns_to_write)
if len(ocr_opr) != 0:
    # write sheet
    write_list = ocr_opr.values.tolist()
    write_sheet(write_list, [columns_to_write.index('volume'),columns_to_write.index('volume_high_count')], position=-1)
    for dt in ocr_opr['datetime']:
        outliers_close_rows.drop(outliers_close_rows[outliers_close_rows['datetime'] == dt].index, inplace=True)
        outliers_per_rows.drop(outliers_per_rows[outliers_per_rows['datetime'] == dt].index, inplace=True)
#
ovr_opr = pd.merge(outliers_volume_rows, outliers_per_rows, how='inner', on=columns_to_write)
if len(ovr_opr) != 0:
    # write sheet
    write_list = ovr_opr.values.tolist()
    write_sheet(write_list, [columns_to_write.index('close'),columns_to_write.index('close_count')], position=-1)
    for dt in ovr_opr['datetime']:
        outliers_volume_rows.drop(outliers_volume_rows[outliers_volume_rows['datetime'] == dt].index, inplace=True)
        outliers_per_rows.drop(outliers_per_rows[outliers_per_rows['datetime'] == dt].index, inplace=True)


# write remaining sheets
if len(outliers_close_rows) != 0:
    #write sheet
    write_list = outliers_close_rows.values.tolist()
    write_sheet(write_list, [columns_to_write.index('volume'),columns_to_write.index('per_change'),
                             columns_to_write.index('volume_high_count'), columns_to_write.index('per_change_count')], -1)

if len(outliers_volume_rows) != 0:
    # write sheet
    write_list = outliers_volume_rows.values.tolist()
    write_sheet(write_list, [columns_to_write.index('close'),columns_to_write.index('per_change'),
                             columns_to_write.index('close_count'), columns_to_write.index('per_change_count')], -1)

if len(outliers_per_rows) !=0:
    # write sheet
    write_list = outliers_per_rows.values.tolist()
    write_sheet(write_list, [columns_to_write.index('close'),columns_to_write.index('volume'),
                             columns_to_write.index('volume_high_count'), columns_to_write.index('close_count')], -1)

#






