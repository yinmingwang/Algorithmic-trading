import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import re
import time
import win_unicode_console
from datetime import datetime
win_unicode_console.enable()

class DataLoader():

    def __loaddatafromfile(self, file_path):
        """Read the data from the txt file.
        Read tha data from the txt file and switch the data into a 'Dataframe',
        using the date as index.

        Parameters
        ----------
            file_path: the path of the file

        Returns
        -------
            dataSet: the data of the file

        """

        # Step 1 : Create a 'DataFrame' with the columns we need

        columns_index = [
            'exchg', 'code', 'name', 'time', 'pclose', 'price', 'open', ...and
            'high', 'low', 'volume', 'amount', 'tick', 'wavgbp', 'wavgsp', ...and
            'bvol', 'svol', 'iopv', 'ytm', 'type', 'timestamp',  ...and
            '卖价1', '卖手1', '买价1', '买手1', ...and
            '卖价2', '卖手2', '买价2', '买手2', ...and
            '卖价3', '卖手3', '买价3', '买手3', ...and
            '卖价4', '卖手4', '买价4', '买手4', ...and
            '卖价5', '卖手5', '买价5', '买手5', ...and
            '卖价6', '卖手6', '买价6', '买手6', ...and
            '卖价7', '卖手7', '买价7', '买手7', ...and
            '卖价8', '卖手8', '买价8', '买手8', ...and
            '卖价9', '卖手9', '买价9', '买手9', ...and
            '卖价10', '卖手10', '买价10', '买手10', ...and
            'daily']

        dataSet = DataFrame(columns=columns_index)

        # Step 2 : Read the data from the file.

        count = -1
        line_count = 0
        temp = [0] * 61
        with open(file_path, 'r') as file:
            lines = file.read().splitlines()
            for line in lines:
                count = count + 1
                if count < 4:
                    temp[count] = line
                elif count < 9:
                    temp[count] = float(line)
                elif count < 11:
                    temp[count] = int(line)
                elif count < 12:
                    temp[count] = line
                elif count < 14:
                    temp[count] = float(line)
                elif count < 16:
                    temp[count] = int(line)
                elif count < 18:
                    temp[count] = float(line)
                elif count == 18:
                    temp[count] = line
                elif count == 19:
                    temp[count] = self.timestamp_to_date(
                        self.timestamp_to_timestamp10(int(line)))
                elif count >= 20 and count <= 29:
                    single_data = re.split(' ', line)
                    temp[20 + (count - 20) * 4] = float(single_data[0])
                    temp[20 + (count - 20) * 4 + 1] = int(single_data[1])
                    temp[20 + (count - 20) * 4 + 2] = float(single_data[2])
                    temp[20 + (count - 20) * 4 + 3] = int(single_data[3])
                else:
                    temp[60] = line
                    dataSet.loc[line_count] = temp
                    count = -1
                    line_count = line_count + 1
                    print(temp)
                    temp = [0] * 61

        file.close()

        # Step 3 : Data cleaning

        dataSet = dataSet.drop_duplicates('timestamp')

        # Set the 'datatime' as the index
        dataSet = dataSet.set_index('timestamp')
        dataSet.head()

        #print(dataSet)

        return dataSet

    def loaddata(self, file_path):
        data = self.__loaddatafromfile(file_path)
        return data

    #生成当前时间的时间戳，只有一个参数即时间戳的位数，默认为10位，输入位数即生成相应位数的时间戳，比如可以生成常用的13位时间戳
    def now_to_timestamp(self, digits=10):
        time_stamp = time.time()
        digits = 10 ** (digits - 10)
        time_stamp = int(round(time_stamp*digits))
        return time_stamp

    #将时间戳规范为10位时间戳
    def timestamp_to_timestamp10(self, time_stamp):
        time_stamp = int(time_stamp * (10 ** (10-len(str(time_stamp)))))
        return time_stamp

    #将当前时间转换为时间字符串，默认为2017-10-01 13:37:04格式
    def now_to_date(self, format_string="%Y-%m-%d %H:%M:%S"):
        time_stamp = int(time.time())
        time_array = time.localtime(time_stamp)
        str_date = time.strftime(format_string, time_array)
        return str_date

    #将10位时间戳转换为时间字符串，默认为2017-10-01 13:37:04格式
    def timestamp_to_date(self, time_stamp, format_string="%Y-%m-%d %H:%M:%S"):
        time_array = time.localtime(time_stamp)
        str_date = time.strftime(format_string, time_array)
        return str_date

    #将时间字符串转换为10位时间戳，时间字符串默认为2017-10-01 13:37:04格式
    def date_to_timestamp(self, date, format_string="%Y-%m-%d %H:%M:%S"):
        time_array = time.strptime(date, format_string)
        time_stamp = int(time.mktime(time_array))
        return time_stamp

    #不同时间格式字符串的转换
    def date_style_transfomation(self, date, format_string1="%Y-%m-%d %H:%M:%S", format_string2="%Y-%m-%d %H-%M-%S"):
        time_array = time.strptime(date, format_string1)
        str_date = time.strftime(format_string2, time_array)
        return str_date
