## Import libaries
import requests
from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
import time
import mysql_db as db

# pip install html5lib
# pip install bs4
# pip install requests


def check_record_is_exist(check_status):
    return check_status

def get_url_parse(url,check_num_for_category,topicid):
    check_status = 0
    r = requests.get(url)
    # time.sleep(1)
    soup = BeautifulSoup(r.content,'html5lib')  # If this line causes an error, run 'pip install html5lib' or install html5lib
    quotes = []  # a list to store quotes
    ## find the category
    topic_category = soup.find_all('div', attrs={'class': 'topic-category'})
    ## stock category find
    if int(check_num_for_category) == 1:
        try:

            category_name_first = topic_category[0]('span', attrs={'class': 'category-name'})[0].text
            category_name_second = topic_category[0]('span', attrs={'class': 'category-name'})[1].text
            db.insertTopicCategory(topicid, category_name_first) # stocks
            db.insertTopicCategory(topicid, category_name_second) # desc
        except Exception as e:
            pass

    ##
    table = soup.find_all('div', attrs={'class': 'topic-body crawler-post'})
    #for i in range(20):
    for rows in table:
        ## description
        try:
            ### Creator
            creator = rows.find_all('span', attrs={'class': 'creator'})
            creator = " ".join((creator[0].text).replace("\n", "").split())
            ## Date time
            datemodified = rows('span', attrs={'class': 'crawler-post-infos'})
            postdate = datetime.datetime.strptime(datemodified[0].meta['content'], "%Y-%m-%dT%H:%M:%SZ")
            postdate = postdate + timedelta (hours=5,minutes=30)
            row =rows('div',attrs={'class': 'post'})
            desc = row[0].text.replace('\n', ' ').lstrip()
            quotes.append({"user": creator,"postdate":postdate,"desc":desc})
            ## inserting records in user table
            try:
                db.insertUser(creator)  ## saving user name
                checkUserId = db.getUserDetails(creator)
                check_status = db.check_discussion_record_is_exist(topicid,checkUserId[0][0],postdate)
                disucsstext = desc.encode('ascii', errors='ignore').decode("utf-8")
                db.insertTopicDiscussion(topicid, checkUserId[0][0], disucsstext, postdate)
                # if check_status[0][0] == 0:
                #     disucsstext = desc.encode('ascii', errors='ignore').decode("utf-8")
                #     db.insertTopicDiscussion(topicid, checkUserId[0][0], disucsstext, postdate)
                # else:
                #     check_status = [(1,)]
                #     break

            except Exception as e:
                print("Records insert Error======",e)
        except Exception as e:
            pass

    #return quotes,check_status
    return quotes


def status(topicid,url):
    number = 1
    username = ""
    createddate = ""
    lst = []
    num = url.split("/")[-1]
    while True:
        try:

            #url = url.replace(url.split("/")[-1], str(num))
            url = url[:url.rfind('/')] + "/" + str(num)
            print(url)
            # out,check_count_value = get_url_parse(url, num,topicid)
            out = get_url_parse(url, num, topicid)
            # if int(check_count_value[0][0]) == 0:
            num = int(num) + 20
            lst.append(out)
            ## ALTER TABLE topicdiscussion ADD CONSTRAINT constraint_topicdisc UNIQUE KEY(TopicId,UserId,DiscussionDateCopy);
            if username == lst[len(lst) - 1][0]['user'] and createddate == lst[len(lst) - 1][0]['postdate']:
                number = int(num) - 40
                break
            username = lst[len(lst) - 1][0]['user']
            createddate = lst[len(lst) - 1][0]['postdate']
            # else:
            #     break

        except Exception as e:
            break


    return number

# url='https://forum.valuepickr.com/t/godawari-power-any-trackers/4815/1'
# status(url)