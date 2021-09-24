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
            #topicTitles= fps.find_element_by_partial_link_text('a').text
            topicTitles = fps.text.split('\n')[0]
            #print(topicTitles)
            #lnks= fps.find_element_by_partial_link_text('a').get_attribute('href')
            lnks = fps.find_elements_by_class_name('topic a')[0].get_attribute('href')
            print(lnks, topicTitles)
            record_count = db.check_topic_details(topicTitles)
            if record_count[0][0] == 0:
                lnks= lnks.replace(lnks.split("/")[-1], "1")
                db.insertTopic(topicTitles, lnks)

            lnksLst.append((topicTitles, lnks))

        ## lnks="https://forum.valuepickr.com/t/vaibhav-global-back-from-the-dead/960/371"
        ## lnksLst.append(('Vaibhav Global : Back from the dead', lnks))

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
            #print(lst)
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
                    topics = db.getReadTopic(topic[0])
                    latest_URL_last_count = int(topic[1].split("/")[-1]) ## new url
                    old_db_URL_last_count = int(topics[0][2].split("/")[-1]) ## old or db url

                    url_link=""
                    if old_db_URL_last_count == latest_URL_last_count:
                        url_link = topic[1]
                        print("No change in URL of {}=============".format(topic[0]))
                        continue
                    else:
                        if old_db_URL_last_count > latest_URL_last_count:
                            print("No change in URL of {}=============".format(topic[0]))
                            continue
                        else:
                            diff_value_count= latest_URL_last_count-old_db_URL_last_count
                            if diff_value_count <= 20:
                                print("No change in URL of {}=============".format(topic[0]))
                                continue
                            else:
                                url_link = topic[1].replace(topic[1].split("/")[-1], str(old_db_URL_last_count))
                    #obj_vp.run(self.driver,topics[0][0], topics[0][2])

                    num_value= obj_vp.run_with_html_view(topics[0][0], url_link)
                    #url_first = topics[0][2]
                    # url_first = url_link
                    # url_update = topics[0][2].replace(topics[0][2].split("/")[-1], str(num_value))
                    url_update = url_link.replace(url_link.split("/")[-1], str(num_value))
                    db.update_url(url_update,topics[0][2]) ## update url
                except Exception as e:
                    print("inner topic processing error==", e)
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
    # input_date='2021-08-26'
    queryParameter = config.QUERY_PARAMETER + input_date
    print(queryParameter)
    obj.run_process(queryParameter)
