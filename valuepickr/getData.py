from selenium import webdriver
import valuepickrconfig as config
import os
import time
import mysql_db as db
# Import the argparse library
import argparse
#from valuepickr.process_links import ValuePickrProcess
from process_links import ValuePickrProcess
from webdriver_manager.chrome import ChromeDriverManager

# create object
obj_vp = ValuePickrProcess()

class ValuePickrGetLinks():

    def __init__(self):
        # initialize driver
        self.chromedriver = os.getcwd() + config.DRIVER_PATH

        # create driver object
        ## link https://stackoverflow.com/questions/60296873/sessionnotcreatedexception-message-session-not-created-this-version-of-chrome/62127806
        self.driver = webdriver.Chrome(self.chromedriver)
        #self.driver = webdriver.Chrome(ChromeDriverManager().install())
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
        fps_results = self.driver.find_element_by_class_name('fps-result-entries')
        fps_results=fps_results.find_elements_by_class_name('fps-result')
        for fps in fps_results:
            topicTitles= fps.find_element_by_partial_link_text('a').text
            lnks= fps.find_element_by_partial_link_text('a').get_attribute('href')
            print(lnks, topicTitles)
            db.insertTopic(topicTitles, lnks)
            lnksLst.append((topicTitles,lnks))


            # lnksLst.append((topicTitles,lnks))
            # for topic in topics:
            #     lnks = topic.find_element_by_tag_name(config.DIV_LIST_ANCHOR).get_attribute('href')
            #     topicTitles = topic.find_element_by_class_name("topic-title").text
            #     print(lnks,topicTitles)
            #     db.insertTopic(topicTitles, lnks)
            #     lnksLst.append((topicTitles,lnks))

        ## Start parsing
        if len(lnksLst) > 0:
            self.topic_processes(lnksLst)
        else:
            lnksLst.append("Data not Found!!")

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

    def run_process(self, urlQuery):
        self.browser_call(urlQuery)

    def topic_processes(self, topicslst):
        try:
            for topic in topicslst:
                try:
                    topics = db.getReadTopic(topic[1], topic[0])

                    obj_vp.run(self.driver,topics[0][0], topics[0][2])
                except Exception as e:
                    print("inner topic processing error==",e)
        except Exception as e:
            print("outer topic processing error==",e)

if __name__ == '__main__':
    obj = ValuePickrGetLinks()
    # Create the parser
    my_parser = argparse.ArgumentParser(description='date structure format eg. 2021-04-01')

    # Add the arguments
    my_parser.add_argument('Date',
                           metavar='date',
                           type=str,
                           help='valuePickr Date')

    # Execute the parse_args() method
    args = my_parser.parse_args()

    input_date = args.Date
    #input_date='2021-08-23'
    #print("input_date=========", input_date)
    queryParameter = config.QUERY_PARAMETER + input_date
    print(queryParameter)
    obj.run_process(queryParameter)
