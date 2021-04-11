import pandas as pd
from common.sheetOperations import SheetOps
from common.common import CommonFunctions
import Investing.investConfig as investConfig
import warnings
import config
warnings.filterwarnings("ignore")


class HelpIn:
    
    def __init__(self):
        self.col2wrt = ['datetime', 'symbol', 'pid', 'resolution', 'close',
                        'volume', 'per_change', 'volume_high_count', 
                        'close_count', 'per_change_count']
        self.objSheet = SheetOps()
        self.objCommon = CommonFunctions()

    def convert2datime(self, dff):

        try:
            dff['datetime'] = dff['datetime'].astype('datetime64[ns]')
            dff['symbol'] = dff['symbol'].astype('str')
            dff['pid'] = dff['pid'].astype('int64')
            dff['resolution'] = dff['resolution'].astype('str')
            dff['close'] = dff['close'].astype('float64')
            dff['volume'] = dff['volume'].astype('int64')
            dff['per_change'] = dff['per_change'].astype('float64')
            dff['volume_high_count'] = dff['volume_high_count'].astype('int64')
            dff['close_count'] = dff['close_count'].astype('int64')
            dff['per_change_count'] = dff['per_change_count'].astype('int64')
            return dff
        except Exception as e:
            print('Exception in converting to datetime:', e)
            return dff

    def write_sheet(self, write_list, l, position=-1):
        for wl in write_list:
            t = wl[0]
            wl[0] = str(t)
            if position != -1 and len(l) == 0:
                wl[position] = ' '
            if position == -1 and len(l) != 0:
                for i in l:
                    wl[i] = ' '
            self.objSheet.writeSheet(config.Notesheet, wl, 'InvestingNotify')

    def calculations(self, df, candles_to_notify_from):
        outliers_close_rows = []
        outliers_volume_rows = []
        outliers_per_rows = []

        for i in range(candles_to_notify_from):
            slice = df[i:200 + i]
            r = self.objCommon.get_outliers(slice, 'close_count', slice['close_count'].iloc[i])
            if len(r) != 0:
                c = slice[slice.close_count.isin(r)]
                outliers_close_rows.append(c)

            r = self.objCommon.get_outliers(slice, 'volume_high_count', slice['volume_high_count'].iloc[i])
            if len(r) != 0:
                c = slice[slice.close_count.isin(r)]
                outliers_volume_rows.append(c)

            r = self.objCommon.get_outliers(slice, 'per_change_count', slice['per_change_count'].iloc[i])
            if len(r) != 0:
                c = slice[slice.close_count.isin(r)]
                outliers_per_rows.append(c)

        if len(outliers_close_rows) > 1:
            outliers_close_rows_df = pd.concat(outliers_close_rows).drop_duplicates().reset_index(drop=True)
        elif len(outliers_close_rows) == 1:
            outliers_close_rows_df = outliers_close_rows[0]
        else:
            outliers_close_rows_df = pd.DataFrame(columns=self.col2wrt)

        if len(outliers_volume_rows) > 1:
            outliers_volume_rows_df = pd.concat(outliers_volume_rows).drop_duplicates().reset_index(drop=True)
        elif len(outliers_volume_rows) == 1:
            outliers_volume_rows_df = outliers_volume_rows[0]
        else:
            outliers_volume_rows_df = pd.DataFrame(columns=self.col2wrt)

        if len(outliers_per_rows) > 1:
            outliers_per_rows_df = pd.concat(outliers_per_rows).drop_duplicates().reset_index(drop=True)
        elif len(outliers_per_rows) == 1:
            outliers_per_rows_df = outliers_per_rows[0]
        else:
            outliers_per_rows_df = pd.DataFrame(columns=self.col2wrt)

        return outliers_close_rows_df, outliers_volume_rows_df, outliers_per_rows_df


            
    def notifications(self, df, candles_to_notify_from):
        try:
            # df['datetime'] = df['datetime'].astype('datetime64[ns]')
            # slice = df.iloc[:investConfig.no_of_past_candles_5MIN]
            # slice = slice[self.col2wrt]
            outliers_close_rows, outliers_volume_rows, outliers_per_rows = self.calculations(df, candles_to_notify_from)


            # all three
            outliers_close_rows = self.convert2datime(outliers_close_rows)
            outliers_volume_rows = self.convert2datime(outliers_volume_rows)
            temp = pd.merge(outliers_close_rows, outliers_volume_rows, how='inner', on=self.col2wrt)

            temp = self.convert2datime(temp)
            outliers_per_rows = self.convert2datime(outliers_per_rows)
            ocr_ovr_opr = pd.merge(temp, outliers_per_rows, how='inner', on=self.col2wrt)
            # ocr_ovr_opr = pd.concat([outliers_close_rows, outliers_volume_rows, outliers_per_rows], axis=1, join='inner')
            if len(ocr_ovr_opr) != 0:
                # write sheet
                write_list = ocr_ovr_opr.values.tolist()
                self.write_sheet(write_list, [], -2)
                for dt in ocr_ovr_opr['datetime']:
                    outliers_close_rows.drop(outliers_close_rows[outliers_close_rows['datetime'] == dt].index, inplace=True)
                    outliers_volume_rows.drop(outliers_volume_rows[outliers_volume_rows['datetime'] == dt].index,
                                              inplace=True)
                    outliers_close_rows.drop(outliers_per_rows[outliers_per_rows['datetime'] == dt].index, inplace=True)

            # any two
            outliers_close_rows = self.convert2datime(outliers_close_rows)
            outliers_volume_rows = self.convert2datime(outliers_volume_rows)
            ocr_ovr = pd.merge(outliers_close_rows, outliers_volume_rows, how='inner', on=self.col2wrt)
            # ocr_ovr = pd.concat([outliers_close_rows, outliers_volume_rows], axis=1, join='inner')

            if len(ocr_ovr) != 0:
                # write sheet
                write_list = ocr_ovr.values.tolist()
                self.write_sheet(write_list, [self.col2wrt.index('per_change_count'), self.col2wrt.index('per_change')],
                            position=-1)
                for dt in ocr_ovr['datetime']:
                    outliers_close_rows.drop(outliers_close_rows[outliers_close_rows['datetime'] == dt].index, inplace=True)
                    outliers_volume_rows.drop(outliers_volume_rows[outliers_volume_rows['datetime'] == dt].index,
                                              inplace=True)

            outliers_close_rows = self.convert2datime(outliers_close_rows)
            outliers_per_rows = self.convert2datime(outliers_per_rows)
            ocr_opr = pd.merge(outliers_close_rows, outliers_per_rows, how='inner', on=self.col2wrt)
            if len(ocr_opr) != 0:
                # write sheet
                write_list = ocr_opr.values.tolist()
                self.write_sheet(write_list, [self.col2wrt.index('volume'), self.col2wrt.index('volume_high_count')],
                            position=-1)
                for dt in ocr_opr['datetime']:
                    outliers_close_rows.drop(outliers_close_rows[outliers_close_rows['datetime'] == dt].index, inplace=True)
                    outliers_per_rows.drop(outliers_per_rows[outliers_per_rows['datetime'] == dt].index, inplace=True)
            #
            outliers_volume_rows = self.convert2datime(outliers_volume_rows)
            outliers_per_rows = self.convert2datime(outliers_per_rows)
            ovr_opr = pd.merge(outliers_volume_rows, outliers_per_rows, how='inner', on=self.col2wrt)
            if len(ovr_opr) != 0:
                # write sheet
                write_list = ovr_opr.values.tolist()
                self.write_sheet(write_list, [self.col2wrt.index('close'), self.col2wrt.index('close_count')],
                            position=-1)
                for dt in ovr_opr['datetime']:
                    outliers_volume_rows.drop(outliers_volume_rows[outliers_volume_rows['datetime'] == dt].index,
                                              inplace=True)
                    outliers_per_rows.drop(outliers_per_rows[outliers_per_rows['datetime'] == dt].index, inplace=True)

            # write remaining sheets
            if len(outliers_close_rows) != 0:
                # write sheet
                write_list = outliers_close_rows.values.tolist()
                self.write_sheet(write_list, [self.col2wrt.index('volume'), self.col2wrt.index('per_change'),
                                         self.col2wrt.index('volume_high_count'),
                                         self.col2wrt.index('per_change_count')], -1)

            if len(outliers_volume_rows) != 0:
                # write sheet
                write_list = outliers_volume_rows.values.tolist()
                self.write_sheet(write_list, [self.col2wrt.index('close'), self.col2wrt.index('per_change'),
                                         self.col2wrt.index('close_count'), self.col2wrt.index('per_change_count')], -1)

            if len(outliers_per_rows) != 0:
                # write sheet
                write_list = outliers_per_rows.values.tolist()
                self.write_sheet(write_list, [self.col2wrt.index('close'), self.col2wrt.index('volume'),
                                         self.col2wrt.index('volume_high_count'),
                                         self.col2wrt.index('close_count')], -1)
        except Exception as e:
            print('Exception in Investing Notifications', e)