
import numpy as np
import pandas as pd
import os
import dataloader
import statistics as stats

class PredictiorGenerator():

    def __symbol_to_path(self, symbol, base_dir=os.path.join(".", "data")):
        """Return file path given ticker symbol."""
        return os.path.join(base_dir, "{}.txt".format(str(symbol)))

    def get_current(self, symbols, dates):
        """Read stock data (current) for given symbols from files."""

        df = pd.DataFrame(index=dates)

        for symbol in symbols:
            df_temp = dataloader.DataLoader().loaddata(self.__symbol_to_path(symbol))
            df_temp = pd.DataFrame(df_temp, columns={'current'})
            df_temp = df_temp.rename(columns={'current': symbol})
            df = df.join(df_temp)
            df = df.dropna()

        return df


    def getData(self, symbols, dates):
        price_df = self.get_current(symbols, dates)
        Y_df = stats.Statistics().Y(price_df).fillna(method='ffill')
        BB_df = stats.Statistics().BollingerBand(price_df).fillna(0)
        V_df = stats.Statistics().Volatility(price_df).fillna(0)
        M_df = stats.Statistics().Momentum(price_df).fillna(0)
        total_rows = len(Y_df)
        data = np.zeros(shape=(total_rows, 4))
        price_array = np.zeros(shape=(total_rows, 1))

        for i in range(total_rows):
            data[i,0]=BB_df.ix[i]
            data[i,1]=V_df.ix[i]
            data[i,2]=M_df.ix[i]
            data[i,3]=Y_df.ix[i]

            price_array[i,0] = price_df.ix[i]

        return data , price_array , price_df

