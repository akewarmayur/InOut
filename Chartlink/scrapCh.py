
import base64
import sys
import time
import pickle
from pyvirtualdisplay import Display
from selenium import webdriver
### Define modal here
import numpy as np
from common.sheetOperations import SheetOps
import config
from yoloPrediction import Yolo

class ScrapData:

    def __init__(self):
        self.objSheet = SheetOps()
        self.SheetName = 'CIEconfig'

    def setPrerequisite(driver, cmpName, range):
        display = Display(visible=0, size=(1400, 900))
        display.start()
        sys.path.insert(0, '/usr/lib/chromium-browser/chromedriver')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--start-maximized')
        driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
        objYolo = Yolo()
        # time.sleep(5)
        ## click on upper overlays
        driver.find_element_by_xpath(config.UPPER_OVERLAYS).click()
        print("clicking on upper overlays....done")
        # time.sleep(1)
        ## # identifying the checkbox with xpath, then click
        driver.find_element_by_xpath(config.BOLLINGER_BOND).click()
        driver.find_element_by_xpath(config.PARABOLIC_SAR).click()
        driver.find_element_by_xpath(config.ICHIMOKU_CLOUDS).click()
        print("clicking on upper overlays checked ....done")
        ## Drop down
        # time.sleep(2)

        # print("clicking on period....done")
        if range == '15minutes':
            driver.find_element_by_xpath(config.RANGE).click()
            driver.find_element_by_xpath(config.PERIOD_10DAYS).click()
        elif range == '5minutes':
            driver.find_element_by_xpath(config.RANGE_5MIN).click()
            driver.find_element_by_xpath(config.PERIOD_5DAYS).click()
        elif range == '30minutes':
            driver.find_element_by_xpath(config.RANGE_30MIN).click()
            driver.find_element_by_xpath(config.PERIOD_1MONTH).click()
        elif range == 'daily':
            # driver.find_element_by_xpath(RANGE_DAILLY).click()
            driver.find_element_by_css_selector(config.RANGE_DAILLY).click()
            driver.find_element_by_xpath(config.PERIOD_2YEARS).click()
        elif range == 'weekly':
            # driver.find_element_by_xpath(RANGE_WEEKLY).click()
            driver.find_element_by_css_selector("#d > option:nth-child(2)").click()
            driver.find_element_by_xpath(config.PERIOD_5YEARS).click()
        elif range == '2hours':
            driver.find_element_by_xpath(config.RANGE_120MIN).click()
            driver.find_element_by_xpath(config.PERIOD_2MONTHS).click()

        #
        driver.find_element_by_xpath(config.TYPE).click()
        # print("clicking on range and type....done")

        ## UPDATE Chart
        driver.find_element_by_xpath(config.UPDATE_CHART).click()

        ## click on button to downlaod the image
        # time.sleep(3)
        # WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, SWITCH_TO_IFRAME)))
        # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, IFRAME_BUTTON_CLICK))).click()
        iframe = driver.find_element_by_name("ChartImage")
        driver.switch_to.frame(iframe)
        imgstring = driver.find_element_by_id("cross").get_attribute("src")

        imgdata = base64.b64decode(imgstring.split(",")[1])
        jpg_as_np = np.frombuffer(imgdata, dtype=np.uint8)
        print("jpg_as_np===", jpg_as_np)
        val = objYolo.getPredictOutput(jpg_as_np, cmpName, range)
        print("val====", val)
        driver.switch_to.default_content()
        # img = cv2.imdecode(jpg_as_np, flags=1)
        # print("File has been downloaded...1")

        # self.driver.find_element_by_css_selector("#saverbutton").click()

    def scrap(self):
        # set the pyvirtualdisplay


        content = self.objSheet.readSheet(self.SheetName, 'ChartConfig')
        value = [row[1:] for row in content if row[0] == 'Resolution']
        value = value[0]
        print("value===", value)
        lst = []
        if len(value) > 2:
            value = value[0:2]
            return value
        else:
            return value

        content = self.objSheet.readSheet(self.SheetName, 'ChartStocks', config.machine_name)
        content = content['SID']


