
import pandas as pd

class Statistics():

    # standard of each five day
    def Volatility(self, prices):
        return prices.rolling(center=False, window=5).mean()


    def Momentum(self, prices):
        momentum = (prices/prices.shift(-5))-1
        return momentum


    def BollingerBand(self, prices):
        sma = prices.rolling(center=False, window=5).mean()
        std = prices.rolling(center=False, window=5).std()
        df = (prices - sma)/(2*std)
        return df


    # stocks' price will rise or decline after five days
    # if Y > 0 : it rise else : decline
    def Y(self, prices):
        return (prices.shift(-5)/prices) - 1.0
