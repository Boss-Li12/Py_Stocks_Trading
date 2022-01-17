import stocktrader as s

# Task 9
if __name__ == "__main__":
    s.loadPortfolio('portfolio0.csv')
    s.loadAllStocks()
    s.valuatePortfolio(verbose=True)
    s.tradeStrategy1(verbose=True)
    s.valuatePortfolio('2018-03-13', verbose=True)

