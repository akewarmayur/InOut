from selenium import webdriver
import valuepickrconfig as config
import os
import time
import mysql_db as db
# Import the argparse library
import argparse


class ValuePickrGetLinks():

    def __init__(self):
        # initialize driver
        self.chromedriver = os.getcwd() + config.DRIVER_PATH

        # create driver object
        self.driver = webdriver.Chrome(self.chromedriver)
        self.driver.maximize_window()

    def close_driver(self):
        self.driver.close()

    def bottom_down(self):
        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def loopthrough_read_div(self):
        lnksLst = []
        time.sleep(1)
        containers = self.driver.find_elements_by_class_name(config.DIV_LIST)
        self.driver.find_elements_by_class_name('fps-result')
        self.bottom_down()
        fps_results = self.driver.find_elements_by_class_name('fps-result')
        for i in range(1, len(fps_results) + 1):
            topics = self.driver.find_elements_by_xpath("//*[@id='ember55']/div[" + str(i) + "]/div[2]/div[1]")
            for topic in topics:
                lnks = topic.find_element_by_tag_name(config.DIV_LIST_ANCHOR).get_attribute('href')
                topicTitles = topic.find_element_by_class_name("topic-title").text
                print(lnks,topicTitles)
                db.insertTopic(topicTitles, lnks)
                lnksLst.append((topicTitles,lnks))

        # for item in containers:
        #     lnks = item.find_element_by_tag_name(config.DIV_LIST_ANCHOR)
        #     # traverse list
        #     # print(lnks.get_attribute(config.DIV_LIST_ANCHOR_GET_ARTIBUTE_PROP))
        #     lnksLst.append(lnks.get_attribute(config.DIV_LIST_ANCHOR_GET_ARTIBUTE_PROP))

        # for i in range(5):
        #     for item in containers:
        #         lnks = item.find_element_by_tag_name(config.DIV_LIST_ANCHOR)
        #         # traverse list
        #         #print(lnks.get_attribute(config.DIV_LIST_ANCHOR_GET_ARTIBUTE_PROP))
        #         lnksLst.append(lnks.get_attribute(config.DIV_LIST_ANCHOR_GET_ARTIBUTE_PROP))
        #
        #     time.sleep(1)
        #     self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # '//*[@id="ember55"]/div[1]'

        # print(len(set(lnksLst)))

        return lnksLst

    # call browser + serach box
    def browser_call(self, parameter):
        url = config.URL
        self.driver.get(url)
        self.search_box(parameter)

    ## insert value on search box and click
    def search_box(self, parameter):
        try:
            self.driver.find_element_by_xpath(config.SEARCH_BOX_XPATH).send_keys(parameter)
            self.driver.find_element_by_xpath(config.SEARCH_BOX_BUTTON_CLICK).click()
            lst = self.loopthrough_read_div()
            print(lst)
        except Exception as e:
            print("Error======", e)
        # driver close
        # self.close_driver()

    def run(self, urlQuery):
        self.browser_call(urlQuery)


if __name__ == '__main__':
    obj = ValuePickrGetLinks()
    # # Create the parser
    # my_parser = argparse.ArgumentParser(description='date structure format eg. 2021-04-01')
    #
    # # Add the arguments
    # my_parser.add_argument('Date',
    #                        metavar='date',
    #                        type=str,
    #                        help='valuePickr Date')
    #
    # # Execute the parse_args() method
    # args = my_parser.parse_args()
    #
    # input_date = args.Date
    input_date='2021-05-13'
    print("input_date=========", input_date)
    queryParameter = config.QUERY_PARAMETER + input_date
    print(queryParameter)
    obj.run(queryParameter)
