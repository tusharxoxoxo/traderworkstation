Market Data: LiveCopy Location
Live Data LimitationsCopy Location
For all data, besides Delayed Watchlist Data, a paid data subscription is required to receive market data through the API. See the Market Data Subscriptions page for more information.

Live market data and historical bars are currently not available from the API for the exchange OSE. Only 15 minute delayed streaming data will be available for this exchange.

Some Available Tick Types may not be provided due to the contract details, the time that you run the code…… ,etc. To verify whether the specific Available Tick Type is provided, it is suggested to manually check the data in TWS.
Different Available Tick Types have different updating frequency.
The bid, ask, and last size quotes are displayed in shares instead of lots.

API users have the option to configure the TWS API to work in compatibility mode for older programs, but we recommend migrating to “quotes in shares” at your earliest convenience.

To display quotes as lots, from the Global Configuration > API > Settings page, check “Bypass US Stocks market data in shares warning for API orders.”

5 Second BarsCopy Location
Real time and historical data functionality is combined through the EClient.reqRealTimeBars request. reqRealTimeBars will create an active subscription that will return a single bar in real time every five seconds that has the OHLC values over that period. reqRealTimeBars can only be used with a bar size of 5 seconds.

Important: real time bars subscriptions combine the limitations of both, top and historical market data. Make sure you observe Market Data Lines and Pacing Violations for Small Bars (30 secs or less). For example, no more than 60 _new_ requests for real time bars can be made in 10 minutes, and the total number of active active subscriptions of all types cannot exceed the maximum allowed market data lines for the user.

Request Real Time BarsCopy Location
EClient.reqRealTimeBars (
tickerId: int. Request identifier used to track data.

contract: Contract. The Contract object for which the depth is being requested

barSize: int. Currently being ignored

whatToShow: String. The nature of the data being retrieved:
Available Values: TRADES, MIDPOINT, BID, ASK

useRTH: int. Set to 0 to obtain the data which was also generated outside of the Regular Trading Hours, set to 1 to obtain only the RTH data
)

realTimeBarOptions: List<TagValue>. Internal use only.

Requests real time bars.

Only 5 seconds bars are provided. This request is subject to the same pacing as any historical data request: no more than 60 API queries in more than 600 seconds.

Real time bars subscriptions are also included in the calculation of the number of Level 1 market data subscriptions allowed in an account.

Python
Java
C++
C#
VB.NET
self.reqRealTimeBars(3001, contract, 5, "MIDPOINT", 0, [])

Code example:

from ibapi.client import _
from ibapi.wrapper import _
from ibapi.contract import Contract
import time
class TradeApp(EWrapper, EClient):
def **init**(self):
EClient.**init**(self, self)
def realtimeBar(self, reqId: TickerId, time:int, open*: float, high: float, low: float, close: float, volume: Decimal, wap: Decimal, count: int):
print("RealTimeBar. TickerId:", reqId, RealTimeBar(time, -1, open*, high, low, close, volume, wap, count))

app = TradeApp()  
app.connect("127.0.0.1", 7496, clientId=1)
contract = Contract()
contract.symbol = "AAPL"
contract.secType = "STK"
contract.currency = "USD"
contract.exchange = "SMART"
app.reqRealTimeBars(3001, contract, 5, "TRADES", 0, [])
app.run()

Receive Real Time BarsCopy Location
EWrapper.realtimeBar (
reqId: int. Request identifier used to track data.

time: long. The bar’s start date and time (Epoch/Unix time)

open: double. The bar’s open point

high: double. The bar’s high point

low: double. The bar’s low point

close: double. The bar’s closing point

volume: decimal. The bar’s traded volume (only returned for TRADES data)

WAP: decimal. The bar’s Weighted Average Price rounded to minimum increment (only available for TRADES).

count: int. The number of trades during the bar’s timespan (only available for TRADES).
)

Receives the real time 5 second bars.

Python
Java
C++
C#
VB.NET
def realtimeBar(self, reqId: TickerId, time:int, open*: float, high: float, low: float, close: float, volume: Decimal, wap: Decimal, count: int):
print("RealTimeBar. TickerId:", reqId, RealTimeBar(time, -1, open*, high, low, close, volume, wap, count))

Cancel Real Time BarsCopy Location
EClient.cancelRealTimeBars (
tickerId: int. Request identifier used to track data.
)

Cancels Real Time Bars’ subscription.

Python
Java
C++
C#
VB.NET
self.cancelRealTimeBars(3001)
