import stocktrader as s

# Task 5.5
if __name__ == "__main__":
    s.loadPortfolio()
    val1 = s.valuatePortfolio(verbose=True)
    trans = { 'date':'2013-08-12', 'symbol':'SKY', 'volume':-5 }
    s.addTransaction(trans, verbose=True)
    val2 = s.valuatePortfolio(verbose=True)
    print("Hurray, we have increased our portfolio value by £{:.2f}!".format(val2-val1))
