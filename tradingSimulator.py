import datetime as dt
import predictorGenerator as helper
import portifolioEvaluator as pve
import pandas as pd

def simulateMarket(orders_file, start_date, end_date, frequency):
    """Driver function."""
    start_val = 10000

    # Process orders
    portvals = pve.compute_portvals(
        start_date, end_date, orders_file, start_val, frequency)

    # print("Process orders")
    # print(portvals)
    
    if isinstance(portvals, pd.DataFrame):
        # if a DataFrame is returned select the first column to get a Series
        portvals = portvals[portvals.columns[0]]
        #print "hello"  # get in this condition

    # calculate the number of the trading days
    start = dt.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    end = dt.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    day_num = (end - start).seconds / (24 * 3600)

    rate_of_return = pve.get_rate_of_return(portvals[-1], start_val)
    rate_of_return_yearly = pve.get_rate_of_return_yearly(
        portvals[-1], start_val, day_num)
    sharpe_ratio = pve.get_sharpe_ratio(rate_of_return_yearly, 0.04, portvals)

    # Show portfolio
    print("Initial Portfolio Value: {}".format(start_val))
    print("Data Range: {} to {}".format(start_date, end_date))
    print("Final Portfolio Value: {}".format(portvals[-1]))
    print("Rate of return: {}".format(rate_of_return))
    print("Rate of return yearly: {}".format(rate_of_return_yearly))
    print("Sharpe ratio: {}".format(sharpe_ratio))


