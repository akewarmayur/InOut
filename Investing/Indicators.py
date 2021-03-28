import pandas_ta as ta


class Indicators:
    def __init__(self):
        self.CustomStrategy = ta.Strategy(
            name="First",
            description="EMA 50,100, 200, BBANDS, RSI, PSa2 and Ichimocloud",
            ta=[
                {"kind": "ema", "length": 50},
                {"kind": "ema", "length": 100},
                {"kind": "ema", "length": 200},
                {"kind": "bbands", "length": 14},
                {"kind": "rsi", "length": 14},
                {"kind": "psar"},
                {"kind": "ichimoku"}, ])

    def custom_indicators(self, df, indicator_name):
        try:
            no_of_rows = len(df.index)
            if indicator_name == 'per_change':
                df['per_change'] = 0
                for i, columnData in enumerate(df['close']):
                    s = i + 1
                    if s < no_of_rows:
                        value = ((columnData - df['close'].iloc[i + 1]) / df['close'].iloc[i + 1]) * 100
                        df['per_change'].iloc[i] = value
                    else:
                        df['per_change'].iloc[i] = 0
                return df

            if indicator_name == 'volume_high_count':
                s = 0
                df['volume_high_count'] = 0
                for i, columnData in enumerate(df['volume']):
                    g = i + 1
                    if g < no_of_rows:
                        count = 1
                        so = True
                        for j in range(s, no_of_rows):
                            t = j + 1
                            if t < no_of_rows:
                                if so == True:
                                    cur = df['volume'].iloc[j]
                                next = df['volume'].iloc[j + 1]
                                if cur < next:
                                    break
                                else:
                                    count += 1
                                so = False
                            else:
                                count = count - 1
                                break
                        s += 1
                        df['volume_high_count'].iloc[i] = count
                    else:
                        df['volume_high_count'].iloc[i] = 0

            if indicator_name == 'close_count':
                s = 0
                df['close_count'] = 0
                for i, columnData in enumerate(df['close']):
                    g = i + 1
                    if g < no_of_rows:
                        count = 1
                        so = True
                        for j in range(s, no_of_rows):
                            t = j + 1
                            if t < no_of_rows:
                                if so == True:
                                    cur = df['close'].iloc[j]
                                next = df['close'].iloc[j + 1]
                                if cur < next:
                                    break
                                else:
                                    count += 1
                                so = False
                            else:
                                count = count - 1
                                break
                        s += 1
                        df['close_count'].iloc[i] = count
                    else:
                        df['close_count'].iloc[i] = 0

            if indicator_name == 'per_change_count':
                s = 0
                df['per_change_count'] = 0
                for i, columnData in enumerate(df['per_change']):
                    g = i + 1
                    if g < no_of_rows:
                        count = 1
                        so = True
                        for j in range(s, no_of_rows):
                            t = j + 1
                            if t < no_of_rows:
                                if so == True:
                                    cur = df['per_change'].iloc[j]
                                next = df['per_change'].iloc[j + 1]
                                if cur < 0:
                                    if cur > next:
                                        break
                                    else:
                                        count += 1
                                    so = False
                                else:
                                    if cur < next:
                                        break
                                    else:
                                        count += 1
                                    so = False
                            else:
                                count = count - 1
                                break
                        s += 1
                        if cur < 0:
                            df['per_change_count'].iloc[i] = count * -1
                        else:
                            df['per_change_count'].iloc[i] = count
                    else:
                        df['per_change_count'].iloc[i] = 0
            return df
        except Exception as e:
            print('Exception while calculating custom indicators', e)
            return df

    def cal_heiken_ashi(self, df):
        try:
            df['ha_close'] = (df.open + df.high + df.low + df.close) / 4
            df.reset_index(inplace=True)
            ha_open = [(df.open[0] + df.close[0]) / 2]
            [ha_open.append((ha_open[i] + df.ha_close.values[i]) / 2) for i in range(0, len(df) - 1)]
            df['ha_open'] = ha_open
            df.set_index('index', inplace=True)
            df['ha_high'] = df[['ha_open', 'ha_close', 'high']].max(axis=1)
            df['ha_low'] = df[['ha_open', 'ha_close', 'low']].min(axis=1)
            return df
        except Exception as e:
            print('Exception while calculating heiken ashi', e)
            return df