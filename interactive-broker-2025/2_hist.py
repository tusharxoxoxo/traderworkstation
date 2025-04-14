


from ib_async import *
# util.startLoop()  # uncomment this line when in a notebook
import time
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=2)

ib.reqMarketDataType(4)  # Use free, delayed, frozen data
contract = ib.qualifyContracts(Future(symbol='BANKNIFTY',currency='INR',exchange='NSE',lastTradeDateOrContractMonth='202501'))[0]
# contract = ib.qualifyContracts(Future(symbol='BANKNIFTY',currency='INR',exchange='NSE',lastTradeDateOrContractMonth='20250227'))[0]
# contract=Contract(symbol='BANKNIFTY',currency='INR',exchange='NSE',secType='IND')
print(contract)

ct=time.time()

import datetime as dt
bars = ib.reqHistoricalData(
    contract, endDateTime=dt.datetime.now(), durationStr='10 D',
    barSizeSetting='1 hour', whatToShow='TRADES', useRTH=True)

# convert to pandas dataframe (pandas needs to be installed):
df = util.df(bars)
print(df)

time_taken=time.time()-ct
print(time_taken)


