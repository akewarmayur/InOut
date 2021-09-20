import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import re


#USER_AGENT={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#response = requests.get("https://www.investing.com/equities/acc", headers=USER_AGENT)

#soup = BeautifulSoup(response.text,'html.parser')
#pidJSON=soup.find('script', id="__NEXT_DATA__").text
#pid = re.search('instrument_id.....[\d]+', pidJSON ).group(0).replace('instrument_id\\":\\"', '')
#print(pidJSON)
#print(pid)

#exit()

def get_pids(link_csv_path):
  stocks = []
  pids = []
  NCode = []
  USER_AGENT={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
  stocks_pid = pd.DataFrame()

  # print(stocks_pid)
  df = pd.read_csv(link_csv_path)
  # print(df.head())
  for i, link in enumerate(df['Stock Links']):
    try:
        # print(link)
        NiftyCode = ""
        temp = link.split('/')
        stock_name = temp[len(temp) - 1].upper()
        response = requests.get(link, headers=USER_AGENT)
        soup = BeautifulSoup(response.text,'html.parser')

        pidJSON=soup.find('script', id="__NEXT_DATA__").text
        pid = re.search('instrument_id.....[\d]+', pidJSON ).group(0).replace('instrument_id\\":\\"', '')

        NiftyCode=soup.select('span[data-test="instrument-bottom-ticker-value"]')[0].text
        # remove_lower = lambda text: re.sub('[a-z]', '', text)
        # gg = remove_lower(gg)
        print(NiftyCode, pid)
        if (NiftyCode != ""):
            stocks.append(stock_name)
        else:
            stocks.append(stock_name)
        NCode.append(NiftyCode)
        pids.append(pid)

        # print(f"Stock=>{stock_name}   PID=>{temp}")
        #if i == 2:
        #    break

        stocks_pid['stocks'] = stocks
        stocks_pid['niftycode'] = NCode
        stocks_pid['pid'] = pids
        # break
        stocks_pid.to_csv('stocks_pids.csv')
    except:
        pass

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

    result_name = dom.find('CUSIP')
    # print(result_name)
    gg = dom[result_name: result_name + 100]
    gg = re.sub('[^A-Z]+', '', gg)
    NiftyCode = gg.replace('CUSIP', '')
    # remove_lower = lambda text: re.sub('[a-z]', '', text)
    # gg = remove_lower(gg)
    print(NiftyCode)

    return pid, NiftyCode

# link_csv_path = "path to csv file contains urls and name"
# # Enter path of csv It will save as stocks_pids.csv file
stocks_pid_df = get_pids('InvestingStocksLinks.csv')
# print(stocks_pid_df.head())
#
#pid, NiftyCode = get_pid('https://in.investing.com/indices/s-p-cnx-nifty')
