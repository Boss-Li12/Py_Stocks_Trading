"""
stocktrader -- A Python module for virtual stock trading
TODO: Add a description of the module...

description:
The module  allows the user to load historical financial data
and to simulate the buying and selling of shares on the stock market.

Also fill out the personal fields below.

Full name: Peter Pan
StudentId: 123456
Email: peter.pan.123@student.manchester.ac.uk
"""
import datetime
import csv
import os


class TransactionError(Exception):
    '''This exception will be thrown if the Transaction is invalid'''
    def __init__(self, tran):
        '''input data'''
        self.tran = tran

    def __str__(self):
        '''Returns a description of the exception'''
        return f'{self.tran} is not an expected input '

class DateError(Exception):
    '''This exception will be thrown if you enter non-standard date data'''
    def __init__(self, date):
        '''input data'''
        self.date = date

    def __str__(self):
        '''Returns a description of the exception'''
        return f'{self.date} is not an expected input '



stocks = {}
portfolio = {}
transactions = []


# Task 1
def normaliseDate(s): 
    '''format the input date to YYYY-MM-DD
    :param s: str, the input date
    :return: str, the formatted date
    a DateError Exception will be raised if the input date is not in the expected format
    '''
    try:
        if type(s) != str:
            raise DateError(s)

        if '.' in s:
            s = datetime.datetime.strptime(s, '%d.%m.%Y')
        elif '/' in s:
            s = datetime.datetime.strptime(s, '%Y/%m/%d')
        elif '-' in s:
            s = datetime.datetime.strptime(s, '%Y-%m-%d')
        else:
            raise DateError(s)
    except Exception:
        raise DateError(s)
    else:
        return s.strftime('%Y-%m-%d')

    #return datetime.datetime.strptime('22.9.2012', '%d.%m.%Y').strftime('%Y-%m-%d')
    #return datetime.datetime.strptime('2019/9/22', '%Y/%m/%d').strftime('%Y-%m-%d')

# TODO: All other functions from the tasks go here

# Task 2
def loadStock(symbol):
    '''load the stock data from the corresponding CSV
    :param symbol: str, the symbol of a stock
    :return: None
    a FileNotFoundError Exception will be raised if the .csv file is not found
    '''
    global stocks

    fname = symbol + '.csv'
    with open(fname) as f:
        reader = csv.reader(f)
        # skip the header_row
        next(reader)

        stock_data = {}
        for row in reader:
            stock_data[normaliseDate(row[0])] = [float(row[1]), float(row[2]), float(row[3]), float(row[4])]
        stocks[symbol] = stock_data

    return

# Task 3
def loadPortfolio(fname = 'portfolio.csv'):
    ''' This function loads the data from the file and assigns them to the portfolio dictionary
    :param fname: the filename
    :return: None
    a FileNotFoundError Exception will be raised if the .csv file is not found
    a ValueError Exception will be raised if exists some invalid data
    '''
    # empty the global variances
    global portfolio
    global transactions
    global SYMBOLS

    portfolio = {}
    transactions = []

    # load the data from portfolio.csv into the dictionary portfolio
    symbols = []
    with open(fname) as f:
        reader = csv.reader(f)
        row_counter = 1
        for row in reader:
            if row_counter == 1:
                portfolio['date'] = normaliseDate(row[0])
            elif row_counter == 2:
                portfolio['cash'] = float(row[0])
            else:
                portfolio[row[0]] = int(row[1])
                symbols.append(row[0])
            row_counter += 1

    # load the corresponding stock data into the dictionary stocks
    for symbol in symbols:
        loadStock(symbol)

    return


