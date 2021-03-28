from common.sheetOperations import SheetOps
from scrapIn import ScrapData
from common.common import CommonFunctions
from common.gAPI import GoogleAPI
from Investing.helpers import Help
import pandas as pd

class ProcessIn:

    def __init__(self):
        self.resolution_dict = {'CONFIG_5MIN': 5, 'CONFIG_15MIN': 15, 'CONFIG_30MIN': 30,
                       'CONFIG_2H': 120, 'CONFIG_1D': 'D', 'CONFIG_1W': 'W', 'CONFIG_1M': 'M'}
        self.objSheet = SheetOps()
        self.objScrap = ScrapData()
        self.objCommon = CommonFunctions()
        self.objGAPI = GoogleAPI()
        self.objHelp = Help()

    def get_url(self):
        for _ in range(5):
          token = str(self.objScrap.get_token())
          if token != 'None':
            break
        URL= 'https://tvc4.forexpros.com/'+str(token)+'/1615191589/56/56/23/history?'
        print(URL)
        return URL

    def readSymbol(self, pidValue):
        try:
            content = self.objSheet.readSheet('CIEconfig', 'InvestingStocks')
            content = content.loc[content['Pid'] == pidValue]
            return content['Symbol'].values.tolist()
        except Exception as exReadSheet:
            print(exReadSheet)

    def concate(self, previous_df, df_now):
        previous_df = self.objCommon.drop_extra_columns(previous_df, self.objHelp.fixed_columns)

        df_new = previous_df.loc[:, :'volume']

        if len(df_new.index) >= 200:
            slice = df_new.iloc[:200]
        else:
            slice = df_new.iloc[:len(previous_df.index)]

        result = df_now.append(slice)
        result.reset_index(inplace=True)

        # calculate indicators
        result = self.objScrap.cal_indicators(result, ha=True, all=True)

        del_200 = previous_df.iloc[200:]
        final = result.append(del_200)
        final.reset_index(inplace=True)

        return final

    def get_outliers_200(self, df, column_name):
        df_new = df.loc[:, :'volume']
        if len(df_new.index) > 200:
            df_new = df_new.head(200)

        df_new = self.objScrap.cal_indicators(df_new, ha=False, all=False)

        mn = df_new[column_name].mean()
        sd = df_new[column_name].std()
        final_list = [x for x in df_new[column_name] if (x > mn - 2 * sd)]
        final_list = [x for x in final_list if (x < mn + 2 * sd)]
        list_of_outliers = list(set(df_new[column_name].values.tolist()) - set(final_list))
        return sorted(list_of_outliers, reverse=True)

    def start(self, machine_name):
        service = self.objGAPI.intiate_gdAPI()
        URL = self.get_url()
        if URL == 'None':
            URL = self.get_url()
        content = self.objSheet.readSheet('CIEconfig', 'InvestingConfig')
        no_of_days = content['Days']
        resolutions_list = content['Configuration']
        isMarketON = content['MarketON']
        isMarketON = isMarketON[0]
        print('To be Scrapped: ', resolutions_list)
        print('No of days: ', no_of_days)

        content = self.objSheet.readSheet('CIEconfig', 'InvestingStocks', machine_name)
        content = content['Pid']
        content = content.values.tolist()
        pid = [row for row in content if row != '']
        if len(pid) == 0:
            print('No stocks are available in the list to scrap data')
        else:
            try:
                for PID in pid:
                    symbl = self.readSymbol(PID)
                    symbl = symbl[0]
                    name_of_stock = symbl
                    for i, item in enumerate(resolutions_list):
                        resolution = self.resolution_dict[item]

                        file = 'csv/' + str(name_of_stock) + '_' + str(resolution) + '.csv'
                        file_to_save = 'd_csv/' + str(name_of_stock) + '_' + str(resolution) + '.csv'
                        # check the historic data is available for the stock
                        isDataAvailable, file_id = self.objHelp.check_previous_data_exist(file)
                        print('Is Data Available:', isDataAvailable)

                        if isDataAvailable == False:
                            # URL, PID, symbl, row, end_date, no_of_days)
                            status = self.objScrap.scrap(URL, PID, symbl, item, 0, no_of_days[i])
                            # calculate indicators and upload to drive
                            data = pd.read_csv(file, parse_dates=['datetime'])

                            # data.reset_index(drop=True, inplace=True)

                            data = self.objScrap.cal_indicators(data, ha=True, all=True)
                            # data = objIndicators.cal_heiken_ashi(data)

                            outliers_close = self.get_outliers_200(data, 'close')
                            outliers_volume = self.get_outliers_200(data, 'volume')
                            outliers_per = self.get_outliers_200(data, 'per_change_count')

                            print(f"close outliers on first 200 Candles: {outliers_close} ")
                            print(f"volume outliers on first 200 Candles: {outliers_volume} ")
                            print(f"per_change_count outliers on first 200 Candles: {outliers_per} ")

                            # writesheet(Symbol, timenow, Name, Res, Outliers_Close, Outliers_Volume, Outliers_per_change_count)
                            # objScrapData.writesheet(str(PID), name_of_stock, objScrapData.convertUTC_IST(), str(resolution),
                            #                         str(outliers_close), str(outliers_volume), str(outliers_per))

                            # Upload to drive based on condition
                            if isMarketON == 'FALSE':
                                self.objHelp.save_to_drive(data, file)

                        elif isDataAvailable == True:
                            # Download File in Local directory
                            self.objGAPI.download_files(service, file_to_save, file_id, False)
                            previous_data = pd.read_csv(file_to_save, parse_dates=['datetime'])
                            previous_data.head()
                            end_date = self.objHelp.get_end_date(previous_data)
                            # print('End Date of Data=> ', end_date)
                            # print(data.head(5))

                            # Scrap Todays data as per config sheet and save in 'csv' local folder
                            status = self.objScrap.scrap(URL, PID, symbl, item, 0, no_of_days[i])
                            if status == True:
                                current_data = pd.read_csv(file, parse_dates=['datetime'])
                                current_data.head()
                                data = self.concate(previous_data, current_data)
                                # data.reset_index(drop=True, inplace=True)
                                outliers_close = self.get_outliers_200(data, 'close')
                                outliers_volume = self.get_outliers_200(data, 'volume')
                                outliers_per = self.get_outliers_200(data, 'per_change_count')

                                print(f"close outliers on first 200 Candles: {outliers_close} ")
                                print(f"volume outliers on first 200 Candles: {outliers_volume} ")
                                print(f"per_change_count outliers on first 200 Candles: {outliers_per} ")

                                # objScrapData.writesheet(str(PID), name_of_stock, objScrapData.convertUTC_IST(), str(resolution),
                                #                         str(outliers_close), str(outliers_volume), str(outliers_per))

                                if isMarketON == 'FALSE':
                                    self.objHelp.save_to_drive(data, file)
                            else:
                                print('No Data available in the given range of date')

                        else:
                            print('Something is Wrong, Try Again')
            except Exception as e:
                print(e)

        # if isMarketON == 'TRUE':
        #     objRun.save_to_drive_at_once()
if __name__ == '__main__':
    obj = ProcessIn()
    obj.start('Mayur')