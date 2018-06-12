import math
import dataloader
import predictorGenerator as helper
import tradingSimulator as simulator
import orderGenerator
import pandas as pd
from datetime import datetime

if __name__ == "__main__":

    SYMBOL = '600570.XSHG'

    train_data, price_array, price_df1 = helper.PredictiorGenerator().getData(
        [SYMBOL], pd.date_range('2018-04-17 13:36:52', '2018-04-17 13:42:44', freq='S'))
    test_data, price_array, price_df2 = helper.PredictiorGenerator().getData(
        [SYMBOL], pd.date_range('2018-04-17 13:36:52', '2018-04-17 13:42:44', freq='S'))

    train_rows = math.floor(train_data.shape[0])
    test_rows = math.floor(test_data.shape[0])

    # separate out training and testing data
    trainX = train_data[:int(train_rows), 0:-1]
    trainY = train_data[:int(train_rows), -1]

    testX = test_data[:int(test_rows), 0:-1]
    testY = test_data[:int(test_rows), -1]

    # predict
    # pretend predicting the Y
    predY = testY

    # Now Generate Orders Algorithmically based on the predicted values
    orders = orderGenerator.OrderGenerator().generateOrders(price_df1, SYMBOL, predY)

    simulator.simulateMarket('orders.txt', '2018-04-17 13:36:52', '2018-04-17 13:42:44', 'S')