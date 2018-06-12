import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import re
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
            'datetime', 'current', 'high', 'low', 'volume', 'money', 'position', ...and
            '买手1', '买手2', '买手3', '买手4', '买手5', '买价1', '买价2', '买价3', ...and
            '买价4', '买价5', '卖手1', '卖手2', '卖手3', '卖手4', '卖手5', '卖价1', ...and
            '卖价2', '卖价3', '卖价4', '卖价5']

        dataSet = DataFrame(columns=columns_index)

        # Step 2 : Read the data from the file.

        count = 0

        with open(file_path, 'r') as file:
            lines = file.read().splitlines()
            for line in lines:
                temp = re.split(',', line)
                count = count + 1
                if (count % 2 == 0):
                    # change data into 'datetime' and 'float'
                    time = datetime(
                        int(temp[0][0:4]), int(temp[0][4:6]), int(temp[0][6:8]), ...and
                        int(temp[0][8:10]), int(temp[0][10:12]), int(temp[0][12:14]))
                    temp[0] = time
                    for i in range(1, 27):
                        if temp[i] != '':  # ignore empty data
                            temp[i] = float(temp[i])
                    dataSet.loc[count / 2] = temp

        file.close()

        # Step 3 : Data cleaning

        dataSet = dataSet.drop_duplicates('datetime')

        # Set the 'datatime' as the index
        dataSet = dataSet.set_index('datetime')
        dataSet.head()

        return dataSet

    def loaddata(self, file_path):
        data = self.__loaddatafromfile(file_path)
        return data
