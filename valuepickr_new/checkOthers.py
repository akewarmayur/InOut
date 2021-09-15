import pandas as pd

df = pd.read_csv("return.csv")
df= df.pivot(index='date',columns='label',values='value')
print(df.index.tolist())
print(df['NIFTY'].tolist())
df =df.drop('NIFTY',axis=1)
df.reset_index(drop=True, inplace=True)
# print(df)
#print("columns====",list(df.columns))
Lst=[]
for column in df:
    Lst.append(df[column].to_list())
print(Lst)
# print(df.index.tolist())
#print(df['NIFTY'].tolist())

# print(df.index.tolist())
# print(df['value']['NIFTY'].to_list())
# print(df['value'][-1])
#print(df['nifty'].tolist())
#print(df['value']['NIFTY'])
#df= df['value'][1:-1]






'select TradeDateTime as date,CONCAT( StrikePrice, "-", OptionType )as label,OI as value from stockdetails_' + str(tableName) + ' where ScripName = "' + str(symbol) + '" and StrikePrice in (' + str(stkprice) + ') and OptionType in ("' + str(optype) + '") and DATE(TradeDateTime) BETWEEN "' + str(From) + '" AND "' + str(To) + '" union select TradeDateTime as date,ScripName as label,SpotPrice as value from stockdetails_' + str(tableName) + ' where ScripName = "' + str(symbol) + '" and StrikePrice in (' + str(stkprice) + ') and  OptionType in ("' + str(optype) + '") and  DATE(TradeDateTime) BETWEEN "' + str(From) + '" AND "' + str(To) + '"'



