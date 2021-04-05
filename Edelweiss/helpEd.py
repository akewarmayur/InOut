import numpy as np
from common.sheetOperations import SheetOps
import Edelweiss.edleConfig as edleConfig
from common.common import CommonFunctions
import warnings
warnings.filterwarnings("ignore")

class HelpEd:

    def __init__(self):
        self.objSheet = SheetOps()
        self.objCommon = CommonFunctions()

    # def cal_outliers(self, lst):
    #     mn = np.mean(lst)
    #     sd = np.std(lst)
    #     final_list = [x for x in lst if (x > mn - 2 * sd)]
    #     final_list = [x for x in final_list if (x < mn + 2 * sd)]
    #     list_of_outliers = list(set(lst) - set(final_list))
    #     # print('outliers:', list_of_outliers)
    #     return list_of_outliers

    # def cal_change_OI(self, df):
    #     try:
    #         df['OI_change'] = 0
    #         df_length = len(df.index)
    #         for i, columnData in enumerate(df['OI']):
    #             s = i + 1
    #             if s < df_length:
    #                 temp = columnData - df['OI'].iloc[i + 1]
    #                 df['OI_change'].iloc[i] = temp
    #             else:
    #                 df['OI_change'].iloc[i] = 0
    #         return df
    #     except Exception as e:
    #         print('Exception in changeOI calculation:', e)

    def cal_outliers(self, data):
        anomalies = []

        # Set upper and lower limit to 3 standard deviation
        random_data_std = np.std(data)
        random_data_mean = np.mean(data)
        anomaly_cut_off = random_data_std * 2

        lower_limit = random_data_mean - anomaly_cut_off
        upper_limit = random_data_mean + anomaly_cut_off

        # Generate outliers
        for outlier in data:
            if outlier > upper_limit or outlier < lower_limit:
                anomalies.append(outlier)
        return anomalies

    def cal_change_OI(self, df, current_time, symbol, dt):
        try:
            df['OI_change'] = 0
            df['Flag'] = False
            df_length = len(df.index)
            # print(list_ofchangeOI)

            for i, columnData in enumerate(df['OI']):
                s = i + 1
                if s < df_length:
                    temp = columnData - df['OI'].iloc[i + 1]
                    df['OI_change'].iloc[i] = temp
                else:
                    df['OI_change'].iloc[i] = 0
            list_ofchangeOI = df['OI_change'].tolist()
            anomalies = self.cal_outliers(list_ofchangeOI)
            if len(anomalies) != 0:
                for x, y in enumerate(list_ofchangeOI):
                    for a, b in enumerate(anomalies):
                        if b == y:
                            df['Flag'].iloc[x] = True
                            if df['StrTradeDateTime'].iloc[x] == current_time:
                                self.notify_process(df, x, symbol, dt)
            return df
        except Exception as e:
            print('Exception in changeOI calculation:', e)


    def cal_Out(self, df):
        PE = list(df[df['OptionType'] == 'PE']['StrikePrice'].unique())
        CE = list(df[df['OptionType'] == 'CE']['StrikePrice'].unique())
        # print(dd)
        df['OI_change'] = 0
        df['Flag'] = False
        # print(df.head())
        for i, j in enumerate(PE):
            temp = df[df['StrikePrice'] == j]
            temp = self.cal_change_OI(temp)
            # cal_outliers1(j, temp['OI_change'].tolist())
            for a, row in temp.iterrows():
                df['OI_change'].iloc[a] = row['OI_change']
                df['Flag'].iloc[a] = row['Flag']
        for i, j in enumerate(CE):
            temp = df[df['StrikePrice'] == j]
            temp = self.cal_change_OI(temp)
            # print(temp)
            for a, row in temp.iterrows():
                df['OI_change'].iloc[a] = row['OI_change']

    def concate(self, previous_df, df_now, first=True):
        if first == True:
            fixed_columns= ['ScripName', 'StrikePrice', 'OptionType',
                             'StrTradeDateTime', 'TradeDateTime', 'ExpiryDate',
                             'StrExpiryDate', 'OI', 'COI', 'IV', 'VOL']
        else:
            fixed_columns = ['ScripName', 'StrikePrice', 'OptionType',
                                   'StrTradeDateTime', 'TradeDateTime', 'ExpiryDate',
                                   'StrExpiryDate', 'OI', 'COI', 'IV', 'VOL', 'OI_change', 'Flag']
        try:
            previous_df = self.objCommon.drop_extra_columns(previous_df, fixed_columns)
            df_now = self.objCommon.drop_extra_columns(df_now, fixed_columns)
            final = df_now.append(previous_df)
            return final
            # final.reset_index(inplace=True)
        except Exception as e:
            print('concat exception: ', e)

    def outliers_notify(self, df_now, previous_df, current_time, symbol, dt):
        try:
            if len(previous_df) >= edleConfig.no_of_past_instruments:
                value_list = list(previous_df['StrTradeDateTime'].unique())[:edleConfig.no_of_past_instruments]
                boolean_series = previous_df.StrTradeDateTime.isin(value_list)
                p_df = previous_df[boolean_series]
            else:
                p_df = previous_df
            p_df = p_df.loc[:, :'VOL']
            df_op = self.concate(p_df, df_now)
            new_df = self.cal_change_OI(df_op, current_time, symbol, dt)
            df_now = new_df[:len(df_now)]
            result = self.concate(previous_df, df_now, False)
            return result
        except Exception as e:
            print('Exception in outliers notify:', e)
            return previous_df


    def notify_process(self, df, x, symbol, expiry_date):
        try:
            old_COI = df['COI'].iloc[x + 1]
            current_coi = df['COI'].iloc[x]
            dt = df['StrTradeDateTime'].iloc[x]
            s = df['StrikePrice'].iloc[x]
            option_type = df['OptionType'].iloc[0]
            list_to_write = [dt, symbol, expiry_date, option_type, s, old_COI, current_coi]
            self.objSheet.writeSheet('CIEnotifications', list_to_write, 'EdelweissNotify')
        except Exception as e:
            print('Exception in outliers Notification Process:', e)













    # def notify_process(self, df, symbol, option_type, expiry_date):
    #     try:
    #         df = df[df['OptionType'] == option_type]
    #         time = df['StrTradeDateTime'].iloc[0]
    #         StrikePriceList = df[df['StrTradeDateTime'] == time]['StrikePrice']
    #         sl = StrikePriceList.to_list()
    #         for s in sl:
    #             # list_to_write = []
    #             temp = df[df['StrikePrice'] == s]
    #             #print(s)
    #             if len(temp.index) >= 10:
    #                 temp = temp[:10]
    #                 # calculate new column
    #                 temp = self.cal_change_OI(temp)
    #                 # print(temp.head())
    #                 current_coi = temp['COI'].to_list()[0]
    #                 dt = temp['StrTradeDateTime'].to_list()[0]
    #                 temp.dropna(inplace=True)
    #                 ll = temp['OI_change'].to_list()
    #                 old_oi_change = ll[0]
    #                 # print(old_oi_change)
    #                 list_of_outliers = self.cal_outliers(ll)
    #                 # print(list_of_outliers)
    #                 if len(list_of_outliers) > 0:
    #                     if old_oi_change in list_of_outliers:
    #                         old_coi = temp['COI'].to_list()[0]
    #                         list_to_write = [dt, symbol, expiry_date, option_type, s, old_coi, current_coi]
    #                         self.objSheet.writeSheet('CIEnotifications', list_to_write, 'EdelweissNotify')
    #     except Exception as e:
    #         print('Exception in outliers Notification Process:', e)

    # def outliers_notify_old(self, df, symbol, expiry_date):
    #     #result, symbol, expiry_date
    #     try:
    #         self.notify_process(df, symbol, 'CE', expiry_date)
    #         self.notify_process(df, symbol, 'PE', expiry_date)
    #     except Exception as e:
    #         print('Exception in outliers Notification:', e)



