import pandas as pd
from common.sheetOperations import SheetOps
from common.common import CommonFunctions
import Investing.investConfig as investConfig
import warnings
warnings.filterwarnings("ignore")


class HelpIn:
    
    def __init__(self):
        self.col2wrt = ['datetime', 'symbol', 'pid', 'resolution', 'close',
                        'volume', 'per_change', 'volume_high_count', 
                        'close_count', 'per_change_count']
        self.objSheet = SheetOps()
        self.objCommon = CommonFunctions()

    def write_sheet(self, write_list, l, position=-1):
        for wl in write_list:
            t = wl[0]
            wl[0] = str(t)
            if position != -1 and len(l) == 0:
                wl[position] = ' '
            if position == -1 and len(l) != 0:
                for i in l:
                    wl[i] = ' '
            self.objSheet.writeSheet('CIEnotifications', wl, 'InvestingNotify')
            
    def notifications(self, df):
        try:
            slice = df.iloc[:investConfig.no_of_past_candles_5MIN]
            slice = slice[self.col2wrt]
            outliers_close_rows = slice[slice.close_count.isin(self.objCommon.get_outliers(slice, 'close_count'))]
            outliers_volume_rows = slice[slice.volume_high_count.isin(self.objCommon.get_outliers(slice, 'volume_high_count'))]
            outliers_per_rows = slice[slice.per_change_count.isin(self.objCommon.get_outliers(slice, 'per_change_count'))]


            # all three
            temp = pd.merge(outliers_close_rows, outliers_volume_rows, how='inner', on=self.col2wrt)
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
                                         self.col2wrt.index('close_count'), self.col2wrt.index('per_change_count')],
                            -1)

            if len(outliers_per_rows) != 0:
                # write sheet
                write_list = outliers_per_rows.values.tolist()
                self.write_sheet(write_list, [self.col2wrt.index('close'), self.col2wrt.index('volume'),
                                         self.col2wrt.index('volume_high_count'),
                                         self.col2wrt.index('close_count')], -1)
        except Exception as e:
            print('Exception in Investing Notifications', e)