import numpy as np
import predictorGenerator as helper
import pandas as pd

def compute_portvals(start_date, end_date, orders_file, start_val, frequency):
    """Compute daily portfolio value given a sequence of orders in a CSV file.

    File contains - list orders
    Load historical data
    Execute the orders in the past
    At any instant we shall have a portfolio

    'formulate trading strategy using  technical indicators' and then continuously buy/sell stock options and dynamically change the portfolio
    by generating orders and be executing them thru this Market Simulator ...'


    Parameters
    ----------
        start_date: first date to track
        end_date: last date to track
        orders_file: CSV file to read orders from
        start_val: total starting cash available
        frequency: the parameter of 'pd.date_range()', 'S' is refered to 'seconds'

    Returns
    -------
        portvals: portfolio value for each trading day from start_date to end_date (inclusive)
    """

    # Reference : http://quantsoftware.gatech.edu/images/a/a2/Marketsim-guidelines.pdf

    # Step 1 : read the dates and symbols from order file
    orders_df = pd.read_csv(orders_file, header=0, index_col=["Date"])
    symbols = list(set(orders_df["Symbol"]))

    # Step 2 : read actual values
    prices_df = helper.PredictiorGenerator().get_current(
        symbols, pd.date_range(start_date, end_date, freq = frequency))

    # Step 3 : create the matrix of shares
    # Create a dataframe which has all values as zero with index as dates and columns as symbols.
    # Trade Matrix
    '''
    Date AAPL MSFT
    12/1 0 0
    '''
    trading_df = pd.DataFrame(0, index=prices_df.index, columns=symbols)

    # Step 4 : calculate cash timeseriese and trading timeseriese
    '''
    For each order subtract the cash used in that trade.
    - Selling actually gives you cash.

    Date Cash
    12/1 10000
    12/2 -500
    '''
    cash_ts = pd.DataFrame(0, index=prices_df.index, columns=['Cash'], dtype=float)

    for date_index, row in orders_df.iterrows():

        if row['Order'] == 'BUY':
            trading_df.ix[date_index][row['Symbol']] += row['Shares']
            cash_ts.ix[date_index]['Cash'] -= row['Shares'] * prices_df.ix[date_index][row['Symbol']]

        elif row['Order'] == 'SELL':
            trading_df.ix[date_index][row['Symbol']] -= row['Shares']
            cash_ts.ix[date_index]['Cash'] += row['Shares'] * prices_df.ix[date_index][row['Symbol']]
        
    print('save data into trading file.')
    trading_df.to_csv('trading.txt')

    # Step 5 : calculate funds timeseriese
    cash_ts.ix[0] += start_val
    funds_ts = cash_ts.cumsum()

    # Step 6 :
    '''
    Use cummulative sum to convert the trade matrix into holding matrix.
    so that the holdings reflect the correct ammount of daily shares and funds show

    Example :

    PRICE >>
    Date\Sym AAPL MSFT
    12/1     400.0 30.0

    Holdings >>
    Date\Shares AAPL MSFT
    12/1        50.0 200.0

    Funds >>
    Date\Cash
    12/1       1000.0

    Date Value
    12/1 27,000.0  (400*50+30*200+1000)
    '''

    holdings_df = trading_df.cumsum()

    '''
    Now we have both the price and holding matrix.
    Use dot product to calculate value of portfolio on each date.
    '''

    port_value = pd.DataFrame(0, columns=['Value'], index=prices_df.index)
    port_value['Value'] = (prices_df * holdings_df).sum(axis=1)
    port_value['Value'] = (funds_ts['Cash']+port_value['Value'])
    
    return port_value


def get_portfolio_value(prices, allocs, start_val = 1):
    """Compute daily portfolio value given stock prices, allocations and starting value.

    Parameters
    ----------
        prices: daily prices for each stock in portfolio
        allocs: initial allocations, as fractions that sum to 1
        start_val: total starting value invested in portfolio (default: 1)

    Returns
    -------
        port_val: daily portfolio value
    """
    normed_vals = prices / prices.ix[0]
    allocated_vals = normed_vals*allocs
    pos_val = allocated_vals*start_val
    port_val = pos_val.sum(axis=1)

    return port_val


def get_rate_of_return(final_val, init_val):
    return final_val / init_val - 1


def get_rate_of_return_yearly(final_val, init_val, day_num):
    return (final_val / init_val - 1) / (day_num / 365.0)


def get_sharpe_ratio(rate_of_return_yearly, rf, port_val):
    """calculate the sharpe ratio

    Parameters
    ----------
        rate_of_return_yearly: the rate of strategy return yearly
        rf: Risk free interest rate (default 0.04)
        port_val: final value

    Returns
    -------
        sharpe_ratio: sharpe ratio
    """

    daily_returns = (port_val / port_val.shift(1))-1
    daily_returns[0] = 0
    std_daily_ret = daily_returns.std()
    sharpe_ratio = (rate_of_return_yearly - rf) / std_daily_ret
    return sharpe_ratio


def get_portfolio_stats(port_val, daily_rf = 0, samples_per_year=252):
    """Calculate statistics on given portfolio values.

    Parameters
    ----------
        port_val: daily portfolio value
        daily_rf: daily risk-free rate of return (default: 0%)
        samples_per_year: frequency of sampling (default: 252 trading days)

    Returns
    -------
        cum_ret: cumulative return
        avg_daily_ret: average of daily returns
        std_daily_ret: standard deviation of daily returns
        sharpe_ratio: annualized Sharpe ratio
    """

    k = np.sqrt(samples_per_year)
    daily_returns = (port_val / port_val.shift(1))-1
    cum_ret = (port_val[-1] / port_val[0]) - 1
    avg_daily_ret = daily_returns.mean()
    std_daily_ret = daily_returns.std()
    daily_returns[0] = 0
    sharpe_ratio = k * (np.mean(daily_returns - daily_rf) /
                        np.std(daily_returns))
    return cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio


def plot_normalized_data(df, title="Normalized prices", xlabel="Date", ylabel="Normalized price"):
    """Normalize given stock prices and plot for comparison.

    Parameters
    ----------
        df: DataFrame containing stock prices to plot (non-normalized)
        title: plot title
        xlabel: X-axis label
        ylabel: Y-axis label
    """
    df = df / df.ix[0]
    df.plot(figsize=(8, 5))
