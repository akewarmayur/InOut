from common.gAPI import GoogleAPI
import time
import glob


class CommonFunctions:

    def __init__(self):
        self.objGAPI = GoogleAPI()

    def drop_extra_columns(self, df, fixed_columns):
        try:
            list_of_columns = df.columns.tolist()
            extra_columns = list(set(list_of_columns) - set(fixed_columns))
            try:
                df.drop(extra_columns, axis=1, inplace=True)
            except:
                pass
        except Exception as e:
            print('Exception while dropping extra columns', e)
        return df


    def check_previous_data_exist(self, file_path, folder_id):
        try:
            name_of_file = file_path.split('/')[1]
            service = self.objGAPI.intiate_gdAPI()
            file_id = self.objGAPI.search_file(service, name_of_file, "text/csv", folder_id, True)
            if type(file_id) is str:
                return True, file_id
            else:
                return False, file_id
        except Exception as e:
            print('Exception while checking previous data exist', e)
            return None

    def get_list_of_csv_files_in_folder(self, folder_name):
        list_of_files = []
        try:
            for file in glob.glob(folder_name + '/*.csv'):
                list_of_files.append(file)
            return list_of_files
        except Exception as e:
            print('Exception in getting list of files', e)
            return list_of_files

    def get_outliers(self, df, column_name):
        try:
            mn = df[column_name].mean()
            sd = df[column_name].std()
            final_list = [x for x in df[column_name] if (x > mn - 2 * sd)]
            final_list = [x for x in final_list if (x < mn + 2 * sd)]
            list_of_outliers = list(set(df[column_name].values.tolist()) - set(final_list))
            return sorted(list_of_outliers, reverse=True)
        except Exception as e:
            print('Exception in getting list of files', e)
            return []

