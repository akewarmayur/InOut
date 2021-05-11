import datetime
import pandas as pd
import glob
import time
from pytz import timezone
from common.common import CommonFunctions
import warnings
import os
from common.gAPI import GoogleAPI
from datetime import timedelta

warnings.filterwarnings("ignore")


class Help:

    def __init__(self):
        self.objCommon = CommonFunctions()
        self.objGAPI = GoogleAPI()
        self.fixed_columns = ['datetime', 'symbol', 'pid', 'resolution', 'open', 'close', 'high', 'low', 'volume', 'EMA_50', 'EMA_100', 'EMA_200',
             'BBL_14_2.0', 'BBM_14_2.0', 'BBU_14_2.0', 'BBB_14_2.0', 'RSI_14', 'PSARl_0.02_0.2', 'PSARs_0.02_0.2',
             'PSARaf_0.02_0.2', 'PSARr_0.02_0.2', 'ISA_9', 'ISB_26', 'ITS_9', 'IKS_26', 'ICS_26',
             'per_change', 'volume_high_count', 'close_count', 'per_change_count', 'ha_close', 'ha_open', 'ha_high',
             'ha_low']

    def get_end_date(self, df):
        end_d = df['datetime'].iloc[0]
        print('Last Date of scrapped data=> ', end_d)
        end_date = datetime.datetime.timestamp(end_d)
        #print('End date timestamp=> ', end_date)
        return int(end_date)

    def cvtDateTimeToNumber(self, dtime):
        element = datetime.datetime.strptime(dtime, "%Y-%m-%d %H:%M:%S")
        timestamp = datetime.datetime.timestamp(element)
        return int(timestamp)

    def cvtNumberToDateTime(self, timestamp):
        dt = datetime.datetime.fromtimestamp(timestamp)
        format = "%YYYY-%mm-%dd %HH:%MM:%SS" #YYYY-MM-DD HH:MI:SS
        # Convert to Asia/Kolkata time zone
        now_asia = dt.astimezone(timezone('Asia/Kolkata'))
        tt = now_asia.strftime(format)
        dat = datetime.datetime.strptime(tt, '%YYYY-%mm-%dd %HH:%MM:%SS')
        return dat

    def cvtNumberToDateTimeWeek(self, timestamp):
        dt = datetime.datetime.fromtimestamp(timestamp)
        format = "%YYYY-%mm-%dd 00:00:00" #YYYY-MM-DD HH:MI:SS
        # Convert to Asia/Kolkata time zone
        now_asia = dt.astimezone(timezone('Asia/Kolkata'))
        tt = now_asia.strftime(format)
        dat = datetime.datetime.strptime(tt, '%YYYY-%mm-%dd 00:00:00')
        dat = dat + timedelta(days=1)
        return dat

    def cvtNumberToDateTimeDay(self, timestamp):
        dt = datetime.datetime.fromtimestamp(timestamp)
        format = "%YYYY-%mm-%dd 00:00:00" #YYYY-MM-DD HH:MI:SS
        # Convert to Asia/Kolkata time zone
        now_asia = dt.astimezone(timezone('Asia/Kolkata'))
        tt = now_asia.strftime(format)
        dat = datetime.datetime.strptime(tt, '%YYYY-%mm-%dd 00:00:00')
        return dat


    def convertUTC_IST(self):
        format = "%Y-%m-%d %H:%M:%S"
        # Current time in UTC
        now_utc = datetime.datetime.now(timezone('UTC'))
        # print(now_utc.strftime(format))
        # Convert to Asia/Kolkata time zone
        now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
        #print(now_asia)
        tt = now_asia.strftime(format)
        tod = datetime.datetime.strptime(tt, '%Y-%m-%d %H:%M:%S')
        return tod

    def cnvNumber(self):
        tod = self.convertUTC_IST()
        # print("today: ", tod)
        timestamp = datetime.datetime.timestamp(tod)
        return int(timestamp)


    def cnvNumberWithDate(self, numofDays):
        tod = self.convertUTC_IST()
        backdate = datetime.timedelta(days = numofDays)
        next_date_time = tod - backdate
        # print("next date time :", next_date_time)
        timestamp = datetime.datetime.timestamp(next_date_time)
        return int(timestamp)

    def get_resolution_type(self, file_name):
        #1wyLQQLg-QKY5zrocxV6YQLhjknjUKLoX
        hh = file_name.split('_')[1]
        resolution_type = hh.split('.')[0]
        return resolution_type

    def get_folder_id(self, file):
        folder_id = 0
        name_of_file = file.split('csv/')[1]
        resolution_type = self.get_resolution_type(name_of_file)
        if resolution_type == 'D':
            folder_id = '1qOF0mqmrMwrY3HR0QEXpBZKI9n3F43WU'
        elif resolution_type == '5':
            folder_id = '1wyLQQLg-QKY5zrocxV6YQLhjknjUKLoX'
        elif resolution_type == '15':
            folder_id = '1cDUFrwXTU--3wjYn5FqSntuRJVOGjX17'
        elif resolution_type == '30':
            folder_id = '1jqHsMJ1o31fqZgCdS1FdbDgYNNMetV0F'
        elif resolution_type == '120':
            folder_id = '1k2-WNnkUpCbojqMjK5fmmuGHc9PtqWQ_'
        elif resolution_type == 'M':
            folder_id = '1GYM6931x31C_uWS4WZXfUKauP-2499qb'
        elif resolution_type == 'W':
            folder_id = '1nrnY93F32BUasJrqH_JcXxdqwlYc4CXu'
        elif resolution_type == '1':
            folder_id = 'ylOFW98i2OzQxjyH9aEAomZsJKZoJoAF'
        return folder_id

    def check_previous_data_exist(self, file_name):
        try:
            name_of_file = file_name.split('csv/')[1]
            service = self.objGAPI.intiate_gdAPI()
            folder_id = self.get_folder_id(file_name)
            file_id = self.objGAPI.search_file(service, name_of_file, "text/csv", folder_id, True)
            if type(file_id) is str:
                return True, file_id
            else:
                return False, file_id
        except Exception as e:
            print('Exception in checking previous data:', e)


    def save_to_drive(self, file):
        try:
            # temp = self.objCommon.drop_extra_columns(temp, self.fixed_columns)
            name_of_file = file.split('csv/')[1]
            # temp.to_csv(os.getcwd() + '/Investing/sample_data/' + name_of_file, index=False)
            destination = os.getcwd() + '/Investing/sample_data/' + name_of_file
            #resolution_type = self.get_resolution_type(name_of_file)
            folder_id = self.get_folder_id(file)
            service = self.objGAPI.intiate_gdAPI()
            # Search file id to check it is exists or not
            # def search_file(service, file_name, mime_type, folder_id, search_in_folder=False):
            file_id = self.objGAPI.search_file(service, str(name_of_file), 'text/csv', folder_id, True)
            if type(file_id) is int:
                self.objGAPI.upload_file(service, str(name_of_file), destination, folder_id, 'text/csv')
            if type(file_id) is str:
                self.objGAPI.delete_file(service, file_id)
                time.sleep(1)
                self.objGAPI.upload_file(service, str(name_of_file), destination, folder_id, 'text/csv')
        except Exception as e:
            print('Exception in saving data on drive:', e)

    def save_to_drive_at_once(self):
        for file in glob.glob('sample_data/*.csv'):
            file_id = 0
            temp = pd.read_csv(file, index_col=0)
            # print(temp.head(2))
            name_of_file = file.split('csv/')[1]
            destination = os.getcwd() + '/Investing/sample_data/sample_data/' + name_of_file
            resolution_type = self.get_resolution_type(name_of_file)
            folder_id = self.get_folder_id(file)
            service = self.objGAPI.intiate_gdAPI()
            # Search file id to check it is exists or not
            # def search_file(service, file_name, mime_type, folder_id, search_in_folder=False):
            file_id = self.objGAPI.search_file(service, str(name_of_file), 'text/csv', folder_id, True)
            if type(file_id) is int:
                self.objGAPI.upload_file(service, str(name_of_file), destination, folder_id, 'text/csv')
            if type(file_id) is str:
                self.objGAPI.delete_file(service, file_id)
                time.sleep(1)
                self.objGAPI.upload_file(service, str(name_of_file), destination, folder_id, 'text/csv')








