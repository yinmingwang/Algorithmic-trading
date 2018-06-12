import pandas as pd
import numpy as np

class OrderGenerator():

    def generateOrders(self, price_df, symbol, predY):
        """Generate the orders of the stock depending on your strategy.

        Your can use the price of the stocks and the predictions to
        make your own strategy. The order contain the record of 'BUY' or
        'SELL' the stocks.

        Parameters
        ----------
            price_df: the data of the stocks
            symbol: the name of the stocks
            predY: the predictions of the stocks

        Returns
        -------
            orders: the record of 'BUY' or 'SELL'

        """

        total_stock = 10000  # number of original stock
        restbuy = 10000  
        restsell = 10000

        print("******** Generate Orders based on Predictions:")

        orders = pd.DataFrame(index=np.arange(price_df.size), columns=[
                            'Date', 'Symbol', 'Order', 'Shares'])

        """
        long_entries: stock(in)
        short_entries: going short(in)
        long_exits: stock(out)
        short_exits: stock(out)
        """
        long_entries = pd.DataFrame(index=price_df.index, columns=[symbol])
        short_entries = pd.DataFrame(index=price_df.index, columns=[symbol])
        long_exits = pd.DataFrame(index=price_df.index, columns=[symbol])
        short_exits = pd.DataFrame(index=price_df.index, columns=[symbol])

        last_position = 'NA'  # the last action
        i = 0  # range(0, df.shape[0])
        j = -1
        s = -1
        t = 0

        # the band of the stock
        long_entry_band = 5
        short_entry_band = 5

        col = price_df.iloc[:, 0]
        price_arrs = col.values

        # five day later price
        five_days_price = (predY + 1.0) * price_arrs
        N = len(predY)

        for date_index, row in price_df.iterrows():

            index_date = date_index
            
            if(i < N):

                diff = (five_days_price[i] - price_arrs[i]) / price_arrs[i]

                if (diff > 0.08 and long_entry_band > 0):

                    short_entry_band = 5
                    long_entry_band -= 1

                    long_entries.iloc[i][symbol] = price_df.iloc[i][symbol]
                    last_position = 'LONG_ENTRY'
                    j = j + 1

                    standard = total_stock / (10*100)
                    shares = restbuy / 100

                    if(shares > 0):

                        if (shares > standard):
                            shares = standard

                        orders.iloc[j]['Date'] = index_date
                        orders.iloc[j]['Symbol'] = symbol
                        orders.iloc[j]['Order'] = 'BUY'
                        orders.iloc[j]['Shares'] = 100*shares
                        restbuy -= 100*shares

                elif (diff > 0.05 and long_entry_band > 0):

                    short_entry_band = 5
                    long_entry_band -= 1

                    long_entries.iloc[i][symbol] = price_df.iloc[i][symbol]
                    last_position = 'LONG_ENTRY'
                    j = j + 1

                    standard = total_stock / (50*100)
                    shares = restbuy / 100

                    if(shares > 0):

                        if (shares > standard):
                            shares = standard

                        orders.iloc[j]['Date'] = index_date
                        orders.iloc[j]['Symbol'] = symbol
                        orders.iloc[j]['Order'] = 'BUY'
                        orders.iloc[j]['Shares'] = 100*shares
                        restbuy -= 100*shares

                elif (diff > 0.02 and long_entry_band > 0):

                    short_entry_band = 5
                    long_entry_band -= 1

                    long_entries.iloc[i][symbol] = price_df.iloc[i][symbol]
                    last_position = 'LONG_ENTRY'
                    j = j + 1

                    standard = 2
                    shares = restbuy / 100

                    if(shares > 0):

                        if (shares > standard):
                            shares = standard

                        orders.iloc[j]['Date'] = index_date
                        orders.iloc[j]['Symbol'] = symbol
                        orders.iloc[j]['Order'] = 'BUY'
                        orders.iloc[j]['Shares'] = 100*shares
                        restbuy -= 100*shares

                elif (diff > 0 and long_entry_band > 0):

                    short_entry_band = 5
                    long_entry_band -= 1

                    long_entries.iloc[i][symbol] = price_df.iloc[i][symbol]
                    last_position = 'LONG_ENTRY'
                    j = j + 1

                    standard = 1
                    shares = restbuy / 100

                    if(shares > 0):

                        if (shares > standard):
                            shares = standard

                        orders.iloc[j]['Date'] = index_date
                        orders.iloc[j]['Symbol'] = symbol
                        orders.iloc[j]['Order'] = 'BUY'
                        orders.iloc[j]['Shares'] = 100*shares
                        restbuy -= 100*shares

                elif (diff > -0.02 and short_entry_band > 0):

                    long_entry_band = 5
                    short_entry_band -= 1

                    short_entries.iloc[i][symbol] = price_df.iloc[i][symbol]
                    last_position = 'SHORT_ENTRY'
                    j = j + 1

                    standard = 1
                    shares = restsell / 100
                    if (shares > 0):

                        if (shares > standard):
                            shares = standard

                        orders.iloc[j]['Date'] = index_date
                        orders.iloc[j]['Symbol'] = symbol
                        orders.iloc[j]['Order'] = 'SELL'
                        orders.iloc[j]['Shares'] = 100 * shares
                        restsell -= 100*shares

                elif (diff > -0.05 and short_entry_band > 0):

                    long_entry_band = 5
                    short_entry_band -= 1

                    short_entries.iloc[i][symbol] = price_df.iloc[i][symbol]
                    last_position = 'SHORT_ENTRY'
                    j = j + 1

                    standard = 2
                    shares = restsell / 100
                    if (shares > 0):
                        if (shares > standard):
                            shares = standard

                        orders.iloc[j]['Date'] = index_date
                        orders.iloc[j]['Symbol'] = symbol
                        orders.iloc[j]['Order'] = 'SELL'
                        orders.iloc[j]['Shares'] = 100 * shares
                        restsell -= 100*shares

                elif (diff > -0.08 and short_entry_band > 0):

                    long_entry_band = 5
                    short_entry_band -= 1

                    short_entries.iloc[i][symbol] = price_df.iloc[i][symbol]
                    last_position = 'SHORT_ENTRY'
                    j = j + 1

                    standard = total_stock / (50*100)
                    shares = restsell / 100
                    if (shares > standard):
                        shares = standard

                        orders.iloc[j]['Date'] = index_date
                        orders.iloc[j]['Symbol'] = symbol
                        orders.iloc[j]['Order'] = 'SELL'
                        orders.iloc[j]['Shares'] = 100 * shares
                        restsell -= 100*shares

                elif (diff <= -0.08 and short_entry_band > 0):

                    long_entry_band = 5
                    short_entry_band -= 1

                    short_entries.iloc[i][symbol] = price_df.iloc[i][symbol]
                    last_position = 'SHORT_ENTRY'
                    j = j + 1

                    standard = total_stock / (10*100)
                    shares = restsell / 100
                    if (shares > standard):
                        shares = standard

                        orders.iloc[j]['Date'] = index_date
                        orders.iloc[j]['Symbol'] = symbol
                        orders.iloc[j]['Order'] = 'SELL'
                        orders.iloc[j]['Shares'] = 100 * shares
                        restsell -= 100*shares

                elif (last_position == 'LONG_ENTRY' and long_entry_band < 1):
                    long_entry_band = 5

                    long_exits.iloc[i][symbol] = price_df.iloc[i][symbol]

                    last_position = 'LONG_EXIT'

                    j = j + 1
                    orders.iloc[j]['Date'] = index_date
                    orders.iloc[j]['Symbol'] = symbol
                    orders.iloc[j]['Order'] = 'SELL'
                    orders.iloc[j]['Shares'] = 100

                elif (last_position == 'SHORT_ENTRY' and short_entry_band < 1):
                    short_entry_band = 5
                    short_exits.iloc[i][symbol] = price_df.iloc[i][symbol]

                    last_position = 'SHORT_EXIT'

                    j = j + 1
                    orders.iloc[j]['Date'] = index_date
                    orders.iloc[j]['Symbol'] = symbol
                    orders.iloc[j]['Order'] = 'BUY'
                    orders.iloc[j]['Shares'] = 100

            i = i + 1
            t = t + 1

        print("-----restbuy-----")
        print(restbuy)
        print("-----restsell-----")
        print(restsell)
        print('--------------------')

        # sort by date time
        orders = orders.dropna(subset=["Symbol"]).sort_index()

        print('save data into orders file.')
        orders.to_csv('orders.txt')

        return orders