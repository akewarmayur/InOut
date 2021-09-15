import requests
from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
import time
# pip install html5lib
# pip install bs4
# pip install requests


def checkExist(userId,date_time):
    pass


def get_url_parse(url,check_num_for_category):
    r = requests.get(url)
    # time.sleep(1)
    soup = BeautifulSoup(r.content,'html5lib')  # If this line causes an error, run 'pip install html5lib' or install html5lib
    quotes = []  # a list to store quotes
    ## find the category
    topic_category = soup.find_all('div', attrs={'class': 'topic-category'})
    ## stock category find
    if check_num_for_category == 1:
        category_name_first = topic_category[0]('span', attrs={'class': 'category-name'})[0].text
        category_name_second = topic_category[0]('span', attrs={'class': 'category-name'})[1].text
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
        except Exception as e:
            pass
    #print(quotes)
    return quotes



# for i in range(1,3):
#     if i == 1:
#         s = get_url_parse(url + str(i))
#         lst.append(s)
#     else:
#         i=41
#         s= get_url_parse(url+str(i))
#         lst.append(s)
# print(lst)
lst =[]
count = 1
url = 'https://forum.valuepickr.com/t/granules-india-ltd/940/1'
num = url.split("/")[-1]
username=""
createddate=""
while True:
    try:

        url= url.replace(url.split("/")[-1],str(num))
        print(url)
        out= get_url_parse(url,num)
        num = int(num) + 20
        lst.append(out)
        if username==lst[len(lst) - 1][0]['user'] and createddate==lst[len(lst) - 1][0]['postdate']:
            break
        username = lst[len(lst) - 1][0]['user']
        createddate = lst[len(lst) - 1][0]['postdate']
        print(lst)
    except Exception as e:
        print("Error==",e)

#print(lst)

