import pandas as pd
import requests
import re

def get_pids(link_csv_path):
  stocks = []
  pids = []
  USER_AGENT={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
  stocks_pid = pd.DataFrame()

  print(stocks_pid)
  df = pd.read_csv(link_csv_path)
  # print(df.head())
  for i, link in enumerate(df['Stock Links']):
    print(link)
    temp = link.split('/')
    stock_name = temp[len(temp) - 1].upper()
    response = requests.get(link, headers=USER_AGENT)
    dom = response.text
    result = dom.find('instrumentId')
    ff = dom[result: result + 45]
    ff = ff.replace('"', '')
    ff = ff.replace(',', '')
    temp = int(re.findall(r'\d+', ff)[0])

    if (ff.count(stock_name)>0):
        stocks.append(stock_name)
    else:
        stocks.append(stock_name)

    pids.append(temp)

    print(f"Stock=>{stock_name}   PID=>{temp}")


    stocks_pid['stocks'] = stocks
    stocks_pid['pid'] = pids
    stocks_pid.to_csv('stocks_pids.csv')
    return stocks_pid


# Get pids from url

def get_pid(url):
    USER_AGENT = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    temp = url.split('/')
    stock_name = temp[len(temp) - 1].upper()
    response = requests.get(url, headers=USER_AGENT)
    dom = response.text

    result = dom.find('instrumentId')

    ff = dom[result: result + 45]
    print(ff)
    ff = ff.replace('"', '')
    ff = ff.replace(',', '')
    pid = int(re.findall(r'\d+', ff)[0])

    return pid

# link_csv_path = "path to csv file contains urls and name"
# # Enter path of csv It will save as stocks_pids.csv file
# stocks_pid_df = get_pids(link_csv_path)
# print(stocks_pid_df.head())
#
# pid = get_pid('https://in.investing.com/indices/s-p-cnx-nifty')
# print(pid)