# Task 4
def valuatePortfolio(date = None, verbose = False):
    '''The function valuates the portfolio at a given date and returns a floating point number corresponding to its total value
    :param date: a given date
    :param verbose: Boolean, show details or not
    :return: float, the total value
    a DateError Exception will be raised if the date is earlier than the date of the portfolio
    or the date is not a trading day
    '''
    global portfolio
    global stocks

    if date is None:
        date = portfolio['date']

    if normaliseDate(date) < normaliseDate(portfolio['date']):
        raise DateError(date)

    # calculate the total value
    total = portfolio['cash']
    cash = portfolio['cash']
    symbols = []
    for key in portfolio:
        symbol = None
        if key != 'cash' and key != 'date':
            symbol = key
        if symbol is not None:
            try:
                symbols.append([symbol, portfolio[symbol], stocks[symbol][normaliseDate(date)][2]])
                total += portfolio[symbol] * stocks[symbol][normaliseDate(date)][2]
            except:
                raise DateError(date)

    # display the details
    if verbose is True:
        print(f' Your portfolio on {normaliseDate(date)}:')
        print(f' [* share values based on the lowest price on {normaliseDate(date)}]')
        print("\n")
        print(" Capital type          | Volume | Val/Unit* | Value in £*")
        print("-----------------------+--------+-----------+-------------")
        #print(f' Cash                  |      1 |  {cash:.2f} |    {cash:.2f}')
        print(f' Cash'.ljust(22), "|", '1'.rjust(6), "|", f'{cash:.2f}'.rjust(9), "|", f'   {cash:.2f}')
        for symbol in symbols :
            if symbol[1] != 0:
                print(f' Shares of {symbol[0]}'.ljust(22), "|", f'{symbol[1]}'.rjust(6), "|", f'{symbol[2]:.2f}'.rjust(9), "|", f'   {(symbol[1] * symbol[2]):.2f}')
                #print(f' Shares of {symbol[0]}         |      {symbol[1]} |    {symbol[2]:.2f} |     {(symbol[1] * symbol[2]):.2f} ')
        print("-----------------------+--------+-----------+-------------")
        print(f' TOTAL VALUE                                     {total:.2f}')
        print("\n")
        print("\n")
    return total


# Task 5
def addTransaction(trans, verbose = False):
    '''add a Transaction, update the portfolio and trans
    :param trans: dict, the information of the transaction
    :param verbose: boolean, show the details or not
    :return: None
    DateError: the date of the transaction is earlier than the date of the portfolio
    ValueError: the symbol value of the transaction is not listed in the stocks dictionary
    TransactionError: don't have enough cash to buy or don't have enough shares to sell
    '''
    global portfolio
    global transactions
    global stocks

    # if the date of the transaction is earlier than the date of the portfolio
    if normaliseDate(trans['date']) < normaliseDate(portfolio['date']):
        raise DateError(trans['date'])

    # update the date of portfolio to the date of the transaction
    portfolio['date'] = normaliseDate(trans['date'])

    # if the symbol value of the transaction is not listed in the stocks dictionary
    if trans['symbol'] not in stocks:
        raise ValueError("the symbol value of the transaction is not listed in the stocks dictionary")

    # buy some shares
    if trans['volume'] > 0:
        # do not have enough money
        if portfolio['cash'] < trans['volume'] * stocks[trans['symbol']][normaliseDate(trans['date'])][1]:
            raise TransactionError(trans)
        # expected situation
        if trans['symbol'] in portfolio:
            portfolio[trans['symbol']] += trans['volume']
        else:
            portfolio[trans['symbol']] = trans['volume']
        portfolio['cash'] -= trans['volume'] * stocks[trans['symbol']][normaliseDate(trans['date'])][1]
        transactions.append(trans)
        if verbose is True:
            date = normaliseDate(trans['date'])
            num = trans['volume']
            sym = trans['symbol']
            total = trans['volume'] * stocks[trans['symbol']][normaliseDate(trans['date'])][1]
            cash = portfolio['cash']
            print(f'{date}: Bought {num} shares of {sym} for a total of £{total:.2f}')
            print(f'Remaining cash: £{cash:.2f}')
            print("\n")
            print("\n")
    # sell some shares
    else:
        # do not have enough shares
        if trans['volume'] > portfolio[trans['symbol']]:
            raise TransactionError(trans)
        # expected situation
        portfolio[trans['symbol']] += trans['volume']
        portfolio['cash'] -= trans['volume'] * stocks[trans['symbol']][normaliseDate(trans['date'])][2]
        transactions.append(trans)
        if verbose is True:
            date = normaliseDate(trans['date'])
            num = -trans['volume']
            sym = trans['symbol']
            total = -trans['volume'] * stocks[trans['symbol']][normaliseDate(trans['date'])][2]
            cash = portfolio['cash']
            print(f'{date}: Sold {num} shares of {sym} for a total of £{total:.2f}')
            print(f'Available cash: £{cash:.2f}')
            print("\n")
            print("\n")


# Task 6
def savePortfolio(fname = 'portfolio.csv'):
    '''saves the current dictionary portfolio to a CSV file
    :param fname: string, the file name
    :return: None
    '''
    global portfolio

    csv_data = []
    for key in portfolio:
        if key == 'date' or key == 'cash':
            csv_data.append([str(portfolio[key])])

        else:
            csv_data.append([key, portfolio[key]])

    # write the data to fname
    with open(fname, 'w', newline = '') as f:
        csv_writer = csv.writer(f)
        for r in csv_data:
            csv_writer.writerow(r)

    return


