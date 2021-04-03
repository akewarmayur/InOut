import numpy as np
from common.sheetOperations import SheetOps
import warnings
warnings.filterwarnings("ignore")

class HelpEd:

    def __init__(self):
        self.objSheet = SheetOps()

    def cal_outliers(self, lst):
        mn = np.mean(lst)
        sd = np.std(lst)
        final_list = [x for x in lst if (x > mn - 2 * sd)]
        final_list = [x for x in final_list if (x < mn + 2 * sd)]
        list_of_outliers = list(set(lst) - set(final_list))
        # print('outliers:', list_of_outliers)
        return list_of_outliers

    def cal_change_OI(self, df):
        df['OI_change'] = 0
        for i, columnData in enumerate(df['OI']):
            if i == 0:
                df['OI_change'].iloc[i] = None
            else:
                temp = columnData - df['OI'].iloc[i - 1]
                df['OI_change'].iloc[i] = temp
        return df

    def notify_process(self, df, symbol, option_type, expiry_date):
        try:
            df = df[df['OptionType'] == option_type]
            time = df['StrTradeDateTime'].iloc[0]
            StrikePriceList = df[df['StrTradeDateTime'] == time]['StrikePrice']
            sl = StrikePriceList.to_list()
            for s in sl:
                # list_to_write = []
                temp = df[df['StrikePrice'] == s]
                print(s)
                if len(temp.index) >= 10:
                    temp = temp[:10]
                    # calculate new column
                    temp = self.cal_change_OI(temp)
                    # print(temp.head())
                    current_coi = temp['COI'].to_list()[0]
                    dt = temp['StrTradeDateTime'].to_list()[0]
                    temp.dropna(inplace=True)
                    ll = temp['OI_change'].to_list()
                    old_oi_change = ll[0]
                    # print(old_oi_change)
                    list_of_outliers = self.cal_outliers(ll)
                    # print(list_of_outliers)
                    if len(list_of_outliers) > 0:
                        if old_oi_change in list_of_outliers:
                            old_coi = temp['COI'].to_list()[0]
                            list_to_write = [dt, symbol, expiry_date, option_type, s, old_coi, current_coi]
                            self.objSheet.writeSheet('CIEnotifications', list_to_write, 'EdelweissNotify')
        except Exception as e:
            print('Exception in outliers Notification Process:', e)

    def outliers_notify(self, df, symbol, expiry_date):
        #result, symbol, expiry_date
        try:
            self.notify_process(df, symbol, 'CE', expiry_date)
            self.notify_process(df, symbol, 'PE', expiry_date)
        except Exception as e:
            print('Exception in outliers Notification:', e)
