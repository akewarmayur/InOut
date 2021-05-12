from selenium import webdriver
import valuepickrconfig as config
import os
import time
import mysql_db as db
import argparse

class ValuePickrProcess():

    def __init__(self):
        # initialize driver
        self.chromedriver = os.getcwd() + config.DRIVER_PATH

        # create driver object
        self.driver = webdriver.Chrome(self.chromedriver)
        self.driver.maximize_window()

    def close_driver(self):
        self.driver.close()

    def loopthrough_read_div(self):
        lnksLst=[]
        time.sleep(1)
        #containers = self.driver.find_elements_by_xpath("//*[@id='ember11']")
        containersPosts = self.driver.find_elements_by_xpath("//*[@id='ember11']/div[4]")
        ##containersPostStream= self.driver.find_elements_by_xpath("//*[@id='ember24']/div")
        for i in range(1, 100):
            try:

                s="//*[@id='post_"+str(i)+"']"
                print(s)
                lns= self.driver.find_element_by_xpath(s).text
                print(lns)
            except Exception as e:
                print(e)

        # for item in containersPosts:
            # for i in range(1,100):
            #     s="//*[@id='post_"+str(i)+"']/div/div[2]/div[1]"
            #     print(s)
            #     lnks= item.find_element_by_xpath(s).text
            #     print(lnks)

            # lnks = self.driver.find_element_by_xpath("//*[@id='post_1']/div/div[2]/div[1]").text
            # print(lnks)
            #
            # lnks1 = self.driver.find_element_by_xpath("//*[@id='post_2']/div/div[2]/div[1]").text
            # print(lnks1)
            # rows = item.find_elements_by_class_name("row")
            # number_of_rows = len(rows)
            # print("number_of_rows===",number_of_rows)

        #return lnksLst


    def run(self,topicid,parameter):
        self.driver.get(parameter)
        # To scroll top of the page
        for i in range(5):
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)

        # Category name
        # categoryName= self.driver.find_element_by_xpath(config.CATEGORY_NAME_XPATH).text
        # print(categoryName)
        categoryName = self.driver.find_element_by_class_name('topic-category').text
        #categoryName = categoryName.replace("\n", ",")
        try:

            categorys = categoryName.split('\n')
            # insertTopicCategory
            for category in categorys:
                db.insertTopicCategory(topicid,category)
        except Exception as e:
            print("Category parsing issue===:", e)
        # to scroll to bottom
        #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #self.loopthrough_read_div()

        webclientLst=[]
        crawler_post = self.driver.find_elements_by_class_name('topic-body')
        for crawler in crawler_post:
            metas = crawler.find_elements_by_class_name('topic-meta-data')
            for row in metas:
                userName = row.find_element_by_tag_name('a').text
                #user_post_date = row.find_element_by_class_name('post-infos').text
                user_post_date = row.find_element_by_css_selector('.relative-date').get_attribute('title')
                print(userName,user_post_date)
                db.insertUser(userName)
                print("==========")
                ## contents
            cooked = crawler.find_elements_by_css_selector('.contents')
            for cook in cooked:
                user_post_desc = cook.find_element_by_tag_name('div').text
                #print(user_post_desc)
                print("==================================================")
                #print(cooked)
                ## Add userId
                checkUserId = db.getUserDetails(userName)
                checkUserId = checkUserId[0][0]
                webclientLst.append((checkUserId,userName, user_post_date,user_post_desc))
                #print("===================================================")

        SCROLL_PAUSE_TIME = 0.5
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        print("last_height=========", last_height)
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            print("last_height=========", new_height)
            if new_height == last_height:
                break
            last_height = new_height
            ### topic-body crawler-post
            crawler_post = self.driver.find_elements_by_class_name('topic-body')
            for crawler in crawler_post:
                metas = crawler.find_elements_by_class_name('topic-meta-data')
                for row in metas:
                    userName = row.find_element_by_tag_name('a').text
                    # user_post_date = row.find_element_by_class_name('post-infos').text
                    user_post_date = self.driver.find_element_by_css_selector('.relative-date').get_attribute(
                        'title')
                    print(userName, user_post_date)
                    db.insertUser(userName)
                    print("==========")
                    ## contents
                cooked = crawler.find_elements_by_css_selector('.contents')
                for cook in cooked:
                    user_post_desc = cook.find_element_by_tag_name('div').text
                    # print(user_post_desc)
                    print("==================================================")
                    # print(cooked)
                    ## Add userId
                    checkUserId = db.getUserDetails(userName)
                    checkUserId = checkUserId[0][0]
                    webclientLst.append((checkUserId, userName, user_post_date, user_post_desc))

        ## check to till bottom
        # for i in range(1,10):
        #     self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     time.sleep(2)
        #     crawler_post = self.driver.find_elements_by_class_name('topic-body')
        #     for crawler in crawler_post:
        #         metas = crawler.find_elements_by_class_name('topic-meta-data')
        #         for row in metas:
        #             userName = row.find_element_by_tag_name('a').text
        #             #user_post_date = row.find_element_by_class_name('post-infos').text
        #             user_post_date = self.driver.find_element_by_css_selector('.relative-date').get_attribute('title')
        #             db.insertUser(userName)
        #         cooked = crawler.find_elements_by_css_selector('.contents')
        #         for cook in cooked:
        #             user_post_desc = cook.find_element_by_tag_name('div').text
        #             print(user_post_desc)
        #             print("===========================================")
        #             ## Add userId
        #             checkUserId = db.getUserDetails(userName)
        #             checkUserId = checkUserId[0][0]
        #             webclientLst.append((checkUserId,userName, user_post_date, user_post_desc))
        #print(set(webclientLst))
        for row in webclientLst:
            db.insertTopicDiscussion(topicid,row[0],row[3],row[2])

    def bottom_down(self):
        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        print("last_height=========",last_height)
        while True:

            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            print("last_height=========", new_height)
            if new_height == last_height:
                break
            last_height = new_height



if __name__=='__main__':

    try:
        # Create the parser
        my_parser = argparse.ArgumentParser(description='date structure format eg. 2021-04-01')

        # Execute the parse_args() method
        args = my_parser.parse_args()
        # create a object
        obj = ValuePickrProcess()
        ## read topics
        topics = db.getReadTopic()

        try:
            for topic in topics:
                #print(topic[0],topic[2])
                obj.run(topic[0],topic[2])
                exit()
        except Exception as e:
            print("Innner Error===", e)

    except Exception as e:
        print("Outer Error===", e)