# Task 7
def sellAll(date = None, verbose = False):
    '''sells all shares in the portfolio on a particular date
    :param date: str, a particular date
    :param verbose: boolean, show the details or not
    :return: None
    '''
    global portfolio
    global stocks

    if date is None:
        date = portfolio['date']

    # sell all the stocks
    for key in portfolio:
        if key != 'cash' and key != 'date':
            trans = {}
            trans['date'] = date
            trans['symbol'] = key
            trans['volume'] = -portfolio[key]
            if trans['volume'] != 0:
                addTransaction(trans, verbose)

    return

# Task 8
def loadAllStocks():
    '''loads all stocks into the dictionary stocks
    :return: None
    '''
    # get all the files in the current dir
    symbols = []
    filelist = os.listdir()
    for file in filelist:
        if os.path.splitext(file)[1] == '.csv' and \
           os.path.splitext(file)[0].isupper():
            symbols.append(os.path.splitext(file)[0])

    #print(symbols)
    for symbol in symbols:
        try:
            loadStock(symbol)
            #print(symbol)
        except:
            # just ignore
            pass

    return


# Task 9
# the core strategy
def tradeStrategy1(verbose = False):
    '''buys and sells shares automatically
    :param verbose: boolean, show the details or not
    :return: None
    '''
    global stocks
    global portfolio

    # get all trading days from stocks
    trading_days = []
    for key in stocks:
        for date in stocks[key]:
            trading_days.append(date)
        break
    #print(trading_days)

    # find the first index cur_j such that portfolio['date'] < trading_days[cur_j]
    # so we buy some stocks in trading_days[cur_j]
    cur_j = 0
    while portfolio['date'] > trading_days[cur_j]:
        cur_j += 1
    if cur_j < 9:
        cur_j = 9
    #print(trading_days[cur_j])

    # go to the main loop
    # whether to buy(which?volume?)
    # whether to sell
    now_symbol = ""
    H_sj = 0
    for j in range(cur_j, len(trading_days)):
        # decide which to buy
        if now_symbol == "":
            max_Q_buy = 0
            # which to buy
            for symbol in stocks:
                Numerator = 10 * stocks[symbol][trading_days[j]][1]
                denominator = 0
                for i in range(10):
                    denominator += stocks[symbol][trading_days[j - i]][1]
                Q_buy = Numerator / denominator
                if Q_buy > max_Q_buy:
                    max_Q_buy = Q_buy
                    now_symbol = symbol
                    H_sj = stocks[symbol][trading_days[j]][1]
                elif Q_buy == max_Q_buy and symbol < now_symbol:
                    now_symbol = symbol
                    H_sj = stocks[symbol][trading_days[j]][1]
            # the max volume
            max_volume = int(portfolio['cash'] // H_sj)
            trans = {}
            trans['date'] = trading_days[j]
            trans['symbol'] = now_symbol
            trans['volume'] = max_volume
            if trans['volume'] != 0:
                addTransaction(trans, verbose)
        # sell or not
        else:
            L_sk = stocks[now_symbol][trading_days[j]][2]
            Q_sell = L_sk / H_sj
            if Q_sell < 0.7 or Q_sell > 1.3:
                sellAll(trading_days[j], verbose)
                # clear
                now_symbol = ""
                H_sj = 0

    return

def main():
    # Test your functions here
    # print(normaliseDate('8.5.212'))
    # loadStock('XYZ')
    # loadStock('EZJ')
    # print(stocks)
    loadPortfolio()
    # loadPortfolio('a.csv')
    # loadPortfolio('portfolio_faulty.csv')
    print(portfolio)
    #print(stocks['SKY'])
    #print(stocks['EZJ'])
    #print(valuatePortfolio('2012-2-6', True))
    #print(valuatePortfolio('2012-1-3'))
    #print(valuatePortfolio('2012-2-12'))
    #print(addTransaction({ 'date':'2013-08-12', 'symbol':'SKY', 'volume':2 }, True))
    print(addTransaction({'date': '2013-08-12', 'symbol': 'SKY', 'volume':-5}, True))
    #print(addTransaction({'date': '2013-08-12', 'symbol': 'SKY', 'volume':5}, True))
    print(portfolio)
    #print(transactions)
    #savePortfolio('portfolio1.csv')
    #sellAll(verbose = True)
    #print(portfolio)
    loadAllStocks()
    print(len(stocks))
    return



# the following allows your module to be run as a program
if __name__ == '__main__' or __name__ == 'builtins':
    main()

