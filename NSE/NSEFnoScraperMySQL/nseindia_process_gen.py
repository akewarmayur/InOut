from selenium import webdriver
import os
import argparse
import shutil
import time
import zipfile
import datetime
from selenium.webdriver.chrome.options import Options
import getpass
import mysql_connector as db

Username = getpass.getuser()
options = Options()
prefs = {"download.default_directory" : "C:\\Users\\" + Username + "\\Downloads\\"}
options.add_experimental_option("prefs",prefs)
options.add_argument('disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
options.add_argument('--headless')

class FavCopy():

    def __init__(self):
        # initialize driver
        self.chromedriver = os.getcwd() + "\\driver\\chromedriver.exe"

        # create driver object
        self.driver = webdriver.Chrome(self.chromedriver,chrome_options=options)
        #self.driver = webdriver.Chrome(self.chromedriver)
        self.driver.maximize_window()

    def close_driver(self):
        self.driver.close()

    def extarcted_files(self, filepath,directory_to_extract_to):
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(directory_to_extract_to)

    def deleteFiles(self,filePath):
        # zip
        try:
            # zip
            if os.path.exists(filePath):
                os.remove(filePath)
                # print("delete files")
            # csv
            filecsv = filePath[0:-4]
            # print(filecsv)
            if os.path.exists(filePath):
                os.remove(filePath)
                # print("delete files")
        except Exception as e:
            print(e)

    def run(self,url,input_date):
        self.driver.get(url)
        try:

            hrefurl= self.driver.find_element_by_xpath('/html/body/table/tbody/tr[1]/td/a').click()
            filename=self.driver.find_element_by_xpath("/html/body/table").text
            #print("filename====",filename)
            #print("hrefurl=======",hrefurl)
            readPath = "C:\\Users\\" + Username + "\\Downloads\\"+filename
            dest= os.getcwd() +"\\contents\\"
            time.sleep(4)
            filePath= os.getcwd() +"\\contents\\"+filename
            print("filePath==",filePath)
            # zip
            self.deleteFiles(filePath)

            time.sleep(1)
            shutil.move(readPath,dest)
            self.extarcted_files(filePath,dest)
            print("Done extraction csv file!!")
            self.close_driver()
            ## file path
            #favcopyPath = 'D:/Projects/django_projects/API_tele/nseindia/contents/fo11MAY2021bhav.csv'
            favcopyPath = os.getcwd() + "\\contents\\" + filename
            favcopyPath=favcopyPath[0:-4]
            csvPath=favcopyPath
            favcopyPath=favcopyPath.replace('\\', '/')
            print(favcopyPath)
            db.insertFno(favcopyPath,input_date)
            #exit()
            # Delete
            # zip
            if os.path.exists(filePath):
                os.remove(filePath)
                os.remove(csvPath)



        except Exception as e:
            print("No file ==",e)

if __name__=='__main__':
    obj=FavCopy()
    # Create the parser
    my_parser = argparse.ArgumentParser(description='date structure format eg. 07-05-2021')
    today_date = str(datetime.date.today())
    print("===================",today_date)
    #today_date_value= today_date.day + today_date.month + today_date.year
    date_object = datetime.datetime.strptime(today_date, "%Y-%m-%d").strftime("%d-%m-%Y")
    print("today_date_value==",date_object)
    # Add the arguments
    my_parser.add_argument('Date',
                           metavar='date',
                           type=str,
                           help='valuePickr Date',nargs='?',
                           default=date_object)


    # Execute the parse_args() method
    args = my_parser.parse_args()

    input_date = args.Date
    if input_date == "":
        input_date=date_object

    # https://www1.nseindia.com/ArchieveSearch?h_filetype=fobhav&date=11-05-2021&section=FO
    #input_date='11-05-2021'
    url="https://www1.nseindia.com/ArchieveSearch?h_filetype=fobhav&date="+str(input_date)+"&section=FO"
    print("url====",url)
    obj.run(url,input_date)
    #obj.close_driver()