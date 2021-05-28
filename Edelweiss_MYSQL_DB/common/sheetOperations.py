import pygsheets
import os
from pathlib import Path

class SheetOps:

    def __init__(self):
        self.srvFilePath = os.getcwd() + "/helpers/ck8sproject-e1fb187dcd6d.json"
        #self.srvFilePath = os.path.join(Path(__file__).cwd(), "/InOut/helpers/ck8sproject-e1fb187dcd6d.json")

    def readSheet(self, spreadsheet_name, sheet_name, machine_name=None):
        try:
            filenameToRead = spreadsheet_name
            # Authorization7
            gc = pygsheets.authorize(service_file=self.srvFilePath)
            # Open the google spreadsheet
            sh = gc.open(filenameToRead)
            # Define which sheet to open in the file
            wks = sh.worksheet_by_title(sheet_name)
            # Get the data from the Sheet into python as DF
            if machine_name == None:
                content = wks.get_as_df(has_header=True)
            else:
                content = wks.get_as_df(has_header=True)
                content = content[content.MachineName == machine_name]
            return content
        except Exception as exReadSheet:
            print('Exception in Reading Spreadsheet: ',exReadSheet)
            return None

    def readSheetColumns(self, content, column_name):
        try:
            column_content = content[column_name]
            return list(column_content)
        except Exception as e:
            print('Exception in reading column content: ', e)
            return None

    def writeSheet(self, filenameToRead, list_to_write, sheet_name):
        try:
            gc = pygsheets.authorize(service_file=self.srvFilePath)
            sh = gc.open(filenameToRead)
            wks = sh.worksheet_by_title(sheet_name)
            wks.update_row(len(wks.get_values('A', 'A1')) + 1, list_to_write)
            return True
        except Exception as e:
            print('Exception in writing sheet: ', e)
            return False