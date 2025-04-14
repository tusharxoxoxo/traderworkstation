 ib_async
1.0
Search docs
ib_async
API docs
IB
Client
Order
Contract
Ticker
Objects
Utilities
FlexReport
IBC
Watchdog
Notebooks
Code recipes
Source code
ib_async Changelog
Links
 API docsView page source
API docs
Release 1.0.3.

Also see the official Python API documentation from IB.

IB
High-level interface to Interactive Brokers.

classib_async.ib.StartupFetch(value, names=<not given>, *values, module=None, qualname=None, type=None, start=1, boundary=None)[source]
POSITIONS= 1
ORDERS_OPEN= 2
ORDERS_COMPLETE= 4
ACCOUNT_UPDATES= 8
SUB_ACCOUNT_UPDATES= 16
EXECUTIONS= 32
classib_async.ib.IB[source]
Provides both a blocking and an asynchronous interface to the IB API, using asyncio networking and event loop.

The IB class offers direct access to the current state, such as orders, executions, positions, tickers etc. This state is automatically kept in sync with the TWS/IBG application.

This class has most request methods of EClient, with the same names and parameters (except for the reqId parameter which is not needed anymore). Request methods that return a result come in two versions:

Blocking: Will block until complete and return the result. The current state will be kept updated while the request is ongoing;

Asynchronous: All methods that have the “Async” postfix. Implemented as coroutines or methods that return a Future and intended for advanced users.

The One Rule:

While some of the request methods are blocking from the perspective of the user, the framework will still keep spinning in the background and handle all messages received from TWS/IBG. It is important to not block the framework from doing its work. If, for example, the user code spends much time in a calculation, or uses time.sleep() with a long delay, the framework will stop spinning, messages accumulate and things may go awry.

The one rule when working with the IB class is therefore that

user code may not block for too long.

To be clear, the IB request methods are okay to use and do not count towards the user operation time, no matter how long the request takes to finish.

So what is “too long”? That depends on the situation. If, for example, the timestamp of tick data is to remain accurate within a millisecond, then the user code must not spend longer than a millisecond. If, on the other extreme, there is very little incoming data and there is no desire for accurate timestamps, then the user code can block for hours.

If a user operation takes a long time then it can be farmed out to a different process. Alternatively the operation can be made such that it periodically calls IB.sleep(0); This will let the framework handle any pending work and return when finished. The operation should be aware that the current state may have been updated during the sleep(0) call.

For introducing a delay, never use time.sleep() but use sleep() instead.

Parameters
:
RequestTimeout (float) – Timeout (in seconds) to wait for a blocking request to finish before raising asyncio.TimeoutError. The default value of 0 will wait indefinitely. Note: This timeout is not used for the *Async methods.

RaiseRequestErrors (bool) –

Specifies the behaviour when certain API requests fail:

False: Silently return an empty result;

True: Raise a RequestError.

MaxSyncedSubAccounts (int) – Do not use sub-account updates if the number of sub-accounts exceeds this number (50 by default).

TimezoneTWS (str) – Specifies what timezone TWS (or gateway) is using. The default is to assume local system timezone.

Events:
connectedEvent (): Is emitted after connecting and synchronzing with TWS/gateway.

disconnectedEvent (): Is emitted after disconnecting from TWS/gateway.

updateEvent (): Is emitted after a network packet has been handled.

pendingTickersEvent (tickers: Set[Ticker]): Emits the set of tickers that have been updated during the last update and for which there are new ticks, tickByTicks or domTicks.

barUpdateEvent (bars: BarDataList, hasNewBar: bool): Emits the bar list that has been updated in real time. If a new bar has been added then hasNewBar is True, when the last bar has changed it is False.

newOrderEvent (trade: Trade): Emits a newly placed trade.

orderModifyEvent (trade: Trade): Emits when order is modified.

cancelOrderEvent (trade: Trade): Emits a trade directly after requesting for it to be cancelled.

openOrderEvent (trade: Trade): Emits the trade with open order.

orderStatusEvent (trade: Trade): Emits the changed order status of the ongoing trade.

execDetailsEvent (trade: Trade, fill: Fill): Emits the fill together with the ongoing trade it belongs to.

commissionReportEvent (trade: Trade, fill: Fill, report: CommissionReport): The commission report is emitted after the fill that it belongs to.

updatePortfolioEvent (item: PortfolioItem): A portfolio item has changed.

positionEvent (position: Position): A position has changed.

accountValueEvent (value: AccountValue): An account value has changed.

accountSummaryEvent (value: AccountValue): An account value has changed.

pnlEvent (entry: PnL): A profit- and loss entry is updated.

pnlSingleEvent (entry: PnLSingle): A profit- and loss entry for a single position is updated.

tickNewsEvent (news: NewsTick): Emit a new news headline.

newsBulletinEvent (bulletin: NewsBulletin): Emit a new news bulletin.

scannerDataEvent (data: ScanDataList): Emit data from a scanner subscription.

wshMetaEvent (dataJson: str): Emit WSH metadata.

wshEvent (dataJson: str): Emit WSH event data (such as earnings dates, dividend dates, options expiration dates, splits, spinoffs and conferences).

errorEvent (reqId: int, errorCode: int, errorString: str, contract: Contract): Emits the reqId/orderId and TWS error code and string (see https://interactivebrokers.github.io/tws-api/message_codes.html) together with the contract the error applies to (or None if no contract applies).

timeoutEvent (idlePeriod: float): Is emitted if no data is received for longer than the timeout period specified with setTimeout(). The value emitted is the period in seconds since the last update.

Note that it is not advisable to place new requests inside an event handler as it may lead to too much recursion.

events= ('connectedEvent', 'disconnectedEvent', 'updateEvent', 'pendingTickersEvent', 'barUpdateEvent', 'newOrderEvent', 'orderModifyEvent', 'cancelOrderEvent', 'openOrderEvent', 'orderStatusEvent', 'execDetailsEvent', 'commissionReportEvent', 'updatePortfolioEvent', 'positionEvent', 'accountValueEvent', 'accountSummaryEvent', 'pnlEvent', 'pnlSingleEvent', 'scannerDataEvent', 'tickNewsEvent', 'newsBulletinEvent', 'wshMetaEvent', 'wshEvent', 'errorEvent', 'timeoutEvent')
RequestTimeout: float= 0
RaiseRequestErrors: bool= False
MaxSyncedSubAccounts: int= 50
TimezoneTWS: str= ''
connect(host='127.0.0.1', port=7497, clientId=1, timeout=4, readonly=False, account='', raiseSyncErrors=False, fetchFields=<StartupFetch.POSITIONS|ORDERS_OPEN|ORDERS_COMPLETE|ACCOUNT_UPDATES|SUB_ACCOUNT_UPDATES|EXECUTIONS: 63>)[source]
Connect to a running TWS or IB gateway application. After the connection is made the client is fully synchronized and ready to serve requests.

This method is blocking.

Parameters
:
host (str) – Host name or IP address.

port (int) – Port number.

clientId (int) – ID number to use for this client; must be unique per connection. Setting clientId=0 will automatically merge manual TWS trading with this client.

timeout (float) – If establishing the connection takes longer than timeout seconds then the asyncio.TimeoutError exception is raised. Set to 0 to disable timeout.

readonly (bool) – Set to True when API is in read-only mode.

account (str) – Main account to receive updates for.

raiseSyncErrors (bool) –

When True this will cause an initial
sync request error to raise a ConnectionError`. When False the error will only be logged at error level.

fetchFields: By default, all account data is loaded and cached
when a new connection is made. You can optionally disable all or some of the account attribute fetching during a connection using the StartupFetch field flags. See StartupFetch in ib.py for member details. There is also StartupFetchNONE and StartupFetchALL as shorthand. Individual flag field members can be added or removed to the fetchFields parameter as needed.

disconnect()[source]
Disconnect from a TWS or IB gateway application. This will clear all session state.

isConnected()[source]
Is there an API connection to TWS or IB gateway?

Return type
:
bool

staticrun(*, timeout=None)
By default run the event loop forever.

When awaitables (like Tasks, Futures or coroutines) are given then run the event loop until each has completed and return their results.

An optional timeout (in seconds) can be given that will raise asyncio.TimeoutError if the awaitables are not ready within the timeout period.

staticschedule(callback, *args)
Schedule the callback to be run at the given time with the given arguments. This will return the Event Handle.

Parameters
:
time (Union[time, datetime]) – Time to run callback. If given as datetime.time then use today as date.

callback (Callable) – Callable scheduled to run.

args – Arguments for to call callback with.

staticsleep()
Wait for the given amount of seconds while everything still keeps processing in the background. Never use time.sleep().

Parameters
:
secs (float) – Time in seconds to wait.

Return type
:
bool

statictimeRange(end, step)
Iterator that waits periodically until certain time points are reached while yielding those time points.

Parameters
:
start (Union[time, datetime]) – Start time, can be specified as datetime.datetime, or as datetime.time in which case today is used as the date

end (Union[time, datetime]) – End time, can be specified as datetime.datetime, or as datetime.time in which case today is used as the date

step (float) – The number of seconds of each period

Return type
:
Iterator[datetime]

statictimeRangeAsync(end, step)
Async version of timeRange().

Return type
:
AsyncIterator[datetime]

staticwaitUntil()
Wait until the given time t is reached.

Parameters
:
t (Union[time, datetime]) – The time t can be specified as datetime.datetime, or as datetime.time in which case today is used as the date.

Return type
:
bool

waitOnUpdate(timeout=0)[source]
Wait on any new update to arrive from the network.

Parameters
:
timeout (float) – Maximum time in seconds to wait. If 0 then no timeout is used.

Note

A loop with waitOnUpdate should not be used to harvest tick data from tickers, since some ticks can go missing. This happens when multiple updates occur almost simultaneously; The ticks from the first update are then cleared. Use events instead to prevent this.

Return type
:
bool

Returns
:
True if not timed-out, False otherwise.

loopUntil(condition=None, timeout=0)[source]
Iterate until condition is met, with optional timeout in seconds. The yielded value is that of the condition or False when timed out.

Parameters
:
condition – Predicate function that is tested after every network

update.

timeout (float) – Maximum time in seconds to wait. If 0 then no timeout is used.

Return type
:
Iterator[object]

setTimeout(timeout=60)[source]
Set a timeout for receiving messages from TWS/IBG, emitting timeoutEvent if there is no incoming data for too long.

The timeout fires once per connected session but can be set again after firing or after a reconnect.

Parameters
:
timeout (float) – Timeout in seconds.

managedAccounts()[source]
List of account names.

Return type
:
List[str]

accountValues(account='')[source]
List of account values for the given account, or of all accounts if account is left blank.

Parameters
:
account (str) – If specified, filter for this account name.

Return type
:
List[AccountValue]

accountSummary(account='')[source]
List of account values for the given account, or of all accounts if account is left blank.

This method is blocking on first run, non-blocking after that.

Parameters
:
account (str) – If specified, filter for this account name.

Return type
:
List[AccountValue]

portfolio(account='')[source]
List of portfolio items for the given account, or of all retrieved portfolio items if account is left blank.

Parameters
:
account (str) – If specified, filter for this account name.

Return type
:
List[PortfolioItem]

positions(account='')[source]
List of positions for the given account, or of all accounts if account is left blank.

Parameters
:
account (str) – If specified, filter for this account name.

Return type
:
List[Position]

pnl(account='', modelCode='')[source]
List of subscribed PnL objects (profit and loss), optionally filtered by account and/or modelCode.

The PnL objects are kept live updated.

Parameters
:
account – If specified, filter for this account name.

modelCode – If specified, filter for this account model.

Return type
:
List[PnL]

pnlSingle(account='', modelCode='', conId=0)[source]
List of subscribed PnLSingle objects (profit and loss for single positions).

The PnLSingle objects are kept live updated.

Parameters
:
account (str) – If specified, filter for this account name.

modelCode (str) – If specified, filter for this account model.

conId (int) – If specified, filter for this contract ID.

Return type
:
List[PnLSingle]

trades()[source]
List of all order trades from this session.

Return type
:
List[Trade]

openTrades()[source]
List of all open order trades.

Return type
:
List[Trade]

orders()[source]
List of all orders from this session.

Return type
:
List[Order]

openOrders()[source]
List of all open orders.

Return type
:
List[Order]

fills()[source]
List of all fills from this session.

Return type
:
List[Fill]

executions()[source]
List of all executions from this session.

Return type
:
List[Execution]

ticker(contract)[source]
Get ticker of the given contract. It must have been requested before with reqMktData with the same contract object. The ticker may not be ready yet if called directly after reqMktData().

Parameters
:
contract (Contract) – Contract to get ticker for.

Return type
:
Optional[Ticker]

tickers()[source]
Get a list of all tickers.

Return type
:
List[Ticker]

pendingTickers()[source]
Get a list of all tickers that have pending ticks or domTicks.

Return type
:
List[Ticker]

realtimeBars()[source]
Get a list of all live updated bars. These can be 5 second realtime bars or live updated historical bars.

Return type
:
List[Union[BarDataList, RealTimeBarList]]

newsTicks()[source]
List of ticks with headline news. The article itself can be retrieved with reqNewsArticle().

Return type
:
List[NewsTick]

newsBulletins()[source]
List of IB news bulletins.

Return type
:
List[NewsBulletin]

reqTickers(*contracts, regulatorySnapshot=False)[source]
Request and return a list of snapshot tickers. The list is returned when all tickers are ready.

This method is blocking.

Parameters
:
contracts (Contract) – Contracts to get tickers for.

regulatorySnapshot (bool) – Request NBBO snapshots (may incur a fee).

Return type
:
List[Ticker]

qualifyContracts(*contracts)[source]
Fully qualify the given contracts in-place. This will fill in the missing fields in the contract, especially the conId.

Returns a list of contracts that have been successfully qualified.

This method is blocking.

Parameters
:
contracts (Contract) – Contracts to qualify.

Return type
:
List[Contract]

bracketOrder(action, quantity, limitPrice, takeProfitPrice, stopLossPrice, **kwargs)[source]
Create a limit order that is bracketed by a take-profit order and a stop-loss order. Submit the bracket like:

for o in bracket:
    ib.placeOrder(contract, o)
https://interactivebrokers.github.io/tws-api/bracket_order.html

Parameters
:
action (str) – ‘BUY’ or ‘SELL’.

quantity (float) – Size of order.

limitPrice (float) – Limit price of entry order.

takeProfitPrice (float) – Limit price of profit order.

stopLossPrice (float) – Stop price of loss order.

Return type
:
BracketOrder

staticoneCancelsAll(orders, ocaGroup, ocaType)[source]
Place the trades in the same One Cancels All (OCA) group.

https://interactivebrokers.github.io/tws-api/oca.html

Parameters
:
orders (List[Order]) – The orders that are to be placed together.

Return type
:
List[Order]

whatIfOrder(contract, order)[source]
Retrieve commission and margin impact without actually placing the order. The given order will not be modified in any way.

This method is blocking.

Parameters
:
contract (Contract) – Contract to test.

order (Order) – Order to test.

Return type
:
OrderState

placeOrder(contract, order)[source]
Place a new order or modify an existing order. Returns a Trade that is kept live updated with status changes, fills, etc.

Parameters
:
contract (Contract) – Contract to use for order.

order (Order) – The order to be placed.

Return type
:
Trade

cancelOrder(order, manualCancelOrderTime='')[source]
Cancel the order and return the Trade it belongs to.

Parameters
:
order (Order) – The order to be canceled.

manualCancelOrderTime (str) – For audit trail.

Return type
:
Optional[Trade]

reqGlobalCancel()[source]
Cancel all active trades including those placed by other clients or TWS/IB gateway.

reqCurrentTime()[source]
Request TWS current time.

This method is blocking.

Return type
:
datetime

reqAccountUpdates(account='')[source]
This is called at startup - no need to call again.

Request account and portfolio values of the account and keep updated. Returns when both account values and portfolio are filled.

This method is blocking.

Parameters
:
account (str) – If specified, filter for this account name.

reqAccountUpdatesMulti(account='', modelCode='')[source]
It is recommended to use accountValues() instead.

Request account values of multiple accounts and keep updated.

This method is blocking.

Parameters
:
account (str) – If specified, filter for this account name.

modelCode (str) – If specified, filter for this account model.

reqAccountSummary()[source]
It is recommended to use accountSummary() instead.

Request account values for all accounts and keep them updated. Returns when account summary is filled.

This method is blocking.

reqAutoOpenOrders(autoBind=True)[source]
Bind manual TWS orders so that they can be managed from this client. The clientId must be 0 and the TWS API setting “Use negative numbers to bind automatic orders” must be checked.

This request is automatically called when clientId=0.

https://interactivebrokers.github.io/tws-api/open_orders.html https://interactivebrokers.github.io/tws-api/modifying_orders.html

Parameters
:
autoBind (bool) – Set binding on or off.

reqOpenOrders()[source]
Request and return a list of open orders.

This method can give stale information where a new open order is not reported or an already filled or cancelled order is reported as open. It is recommended to use the more reliable and much faster openTrades() or openOrders() methods instead.

This method is blocking.

Return type
:
List[Trade]

reqAllOpenOrders()[source]
Request and return a list of all open orders over all clients. Note that the orders of other clients will not be kept in sync, use the master clientId mechanism instead to see other client’s orders that are kept in sync.

Return type
:
List[Trade]

reqCompletedOrders(apiOnly)[source]
Request and return a list of completed trades.

Parameters
:
apiOnly (bool) – Request only API orders (not manually placed TWS orders).

Return type
:
List[Trade]

reqExecutions(execFilter=None)[source]
It is recommended to use fills() or executions() instead.

Request and return a list of fills.

This method is blocking.

Parameters
:
execFilter (Optional[ExecutionFilter]) – If specified, return executions that match the filter.

Return type
:
List[Fill]

reqPositions()[source]
It is recommended to use positions() instead.

Request and return a list of positions for all accounts.

This method is blocking.

Return type
:
List[Position]

reqPnL(account, modelCode='')[source]
Start a subscription for profit and loss events.

Returns a PnL object that is kept live updated. The result can also be queried from pnl().

https://interactivebrokers.github.io/tws-api/pnl.html

Parameters
:
account (str) – Subscribe to this account.

modelCode (str) – If specified, filter for this account model.

Return type
:
PnL

cancelPnL(account, modelCode='')[source]
Cancel PnL subscription.

Parameters
:
account – Cancel for this account.

modelCode (str) – If specified, cancel for this account model.

reqPnLSingle(account, modelCode, conId)[source]
Start a subscription for profit and loss events for single positions.

Returns a PnLSingle object that is kept live updated. The result can also be queried from pnlSingle().

https://interactivebrokers.github.io/tws-api/pnl.html

Parameters
:
account (str) – Subscribe to this account.

modelCode (str) – Filter for this account model.

conId (int) – Filter for this contract ID.

Return type
:
PnLSingle

cancelPnLSingle(account, modelCode, conId)[source]
Cancel PnLSingle subscription for the given account, modelCode and conId.

Parameters
:
account (str) – Cancel for this account name.

modelCode (str) – Cancel for this account model.

conId (int) – Cancel for this contract ID.

reqContractDetails(contract)[source]
Get a list of contract details that match the given contract. If the returned list is empty then the contract is not known; If the list has multiple values then the contract is ambiguous.

The fully qualified contract is available in the the ContractDetails.contract attribute.

This method is blocking.

https://interactivebrokers.github.io/tws-api/contract_details.html

Parameters
:
contract (Contract) – The contract to get details for.

Return type
:
List[ContractDetails]

reqMatchingSymbols(pattern)[source]
Request contract descriptions of contracts that match a pattern.

This method is blocking.

https://interactivebrokers.github.io/tws-api/matching_symbols.html

Parameters
:
pattern (str) – The first few letters of the ticker symbol, or for longer strings a character sequence matching a word in the security name.

Return type
:
List[ContractDescription]

reqMarketRule(marketRuleId)[source]
Request price increments rule.

https://interactivebrokers.github.io/tws-api/minimum_increment.html

Parameters
:
marketRuleId (int) – ID of market rule. The market rule IDs for a contract can be obtained via reqContractDetails() from ContractDetails.marketRuleIds, which contains a comma separated string of market rule IDs.

Return type
:
PriceIncrement

reqRealTimeBars(contract, barSize, whatToShow, useRTH, realTimeBarsOptions=[])[source]
Request realtime 5 second bars.

https://interactivebrokers.github.io/tws-api/realtime_bars.html

Parameters
:
contract (Contract) – Contract of interest.

barSize (int) – Must be 5.

whatToShow (str) – Specifies the source for constructing bars. Can be ‘TRADES’, ‘MIDPOINT’, ‘BID’ or ‘ASK’.

useRTH (bool) – If True then only show data from within Regular Trading Hours, if False then show all data.

realTimeBarsOptions (List[TagValue]) – Unknown.

Return type
:
RealTimeBarList

cancelRealTimeBars(bars)[source]
Cancel the realtime bars subscription.

Parameters
:
bars (RealTimeBarList) – The bar list that was obtained from reqRealTimeBars.

reqHistoricalData(contract, endDateTime, durationStr, barSizeSetting, whatToShow, useRTH, formatDate=1, keepUpToDate=False, chartOptions=[], timeout=60)[source]
Request historical bar data.

This method is blocking.

https://interactivebrokers.github.io/tws-api/historical_bars.html

Parameters
:
contract (Contract) – Contract of interest.

endDateTime (Union[datetime, date, str, None]) – Can be set to ‘’ to indicate the current time, or it can be given as a datetime.date or datetime.datetime, or it can be given as a string in ‘yyyyMMdd HH:mm:ss’ format. If no timezone is given then the TWS login timezone is used.

durationStr (str) – Time span of all the bars. Examples: ‘60 S’, ‘30 D’, ‘13 W’, ‘6 M’, ‘10 Y’.

barSizeSetting (str) – Time period of one bar. Must be one of: ‘1 secs’, ‘5 secs’, ‘10 secs’ 15 secs’, ‘30 secs’, ‘1 min’, ‘2 mins’, ‘3 mins’, ‘5 mins’, ‘10 mins’, ‘15 mins’, ‘20 mins’, ‘30 mins’, ‘1 hour’, ‘2 hours’, ‘3 hours’, ‘4 hours’, ‘8 hours’, ‘1 day’, ‘1 week’, ‘1 month’.

whatToShow (str) – Specifies the source for constructing bars. Must be one of: ‘TRADES’, ‘MIDPOINT’, ‘BID’, ‘ASK’, ‘BID_ASK’, ‘ADJUSTED_LAST’, ‘HISTORICAL_VOLATILITY’, ‘OPTION_IMPLIED_VOLATILITY’, ‘REBATE_RATE’, ‘FEE_RATE’, ‘YIELD_BID’, ‘YIELD_ASK’, ‘YIELD_BID_ASK’, ‘YIELD_LAST’. For ‘SCHEDULE’ use reqHistoricalSchedule().

useRTH (bool) – If True then only show data from within Regular Trading Hours, if False then show all data.

formatDate (int) – For an intraday request setting to 2 will cause the returned date fields to be timezone-aware datetime.datetime with UTC timezone, instead of local timezone as used by TWS.

keepUpToDate (bool) – If True then a realtime subscription is started to keep the bars updated; endDateTime must be set empty (‘’) then.

chartOptions (List[TagValue]) – Unknown.

timeout (float) – Timeout in seconds after which to cancel the request and return an empty bar series. Set to 0 to wait indefinitely.

Return type
:
BarDataList

cancelHistoricalData(bars)[source]
Cancel the update subscription for the historical bars.

Parameters
:
bars (BarDataList) – The bar list that was obtained from reqHistoricalData with a keepUpToDate subscription.

reqHistoricalSchedule(contract, numDays, endDateTime='', useRTH=True)[source]
Request historical schedule.

This method is blocking.

Parameters
:
contract (Contract) – Contract of interest.

numDays (int) – Number of days.

endDateTime (Union[datetime, date, str, None]) – Can be set to ‘’ to indicate the current time, or it can be given as a datetime.date or datetime.datetime, or it can be given as a string in ‘yyyyMMdd HH:mm:ss’ format. If no timezone is given then the TWS login timezone is used.

useRTH (bool) – If True then show schedule for Regular Trading Hours, if False then for extended hours.

Return type
:
HistoricalSchedule

reqHistoricalTicks(contract, startDateTime, endDateTime, numberOfTicks, whatToShow, useRth, ignoreSize=False, miscOptions=[])[source]
Request historical ticks. The time resolution of the ticks is one second.

This method is blocking.

https://interactivebrokers.github.io/tws-api/historical_time_and_sales.html

Parameters
:
contract (Contract) – Contract to query.

startDateTime (Union[str, date]) – Can be given as a datetime.date or datetime.datetime, or it can be given as a string in ‘yyyyMMdd HH:mm:ss’ format. If no timezone is given then the TWS login timezone is used.

endDateTime (Union[str, date]) – One of startDateTime or endDateTime can be given, the other must be blank.

numberOfTicks (int) – Number of ticks to request (1000 max). The actual result can contain a bit more to accommodate all ticks in the latest second.

whatToShow (str) – One of ‘Bid_Ask’, ‘Midpoint’ or ‘Trades’.

useRTH – If True then only show data from within Regular Trading Hours, if False then show all data.

ignoreSize (bool) – Ignore bid/ask ticks that only update the size.

miscOptions (List[TagValue]) – Unknown.

Return type
:
List

reqMarketDataType(marketDataType)[source]
Set the market data type used for reqMktData().

Parameters
:
marketDataType (int) –

One of:

1 = Live

2 = Frozen

3 = Delayed

4 = Delayed frozen

https://interactivebrokers.github.io/tws-api/market_data_type.html

reqHeadTimeStamp(contract, whatToShow, useRTH, formatDate=1)[source]
Get the datetime of earliest available historical data for the contract.

Parameters
:
contract (Contract) – Contract of interest.

useRTH (bool) – If True then only show data from within Regular Trading Hours, if False then show all data.

formatDate (int) – If set to 2 then the result is returned as a timezone-aware datetime.datetime with UTC timezone.

Return type
:
datetime

reqMktData(contract, genericTickList='', snapshot=False, regulatorySnapshot=False, mktDataOptions=[])[source]
Subscribe to tick data or request a snapshot. Returns the Ticker that holds the market data. The ticker will initially be empty and gradually (after a couple of seconds) be filled.

https://interactivebrokers.github.io/tws-api/md_request.html

Parameters
:
contract (Contract) – Contract of interest.

genericTickList (str) –

Comma separated IDs of desired generic ticks that will cause corresponding Ticker fields to be filled:

ID

Ticker fields

100

putVolume, callVolume (for options)

101

putOpenInterest, callOpenInterest (for options)

104

histVolatility (for options)

105

avOptionVolume (for options)

106

impliedVolatility (for options)

162

indexFuturePremium

165

low13week, high13week, low26week, high26week, low52week, high52week, avVolume

221

markPrice

225

auctionVolume, auctionPrice, auctionImbalance

233

last, lastSize, rtVolume, rtTime, vwap (Time & Sales)

236

shortableShares

258

fundamentalRatios (of type ib_async.objects.FundamentalRatios)

293

tradeCount

294

tradeRate

295

volumeRate

375

rtTradeVolume

411

rtHistVolatility

456

dividends (of type ib_async.objects.Dividends)

588

futuresOpenInterest

snapshot (bool) – If True then request a one-time snapshot, otherwise subscribe to a stream of realtime tick data.

regulatorySnapshot (bool) – Request NBBO snapshot (may incur a fee).

mktDataOptions (List[TagValue]) – Unknown

Return type
:
Ticker

cancelMktData(contract)[source]
Unsubscribe from realtime streaming tick data.

Parameters
:
contract (Contract) – The exact contract object that was used to subscribe with.

reqTickByTickData(contract, tickType, numberOfTicks=0, ignoreSize=False)[source]
Subscribe to tick-by-tick data and return the Ticker that holds the ticks in ticker.tickByTicks.

https://interactivebrokers.github.io/tws-api/tick_data.html

Parameters
:
contract (Contract) – Contract of interest.

tickType (str) – One of ‘Last’, ‘AllLast’, ‘BidAsk’ or ‘MidPoint’.

numberOfTicks (int) – Number of ticks or 0 for unlimited.

ignoreSize (bool) – Ignore bid/ask ticks that only update the size.

Return type
:
Ticker

cancelTickByTickData(contract, tickType)[source]
Unsubscribe from tick-by-tick data

Parameters
:
contract (Contract) – The exact contract object that was used to subscribe with.

reqSmartComponents(bboExchange)[source]
Obtain mapping from single letter codes to exchange names.

Note: The exchanges must be open when using this request, otherwise an empty list is returned.

Return type
:
List[SmartComponent]

reqMktDepthExchanges()[source]
Get those exchanges that have have multiple market makers (and have ticks returned with marketMaker info).

Return type
:
List[DepthMktDataDescription]

reqMktDepth(contract, numRows=5, isSmartDepth=False, mktDepthOptions=None)[source]
Subscribe to market depth data (a.k.a. DOM, L2 or order book).

https://interactivebrokers.github.io/tws-api/market_depth.html

Parameters
:
contract (Contract) – Contract of interest.

numRows (int) – Number of depth level on each side of the order book (5 max).

isSmartDepth (bool) – Consolidate the order book across exchanges.

mktDepthOptions – Unknown.

Return type
:
Ticker

Returns
:
The Ticker that holds the market depth in ticker.domBids and ticker.domAsks and the list of MktDepthData in ticker.domTicks.

cancelMktDepth(contract, isSmartDepth=False)[source]
Unsubscribe from market depth data.

Parameters
:
contract (Contract) – The exact contract object that was used to subscribe with.

reqHistogramData(contract, useRTH, period)[source]
Request histogram data.

This method is blocking.

https://interactivebrokers.github.io/tws-api/histograms.html

Parameters
:
contract (Contract) – Contract to query.

useRTH (bool) – If True then only show data from within Regular Trading Hours, if False then show all data.

period (str) – Period of which data is being requested, for example ‘3 days’.

Return type
:
List[HistogramData]

reqFundamentalData(contract, reportType, fundamentalDataOptions=[])[source]
Get fundamental data of a contract in XML format.

This method is blocking.

https://interactivebrokers.github.io/tws-api/fundamentals.html

Parameters
:
contract (Contract) – Contract to query.

reportType (str) –

‘ReportsFinSummary’: Financial summary

’ReportsOwnership’: Company’s ownership

’ReportSnapshot’: Company’s financial overview

’ReportsFinStatements’: Financial Statements

’RESC’: Analyst Estimates

’CalendarReport’: Company’s calendar

fundamentalDataOptions (List[TagValue]) – Unknown

Return type
:
str

reqScannerData(subscription, scannerSubscriptionOptions=[], scannerSubscriptionFilterOptions=[])[source]
Do a blocking market scan by starting a subscription and canceling it after the initial list of results are in.

This method is blocking.

https://interactivebrokers.github.io/tws-api/market_scanners.html

Parameters
:
subscription (ScannerSubscription) – Basic filters.

scannerSubscriptionOptions (List[TagValue]) – Unknown.

scannerSubscriptionFilterOptions (List[TagValue]) – Advanced generic filters.

Return type
:
ScanDataList

reqScannerSubscription(subscription, scannerSubscriptionOptions=[], scannerSubscriptionFilterOptions=[])[source]
Subscribe to market scan data.

https://interactivebrokers.github.io/tws-api/market_scanners.html

Parameters
:
subscription (ScannerSubscription) – What to scan for.

scannerSubscriptionOptions (List[TagValue]) – Unknown.

scannerSubscriptionFilterOptions (List[TagValue]) – Unknown.

Return type
:
ScanDataList

cancelScannerSubscription(dataList)[source]
Cancel market data subscription.

https://interactivebrokers.github.io/tws-api/market_scanners.html

Parameters
:
dataList (ScanDataList) – The scan data list that was obtained from reqScannerSubscription().

reqScannerParameters()[source]
Requests an XML list of scanner parameters.

This method is blocking.

Return type
:
str

calculateImpliedVolatility(contract, optionPrice, underPrice, implVolOptions=[])[source]
Calculate the volatility given the option price.

This method is blocking.

https://interactivebrokers.github.io/tws-api/option_computations.html

Parameters
:
contract (Contract) – Option contract.

optionPrice (float) – Option price to use in calculation.

underPrice (float) – Price of the underlier to use in calculation

implVolOptions (List[TagValue]) – Unknown

Return type
:
OptionComputation

calculateOptionPrice(contract, volatility, underPrice, optPrcOptions=[])[source]
Calculate the option price given the volatility.

This method is blocking.

https://interactivebrokers.github.io/tws-api/option_computations.html

Parameters
:
contract (Contract) – Option contract.

volatility (float) – Option volatility to use in calculation.

underPrice (float) – Price of the underlier to use in calculation

implVolOptions – Unknown

Return type
:
OptionComputation

reqSecDefOptParams(underlyingSymbol, futFopExchange, underlyingSecType, underlyingConId)[source]
Get the option chain.

This method is blocking.

https://interactivebrokers.github.io/tws-api/options.html

Parameters
:
underlyingSymbol (str) – Symbol of underlier contract.

futFopExchange (str) – Exchange (only for FuturesOption, otherwise leave blank).

underlyingSecType (str) – The type of the underlying security, like ‘STK’ or ‘FUT’.

underlyingConId (int) – conId of the underlying contract.

Return type
:
List[OptionChain]

exerciseOptions(contract, exerciseAction, exerciseQuantity, account, override)[source]
Exercise an options contract.

https://interactivebrokers.github.io/tws-api/options.html

Parameters
:
contract (Contract) – The option contract to be exercised.

exerciseAction (int) –

1 = exercise the option

2 = let the option lapse

exerciseQuantity (int) – Number of contracts to be exercised.

account (str) – Destination account.

override (int) –

0 = no override

1 = override the system’s natural action

reqNewsProviders()[source]
Get a list of news providers.

This method is blocking.

Return type
:
List[NewsProvider]

reqNewsArticle(providerCode, articleId, newsArticleOptions=[])[source]
Get the body of a news article.

This method is blocking.

https://interactivebrokers.github.io/tws-api/news.html

Parameters
:
providerCode (str) – Code indicating news provider, like ‘BZ’ or ‘FLY’.

articleId (str) – ID of the specific article.

newsArticleOptions (List[TagValue]) – Unknown.

Return type
:
NewsArticle

reqHistoricalNews(conId, providerCodes, startDateTime, endDateTime, totalResults, historicalNewsOptions=[])[source]
Get historical news headline.

https://interactivebrokers.github.io/tws-api/news.html

This method is blocking.

Parameters
:
conId (int) – Search news articles for contract with this conId.

providerCodes (str) – A ‘+’-separated list of provider codes, like ‘BZ+FLY’.

startDateTime (Union[str, date]) – The (exclusive) start of the date range. Can be given as a datetime.date or datetime.datetime, or it can be given as a string in ‘yyyyMMdd HH:mm:ss’ format. If no timezone is given then the TWS login timezone is used.

endDateTime (Union[str, date]) – The (inclusive) end of the date range. Can be given as a datetime.date or datetime.datetime, or it can be given as a string in ‘yyyyMMdd HH:mm:ss’ format. If no timezone is given then the TWS login timezone is used.

totalResults (int) – Maximum number of headlines to fetch (300 max).

historicalNewsOptions (List[TagValue]) – Unknown.

Return type
:
HistoricalNews

reqNewsBulletins(allMessages)[source]
Subscribe to IB news bulletins.

https://interactivebrokers.github.io/tws-api/news.html

Parameters
:
allMessages (bool) – If True then fetch all messages for the day.

cancelNewsBulletins()[source]
Cancel subscription to IB news bulletins.

requestFA(faDataType)[source]
Requests to change the FA configuration.

This method is blocking.

Parameters
:
faDataType (int) –

1 = Groups: Offer traders a way to create a group of accounts and apply a single allocation method to all accounts in the group.

2 = Profiles: Let you allocate shares on an account-by-account basis using a predefined calculation value.

3 = Account Aliases: Let you easily identify the accounts by meaningful names rather than account numbers.

replaceFA(faDataType, xml)[source]
Replaces Financial Advisor’s settings.

Parameters
:
faDataType (int) – See requestFA().

xml (str) – The XML-formatted configuration string.

reqWshMetaData()[source]
Request Wall Street Horizon metadata.

https://interactivebrokers.github.io/tws-api/fundamentals.html

cancelWshMetaData()[source]
Cancel WSH metadata.

reqWshEventData(data)[source]
Request Wall Street Horizon event data.

reqWshMetaData() must have been called first before using this method.

Parameters
:
data (WshEventData) – Filters for selecting the corporate event data.

https://interactivebrokers.github.io/tws-api/wshe_filters.html

cancelWshEventData()[source]
Cancel active WHS event data.

getWshMetaData()[source]
Blocking convenience method that returns the WSH metadata (that is the available filters and event types) as a JSON string.

Please note that a Wall Street Horizon subscription is required.

# Get the list of available filters and event types:
meta = ib.getWshMetaData()
print(meta)
Return type
:
str

getWshEventData(data)[source]
Blocking convenience method that returns the WSH event data as a JSON string. getWshMetaData() must have been called first before using this method.

Please note that a Wall Street Horizon subscription is required.

# For IBM (with conId=8314) query the:
#   - Earnings Dates (wshe_ed)
#   - Board of Directors meetings (wshe_bod)
data = WshEventData(
    filter = '''{
      "country": "All",
      "watchlist": ["8314"],
      "limit_region": 10,
      "limit": 10,
      "wshe_ed": "true",
      "wshe_bod": "true"
    }''')
events = ib.getWshEventData(data)
print(events)
Return type
:
str

reqUserInfo()[source]
Get the White Branding ID of the user.

Return type
:
str

asyncconnectAsync(host='127.0.0.1', port=7497, clientId=1, timeout=4, readonly=False, account='', raiseSyncErrors=False, fetchFields=<StartupFetch.POSITIONS|ORDERS_OPEN|ORDERS_COMPLETE|ACCOUNT_UPDATES|SUB_ACCOUNT_UPDATES|EXECUTIONS: 63>)[source]
asyncqualifyContractsAsync(*contracts)[source]
Return type
:
List[Contract]

asyncreqTickersAsync(*contracts, regulatorySnapshot=False)[source]
Return type
:
List[Ticker]

whatIfOrderAsync(contract, order)[source]
Return type
:
Awaitable[OrderState]

reqCurrentTimeAsync()[source]
Return type
:
Awaitable[datetime]

reqAccountUpdatesAsync(account)[source]
Return type
:
Awaitable[None]

reqAccountUpdatesMultiAsync(account, modelCode='')[source]
Return type
:
Awaitable[None]

asyncaccountSummaryAsync(account='')[source]
Return type
:
List[AccountValue]

reqAccountSummaryAsync()[source]
Return type
:
Awaitable[None]

reqOpenOrdersAsync()[source]
Return type
:
Awaitable[List[Trade]]

reqAllOpenOrdersAsync()[source]
Return type
:
Awaitable[List[Trade]]

reqCompletedOrdersAsync(apiOnly)[source]
Return type
:
Awaitable[List[Trade]]

reqExecutionsAsync(execFilter=None)[source]
Return type
:
Awaitable[List[Fill]]

reqPositionsAsync()[source]
Return type
:
Awaitable[List[Position]]

reqContractDetailsAsync(contract)[source]
Return type
:
Awaitable[List[ContractDetails]]

asyncreqMatchingSymbolsAsync(pattern)[source]
Return type
:
Optional[List[ContractDescription]]

asyncreqMarketRuleAsync(marketRuleId)[source]
Return type
:
Optional[List[PriceIncrement]]

asyncreqHistoricalDataAsync(contract, endDateTime, durationStr, barSizeSetting, whatToShow, useRTH, formatDate=1, keepUpToDate=False, chartOptions=[], timeout=60)[source]
Return type
:
BarDataList

reqHistoricalScheduleAsync(contract, numDays, endDateTime='', useRTH=True)[source]
Return type
:
Awaitable[HistoricalSchedule]

reqHistoricalTicksAsync(contract, startDateTime, endDateTime, numberOfTicks, whatToShow, useRth, ignoreSize=False, miscOptions=[])[source]
Return type
:
Awaitable[List]

asyncreqHeadTimeStampAsync(contract, whatToShow, useRTH, formatDate)[source]
Return type
:
datetime

reqSmartComponentsAsync(bboExchange)[source]
reqMktDepthExchangesAsync()[source]
Return type
:
Awaitable[List[DepthMktDataDescription]]

reqHistogramDataAsync(contract, useRTH, period)[source]
Return type
:
Awaitable[List[HistogramData]]

reqFundamentalDataAsync(contract, reportType, fundamentalDataOptions=[])[source]
Return type
:
Awaitable[str]

asyncreqScannerDataAsync(subscription, scannerSubscriptionOptions=[], scannerSubscriptionFilterOptions=[])[source]
Return type
:
ScanDataList

reqScannerParametersAsync()[source]
Return type
:
Awaitable[str]

asynccalculateImpliedVolatilityAsync(contract, optionPrice, underPrice, implVolOptions=[])[source]
Return type
:
Optional[OptionComputation]

asynccalculateOptionPriceAsync(contract, volatility, underPrice, optPrcOptions=[])[source]
Return type
:
Optional[OptionComputation]

reqSecDefOptParamsAsync(underlyingSymbol, futFopExchange, underlyingSecType, underlyingConId)[source]
Return type
:
Awaitable[List[OptionChain]]

reqNewsProvidersAsync()[source]
Return type
:
Awaitable[List[NewsProvider]]

reqNewsArticleAsync(providerCode, articleId, newsArticleOptions=[])[source]
Return type
:
Awaitable[NewsArticle]

asyncreqHistoricalNewsAsync(conId, providerCodes, startDateTime, endDateTime, totalResults, historicalNewsOptions=[])[source]
Return type
:
Optional[HistoricalNews]

asyncrequestFAAsync(faDataType)[source]
asyncgetWshMetaDataAsync()[source]
Return type
:
str

asyncgetWshEventDataAsync(data)[source]
Return type
:
str

reqUserInfoAsync()[source]
Client
Socket client for communicating with Interactive Brokers.

classib_async.client.Client(wrapper)[source]
Replacement for ibapi.client.EClient that uses asyncio.

The client is fully asynchronous and has its own event-driven networking code that replaces the networking code of the standard EClient. It also replaces the infinite loop of EClient.run() with the asyncio event loop. It can be used as a drop-in replacement for the standard EClient as provided by IBAPI.

Compared to the standard EClient this client has the following additional features:

client.connect() will block until the client is ready to serve requests; It is not necessary to wait for nextValidId to start requests as the client has already done that. The reqId is directly available with getReqId().

client.connectAsync() is a coroutine for connecting asynchronously.

When blocking, client.connect() can be made to time out with the timeout parameter (default 2 seconds).

Optional wrapper.priceSizeTick(reqId, tickType, price, size) that combines price and size instead of the two wrapper methods priceTick and sizeTick.

Automatic request throttling.

Optional wrapper.tcpDataArrived() method; If the wrapper has this method it is invoked directly after a network packet has arrived. A possible use is to timestamp all data in the packet with the exact same time.

Optional wrapper.tcpDataProcessed() method; If the wrapper has this method it is invoked after the network packet’s data has been handled. A possible use is to write or evaluate the newly arrived data in one batch instead of item by item.

Parameters
:
MaxRequests (int) – Throttle the number of requests to MaxRequests per RequestsInterval seconds. Set to 0 to disable throttling.

RequestsInterval (float) – Time interval (in seconds) for request throttling.

MinClientVersion (int) – Client protocol version.

MaxClientVersion (int) – Client protocol version.

Events:
apiStart ()

apiEnd ()

apiError (errorMsg: str)

throttleStart ()

throttleEnd ()

events= ('apiStart', 'apiEnd', 'apiError', 'throttleStart', 'throttleEnd')
MaxRequests= 45
RequestsInterval= 1
MinClientVersion= 157
MaxClientVersion= 178
DISCONNECTED= 0
CONNECTING= 1
CONNECTED= 2
reset()[source]
serverVersion()[source]
Return type
:
int

run()[source]
isConnected()[source]
isReady()[source]
Is the API connection up and running?

Return type
:
bool

connectionStats()[source]
Get statistics about the connection.

Return type
:
ConnectionStats

getReqId()[source]
Get new request ID.

Return type
:
int

updateReqId(minReqId)[source]
Update the next reqId to be at least minReqId.

getAccounts()[source]
Get the list of account names that are under management.

Return type
:
List[str]

setConnectOptions(connectOptions)[source]
Set additional connect options.

Parameters
:
connectOptions (str) – Use “+PACEAPI” to use request-pacing built into TWS/gateway 974+ (obsolete).

connect(host, port, clientId, timeout=2.0)[source]
Connect to a running TWS or IB gateway application.

Parameters
:
host (str) – Host name or IP address.

port (int) – Port number.

clientId (int) – ID number to use for this client; must be unique per connection.

timeout (Optional[float]) – If establishing the connection takes longer than timeout seconds then the asyncio.TimeoutError exception is raised. Set to 0 to disable timeout.

asyncconnectAsync(host, port, clientId, timeout=2.0)[source]
disconnect()[source]
Disconnect from IB connection.

send(*fields, makeEmpty=True)[source]
Serialize and send the given fields using the IB socket protocol.

if ‘makeEmpty’ is True (default), then the IBKR values representing “no value” become the empty string.

sendMsg(msg)[source]
reqMktData(reqId, contract, genericTickList, snapshot, regulatorySnapshot, mktDataOptions)[source]
cancelMktData(reqId)[source]
placeOrder(orderId, contract, order)[source]
cancelOrder(orderId, manualCancelOrderTime='')[source]
reqOpenOrders()[source]
reqAccountUpdates(subscribe, acctCode)[source]
reqExecutions(reqId, execFilter)[source]
reqIds(numIds)[source]
reqContractDetails(reqId, contract)[source]
reqMktDepth(reqId, contract, numRows, isSmartDepth, mktDepthOptions)[source]
cancelMktDepth(reqId, isSmartDepth)[source]
reqNewsBulletins(allMsgs)[source]
cancelNewsBulletins()[source]
setServerLogLevel(logLevel)[source]
reqAutoOpenOrders(bAutoBind)[source]
reqAllOpenOrders()[source]
reqManagedAccts()[source]
requestFA(faData)[source]
replaceFA(reqId, faData, cxml)[source]
reqHistoricalData(reqId, contract, endDateTime, durationStr, barSizeSetting, whatToShow, useRTH, formatDate, keepUpToDate, chartOptions)[source]
exerciseOptions(reqId, contract, exerciseAction, exerciseQuantity, account, override)[source]
reqScannerSubscription(reqId, subscription, scannerSubscriptionOptions, scannerSubscriptionFilterOptions)[source]
cancelScannerSubscription(reqId)[source]
reqScannerParameters()[source]
cancelHistoricalData(reqId)[source]
reqCurrentTime()[source]
reqRealTimeBars(reqId, contract, barSize, whatToShow, useRTH, realTimeBarsOptions)[source]
cancelRealTimeBars(reqId)[source]
reqFundamentalData(reqId, contract, reportType, fundamentalDataOptions)[source]
cancelFundamentalData(reqId)[source]
calculateImpliedVolatility(reqId, contract, optionPrice, underPrice, implVolOptions)[source]
calculateOptionPrice(reqId, contract, volatility, underPrice, optPrcOptions)[source]
cancelCalculateImpliedVolatility(reqId)[source]
cancelCalculateOptionPrice(reqId)[source]
reqGlobalCancel()[source]
reqMarketDataType(marketDataType)[source]
reqPositions()[source]
reqAccountSummary(reqId, groupName, tags)[source]
cancelAccountSummary(reqId)[source]
cancelPositions()[source]
verifyRequest(apiName, apiVersion)[source]
verifyMessage(apiData)[source]
queryDisplayGroups(reqId)[source]
subscribeToGroupEvents(reqId, groupId)[source]
updateDisplayGroup(reqId, contractInfo)[source]
unsubscribeFromGroupEvents(reqId)[source]
startApi()[source]
verifyAndAuthRequest(apiName, apiVersion, opaqueIsvKey)[source]
verifyAndAuthMessage(apiData, xyzResponse)[source]
reqPositionsMulti(reqId, account, modelCode)[source]
cancelPositionsMulti(reqId)[source]
reqAccountUpdatesMulti(reqId, account, modelCode, ledgerAndNLV)[source]
cancelAccountUpdatesMulti(reqId)[source]
reqSecDefOptParams(reqId, underlyingSymbol, futFopExchange, underlyingSecType, underlyingConId)[source]
reqSoftDollarTiers(reqId)[source]
reqFamilyCodes()[source]
reqMatchingSymbols(reqId, pattern)[source]
reqMktDepthExchanges()[source]
reqSmartComponents(reqId, bboExchange)[source]
reqNewsArticle(reqId, providerCode, articleId, newsArticleOptions)[source]
reqNewsProviders()[source]
reqHistoricalNews(reqId, conId, providerCodes, startDateTime, endDateTime, totalResults, historicalNewsOptions)[source]
reqHeadTimeStamp(reqId, contract, whatToShow, useRTH, formatDate)[source]
reqHistogramData(tickerId, contract, useRTH, timePeriod)[source]
cancelHistogramData(tickerId)[source]
cancelHeadTimeStamp(reqId)[source]
reqMarketRule(marketRuleId)[source]
reqPnL(reqId, account, modelCode)[source]
cancelPnL(reqId)[source]
reqPnLSingle(reqId, account, modelCode, conid)[source]
cancelPnLSingle(reqId)[source]
reqHistoricalTicks(reqId, contract, startDateTime, endDateTime, numberOfTicks, whatToShow, useRth, ignoreSize, miscOptions)[source]
reqTickByTickData(reqId, contract, tickType, numberOfTicks, ignoreSize)[source]
cancelTickByTickData(reqId)[source]
reqCompletedOrders(apiOnly)[source]
reqWshMetaData(reqId)[source]
cancelWshMetaData(reqId)[source]
reqWshEventData(reqId, data)[source]
cancelWshEventData(reqId)[source]
reqUserInfo(reqId)[source]
Order
Order types used by Interactive Brokers.

classib_async.order.Order(orderId=0, clientId=0, permId=0, action='', totalQuantity=0.0, orderType='', lmtPrice=1.7976931348623157e+308, auxPrice=1.7976931348623157e+308, tif='', activeStartTime='', activeStopTime='', ocaGroup='', ocaType=0, orderRef='', transmit=True, parentId=0, blockOrder=False, sweepToFill=False, displaySize=0, triggerMethod=0, outsideRth=False, hidden=False, goodAfterTime='', goodTillDate='', rule80A='', allOrNone=False, minQty=2147483647, percentOffset=1.7976931348623157e+308, overridePercentageConstraints=False, trailStopPrice=1.7976931348623157e+308, trailingPercent=1.7976931348623157e+308, faGroup='', faProfile='', faMethod='', faPercentage='', designatedLocation='', openClose='O', origin=0, shortSaleSlot=0, exemptCode=-1, discretionaryAmt=0.0, eTradeOnly=False, firmQuoteOnly=False, nbboPriceCap=1.7976931348623157e+308, optOutSmartRouting=False, auctionStrategy=0, startingPrice=1.7976931348623157e+308, stockRefPrice=1.7976931348623157e+308, delta=1.7976931348623157e+308, stockRangeLower=1.7976931348623157e+308, stockRangeUpper=1.7976931348623157e+308, randomizePrice=False, randomizeSize=False, volatility=1.7976931348623157e+308, volatilityType=2147483647, deltaNeutralOrderType='', deltaNeutralAuxPrice=1.7976931348623157e+308, deltaNeutralConId=0, deltaNeutralSettlingFirm='', deltaNeutralClearingAccount='', deltaNeutralClearingIntent='', deltaNeutralOpenClose='', deltaNeutralShortSale=False, deltaNeutralShortSaleSlot=0, deltaNeutralDesignatedLocation='', continuousUpdate=False, referencePriceType=2147483647, basisPoints=1.7976931348623157e+308, basisPointsType=2147483647, scaleInitLevelSize=2147483647, scaleSubsLevelSize=2147483647, scalePriceIncrement=1.7976931348623157e+308, scalePriceAdjustValue=1.7976931348623157e+308, scalePriceAdjustInterval=2147483647, scaleProfitOffset=1.7976931348623157e+308, scaleAutoReset=False, scaleInitPosition=2147483647, scaleInitFillQty=2147483647, scaleRandomPercent=False, scaleTable='', hedgeType='', hedgeParam='', account='', settlingFirm='', clearingAccount='', clearingIntent='', algoStrategy='', algoParams=<factory>, smartComboRoutingParams=<factory>, algoId='', whatIf=False, notHeld=False, solicited=False, modelCode='', orderComboLegs=<factory>, orderMiscOptions=<factory>, referenceContractId=0, peggedChangeAmount=0.0, isPeggedChangeAmountDecrease=False, referenceChangeAmount=0.0, referenceExchangeId='', adjustedOrderType='', triggerPrice=1.7976931348623157e+308, adjustedStopPrice=1.7976931348623157e+308, adjustedStopLimitPrice=1.7976931348623157e+308, adjustedTrailingAmount=1.7976931348623157e+308, adjustableTrailingUnit=0, lmtPriceOffset=1.7976931348623157e+308, conditions=<factory>, conditionsCancelOrder=False, conditionsIgnoreRth=False, extOperator='', softDollarTier=<factory>, cashQty=1.7976931348623157e+308, mifid2DecisionMaker='', mifid2DecisionAlgo='', mifid2ExecutionTrader='', mifid2ExecutionAlgo='', dontUseAutoPriceForHedge=False, isOmsContainer=False, discretionaryUpToLimitPrice=False, autoCancelDate='', filledQuantity=1.7976931348623157e+308, refFuturesConId=0, autoCancelParent=False, shareholder='', imbalanceOnly=False, routeMarketableToBbo=False, parentPermId=0, usePriceMgmtAlgo=False, duration=2147483647, postToAts=2147483647, advancedErrorOverride='', manualOrderTime='', minTradeQty=2147483647, minCompeteSize=2147483647, competeAgainstBestOffset=1.7976931348623157e+308, midOffsetAtWhole=1.7976931348623157e+308, midOffsetAtHalf=1.7976931348623157e+308)[source]
Order for trading contracts.

https://interactivebrokers.github.io/tws-api/available_orders.html

orderId: int= 0
clientId: int= 0
permId: int= 0
action: str= ''
totalQuantity: float= 0.0
orderType: str= ''
lmtPrice: float= 1.7976931348623157e+308
auxPrice: float= 1.7976931348623157e+308
tif: str= ''
activeStartTime: str= ''
activeStopTime: str= ''
ocaGroup: str= ''
ocaType: int= 0
orderRef: str= ''
transmit: bool= True
parentId: int= 0
blockOrder: bool= False
sweepToFill: bool= False
displaySize: int= 0
triggerMethod: int= 0
outsideRth: bool= False
hidden: bool= False
goodAfterTime: str= ''
goodTillDate: str= ''
rule80A: str= ''
allOrNone: bool= False
minQty: int= 2147483647
percentOffset: float= 1.7976931348623157e+308
overridePercentageConstraints: bool= False
trailStopPrice: float= 1.7976931348623157e+308
trailingPercent: float= 1.7976931348623157e+308
faGroup: str= ''
faProfile: str= ''
faMethod: str= ''
faPercentage: str= ''
designatedLocation: str= ''
openClose: str= 'O'
origin: int= 0
shortSaleSlot: int= 0
exemptCode: int= -1
discretionaryAmt: float= 0.0
eTradeOnly: bool= False
firmQuoteOnly: bool= False
nbboPriceCap: float= 1.7976931348623157e+308
optOutSmartRouting: bool= False
auctionStrategy: int= 0
startingPrice: float= 1.7976931348623157e+308
stockRefPrice: float= 1.7976931348623157e+308
delta: float= 1.7976931348623157e+308
stockRangeLower: float= 1.7976931348623157e+308
stockRangeUpper: float= 1.7976931348623157e+308
randomizePrice: bool= False
randomizeSize: bool= False
volatility: float= 1.7976931348623157e+308
volatilityType: int= 2147483647
deltaNeutralOrderType: str= ''
deltaNeutralAuxPrice: float= 1.7976931348623157e+308
deltaNeutralConId: int= 0
deltaNeutralSettlingFirm: str= ''
deltaNeutralClearingAccount: str= ''
deltaNeutralClearingIntent: str= ''
deltaNeutralOpenClose: str= ''
deltaNeutralShortSale: bool= False
deltaNeutralShortSaleSlot: int= 0
deltaNeutralDesignatedLocation: str= ''
continuousUpdate: bool= False
referencePriceType: int= 2147483647
basisPoints: float= 1.7976931348623157e+308
basisPointsType: int= 2147483647
scaleInitLevelSize: int= 2147483647
scaleSubsLevelSize: int= 2147483647
scalePriceIncrement: float= 1.7976931348623157e+308
scalePriceAdjustValue: float= 1.7976931348623157e+308
scalePriceAdjustInterval: int= 2147483647
scaleProfitOffset: float= 1.7976931348623157e+308
scaleAutoReset: bool= False
scaleInitPosition: int= 2147483647
scaleInitFillQty: int= 2147483647
scaleRandomPercent: bool= False
scaleTable: str= ''
hedgeType: str= ''
hedgeParam: str= ''
account: str= ''
settlingFirm: str= ''
clearingAccount: str= ''
clearingIntent: str= ''
algoStrategy: str= ''
algoParams: List[TagValue]
smartComboRoutingParams: List[TagValue]
algoId: str= ''
whatIf: bool= False
notHeld: bool= False
solicited: bool= False
modelCode: str= ''
orderComboLegs: List[OrderComboLeg]
orderMiscOptions: List[TagValue]
referenceContractId: int= 0
peggedChangeAmount: float= 0.0
isPeggedChangeAmountDecrease: bool= False
referenceChangeAmount: float= 0.0
referenceExchangeId: str= ''
adjustedOrderType: str= ''
triggerPrice: float= 1.7976931348623157e+308
adjustedStopPrice: float= 1.7976931348623157e+308
adjustedStopLimitPrice: float= 1.7976931348623157e+308
adjustedTrailingAmount: float= 1.7976931348623157e+308
adjustableTrailingUnit: int= 0
lmtPriceOffset: float= 1.7976931348623157e+308
conditions: List[OrderCondition]
conditionsCancelOrder: bool= False
conditionsIgnoreRth: bool= False
extOperator: str= ''
softDollarTier: SoftDollarTier
cashQty: float= 1.7976931348623157e+308
mifid2DecisionMaker: str= ''
mifid2DecisionAlgo: str= ''
mifid2ExecutionTrader: str= ''
mifid2ExecutionAlgo: str= ''
dontUseAutoPriceForHedge: bool= False
isOmsContainer: bool= False
discretionaryUpToLimitPrice: bool= False
autoCancelDate: str= ''
filledQuantity: float= 1.7976931348623157e+308
refFuturesConId: int= 0
autoCancelParent: bool= False
shareholder: str= ''
imbalanceOnly: bool= False
routeMarketableToBbo: bool= False
parentPermId: int= 0
usePriceMgmtAlgo: bool= False
duration: int= 2147483647
postToAts: int= 2147483647
advancedErrorOverride: str= ''
manualOrderTime: str= ''
minTradeQty: int= 2147483647
minCompeteSize: int= 2147483647
competeAgainstBestOffset: float= 1.7976931348623157e+308
midOffsetAtWhole: float= 1.7976931348623157e+308
midOffsetAtHalf: float= 1.7976931348623157e+308
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.order.LimitOrder(action, totalQuantity, lmtPrice, **kwargs)[source]
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.order.MarketOrder(action, totalQuantity, **kwargs)[source]
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.order.StopOrder(action, totalQuantity, stopPrice, **kwargs)[source]
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.order.StopLimitOrder(action, totalQuantity, lmtPrice, stopPrice, **kwargs)[source]
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.order.OrderStatus(orderId=0, status='', filled=0.0, remaining=0.0, avgFillPrice=0.0, permId=0, parentId=0, lastFillPrice=0.0, clientId=0, whyHeld='', mktCapPrice=0.0)[source]
orderId: int= 0
status: str= ''
filled: float= 0.0
remaining: float= 0.0
avgFillPrice: float= 0.0
permId: int= 0
parentId: int= 0
lastFillPrice: float= 0.0
clientId: int= 0
whyHeld: str= ''
mktCapPrice: float= 0.0
PendingSubmit: ClassVar[str]= 'PendingSubmit'
PendingCancel: ClassVar[str]= 'PendingCancel'
PreSubmitted: ClassVar[str]= 'PreSubmitted'
Submitted: ClassVar[str]= 'Submitted'
ApiPending: ClassVar[str]= 'ApiPending'
ApiCancelled: ClassVar[str]= 'ApiCancelled'
Cancelled: ClassVar[str]= 'Cancelled'
Filled: ClassVar[str]= 'Filled'
Inactive: ClassVar[str]= 'Inactive'
DoneStates: ClassVar[FrozenSet[str]]= frozenset({'ApiCancelled', 'Cancelled', 'Filled'})
ActiveStates: ClassVar[FrozenSet[str]]= frozenset({'ApiPending', 'PendingSubmit', 'PreSubmitted', 'Submitted'})
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.order.OrderState(status='', initMarginBefore='', maintMarginBefore='', equityWithLoanBefore='', initMarginChange='', maintMarginChange='', equityWithLoanChange='', initMarginAfter='', maintMarginAfter='', equityWithLoanAfter='', commission=1.7976931348623157e+308, minCommission=1.7976931348623157e+308, maxCommission=1.7976931348623157e+308, commissionCurrency='', warningText='', completedTime='', completedStatus='')[source]
status: str= ''
initMarginBefore: str= ''
maintMarginBefore: str= ''
equityWithLoanBefore: str= ''
initMarginChange: str= ''
maintMarginChange: str= ''
equityWithLoanChange: str= ''
initMarginAfter: str= ''
maintMarginAfter: str= ''
equityWithLoanAfter: str= ''
commission: float= 1.7976931348623157e+308
minCommission: float= 1.7976931348623157e+308
maxCommission: float= 1.7976931348623157e+308
commissionCurrency: str= ''
warningText: str= ''
completedTime: str= ''
completedStatus: str= ''
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.order.OrderComboLeg(price=1.7976931348623157e+308)[source]
price: float= 1.7976931348623157e+308
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.order.Trade(contract=<factory>, order=<factory>, orderStatus=<factory>, fills=<factory>, log=<factory>, advancedError='')[source]
Trade keeps track of an order, its status and all its fills.

Events:
statusEvent (trade: Trade)

modifyEvent (trade: Trade)

fillEvent (trade: Trade, fill: Fill)

commissionReportEvent (trade: Trade, fill: Fill, commissionReport: CommissionReport)

filledEvent (trade: Trade)

cancelEvent (trade: Trade)

cancelledEvent (trade: Trade)

contract: Contract
order: Order
orderStatus: OrderStatus
fills: List[Fill]
log: List[TradeLogEntry]
advancedError: str= ''
events: ClassVar= ('statusEvent', 'modifyEvent', 'fillEvent', 'commissionReportEvent', 'filledEvent', 'cancelEvent', 'cancelledEvent')
isActive()[source]
True if eligible for execution, false otherwise.

Return type
:
bool

isDone()[source]
True if completely filled or cancelled, false otherwise.

Return type
:
bool

filled()[source]
Number of shares filled.

Return type
:
float

remaining()[source]
Number of shares remaining to be filled.

Return type
:
float

dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.order.BracketOrder(parent, takeProfit, stopLoss)[source]
Create new instance of BracketOrder(parent, takeProfit, stopLoss)

parent: Order
takeProfit: Order
stopLoss: Order
classib_async.order.OrderCondition[source]
staticcreateClass(condType)[source]
And()[source]
Or()[source]
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.order.PriceCondition(condType=1, conjunction='a', isMore=True, price=0.0, conId=0, exch='', triggerMethod=0)[source]
condType: int= 1
conjunction: str= 'a'
isMore: bool= True
price: float= 0.0
conId: int= 0
exch: str= ''
triggerMethod: int= 0
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.order.TimeCondition(condType=3, conjunction='a', isMore=True, time='')[source]
condType: int= 3
conjunction: str= 'a'
isMore: bool= True
time: str= ''
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.order.MarginCondition(condType=4, conjunction='a', isMore=True, percent=0)[source]
condType: int= 4
conjunction: str= 'a'
isMore: bool= True
percent: int= 0
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.order.ExecutionCondition(condType=5, conjunction='a', secType='', exch='', symbol='')[source]
condType: int= 5
conjunction: str= 'a'
secType: str= ''
exch: str= ''
symbol: str= ''
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.order.VolumeCondition(condType=6, conjunction='a', isMore=True, volume=0, conId=0, exch='')[source]
condType: int= 6
conjunction: str= 'a'
isMore: bool= True
volume: int= 0
conId: int= 0
exch: str= ''
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.order.PercentChangeCondition(condType=7, conjunction='a', isMore=True, changePercent=0.0, conId=0, exch='')[source]
condType: int= 7
conjunction: str= 'a'
isMore: bool= True
changePercent: float= 0.0
conId: int= 0
exch: str= ''
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

Contract
Financial instrument types used by Interactive Brokers.

classib_async.contract.Contract(secType='', conId=0, symbol='', lastTradeDateOrContractMonth='', strike=0.0, right='', multiplier='', exchange='', primaryExchange='', currency='', localSymbol='', tradingClass='', includeExpired=False, secIdType='', secId='', description='', issuerId='', comboLegsDescrip='', comboLegs=<factory>, deltaNeutralContract=None)[source]
Contract(**kwargs) can create any contract using keyword arguments. To simplify working with contracts, there are also more specialized contracts that take optional positional arguments. Some examples:

Contract(conId=270639)
Stock('AMD', 'SMART', 'USD')
Stock('INTC', 'SMART', 'USD', primaryExchange='NASDAQ')
Forex('EURUSD')
CFD('IBUS30')
Future('ES', '20180921', 'GLOBEX')
Option('SPY', '20170721', 240, 'C', 'SMART')
Bond(secIdType='ISIN', secId='US03076KAA60')
Crypto('BTC', 'PAXOS', 'USD')
Parameters
:
conId (int) – The unique IB contract identifier.

symbol (str) – The contract (or its underlying) symbol.

secType (str) –

The security type:

’STK’ = Stock (or ETF)

’OPT’ = Option

’FUT’ = Future

’IND’ = Index

’FOP’ = Futures option

’CASH’ = Forex pair

’CFD’ = CFD

’BAG’ = Combo

’WAR’ = Warrant

’BOND’ = Bond

’CMDTY’ = Commodity

’NEWS’ = News

’FUND’ = Mutual fund

’CRYPTO’ = Crypto currency

’EVENT’ = Bet on an event

lastTradeDateOrContractMonth (str) – The contract’s last trading day or contract month (for Options and Futures). Strings with format YYYYMM will be interpreted as the Contract Month whereas YYYYMMDD will be interpreted as Last Trading Day.

strike (float) – The option’s strike price.

right (str) – Put or Call. Valid values are ‘P’, ‘PUT’, ‘C’, ‘CALL’, or ‘’ for non-options.

multiplier (str) – The instrument’s multiplier (i.e. options, futures).

exchange (str) – The destination exchange.

currency (str) – The underlying’s currency.

localSymbol (str) – The contract’s symbol within its primary exchange. For options, this will be the OCC symbol.

primaryExchange (str) – The contract’s primary exchange. For smart routed contracts, used to define contract in case of ambiguity. Should be defined as native exchange of contract, e.g. ISLAND for MSFT. For exchanges which contain a period in name, will only be part of exchange name prior to period, i.e. ENEXT for ENEXT.BE.

tradingClass (str) – The trading class name for this contract. Available in TWS contract description window as well. For example, GBL Dec ‘13 future’s trading class is “FGBL”.

includeExpired (bool) – If set to true, contract details requests and historical data queries can be performed pertaining to expired futures contracts. Expired options or other instrument types are not available.

secIdType (str) –

Security identifier type. Examples for Apple:

secIdType=’ISIN’, secId=’US0378331005’

secIdType=’CUSIP’, secId=’037833100’

secId (str) – Security identifier.

comboLegsDescription (str) – Description of the combo legs.

comboLegs (List[ComboLeg]) – The legs of a combined contract definition.

deltaNeutralContract (DeltaNeutralContract) – Delta and underlying price for Delta-Neutral combo orders.

secType: str= ''
conId: int= 0
symbol: str= ''
lastTradeDateOrContractMonth: str= ''
strike: float= 0.0
right: str= ''
multiplier: str= ''
exchange: str= ''
primaryExchange: str= ''
currency: str= ''
localSymbol: str= ''
tradingClass: str= ''
includeExpired: bool= False
secIdType: str= ''
secId: str= ''
description: str= ''
issuerId: str= ''
comboLegsDescrip: str= ''
comboLegs: List[ComboLeg]
deltaNeutralContract: Optional[DeltaNeutralContract]= None
staticcreate(**kwargs)[source]
Create and a return a specialized contract based on the given secType, or a general Contract if secType is not given.

Return type
:
Contract

isHashable()[source]
See if this contract can be hashed by conId.

Note: Bag contracts always get conId=28812380, so they’re not hashable.

Return type
:
bool

dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.contract.Stock(symbol='', exchange='', currency='', **kwargs)[source]
Stock contract.

Parameters
:
symbol (str) – Symbol name.

exchange (str) – Destination exchange.

currency (str) – Underlying currency.

dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.contract.Option(symbol='', lastTradeDateOrContractMonth='', strike=0.0, right='', exchange='', multiplier='', currency='', **kwargs)[source]
Option contract.

Parameters
:
symbol (str) – Symbol name.

lastTradeDateOrContractMonth (str) –

The option’s last trading day or contract month.

YYYYMM format: To specify last month

YYYYMMDD format: To specify last trading day

strike (float) – The option’s strike price.

right (str) – Put or call option. Valid values are ‘P’, ‘PUT’, ‘C’ or ‘CALL’.

exchange (str) – Destination exchange.

multiplier (str) – The contract multiplier.

currency (str) – Underlying currency.

dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.contract.Future(symbol='', lastTradeDateOrContractMonth='', exchange='', localSymbol='', multiplier='', currency='', **kwargs)[source]
Future contract.

Parameters
:
symbol (str) – Symbol name.

lastTradeDateOrContractMonth (str) –

The option’s last trading day or contract month.

YYYYMM format: To specify last month

YYYYMMDD format: To specify last trading day

exchange (str) – Destination exchange.

localSymbol (str) – The contract’s symbol within its primary exchange.

multiplier (str) – The contract multiplier.

currency (str) – Underlying currency.

dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.contract.ContFuture(symbol='', exchange='', localSymbol='', multiplier='', currency='', **kwargs)[source]
Continuous future contract.

Parameters
:
symbol (str) – Symbol name.

exchange (str) – Destination exchange.

localSymbol (str) – The contract’s symbol within its primary exchange.

multiplier (str) – The contract multiplier.

currency (str) – Underlying currency.

dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.contract.Forex(pair='', exchange='IDEALPRO', symbol='', currency='', **kwargs)[source]
Foreign exchange currency pair.

Parameters
:
pair (str) – Shortcut for specifying symbol and currency, like ‘EURUSD’.

exchange (str) – Destination exchange.

symbol (str) – Base currency.

currency (str) – Quote currency.

pair()[source]
Short name of pair.

Return type
:
str

dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.contract.Index(symbol='', exchange='', currency='', **kwargs)[source]
Index.

Parameters
:
symbol (str) – Symbol name.

exchange (str) – Destination exchange.

currency (str) – Underlying currency.

dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.contract.CFD(symbol='', exchange='', currency='', **kwargs)[source]
Contract For Difference.

Parameters
:
symbol (str) – Symbol name.

exchange (str) – Destination exchange.

currency (str) – Underlying currency.

dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.contract.Commodity(symbol='', exchange='', currency='', **kwargs)[source]
Commodity.

Parameters
:
symbol (str) – Symbol name.

exchange (str) – Destination exchange.

currency (str) – Underlying currency.

dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.contract.Bond(**kwargs)[source]
Bond.

dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.contract.FuturesOption(symbol='', lastTradeDateOrContractMonth='', strike=0.0, right='', exchange='', multiplier='', currency='', **kwargs)[source]
Option on a futures contract.

Parameters
:
symbol (str) – Symbol name.

lastTradeDateOrContractMonth (str) –

The option’s last trading day or contract month.

YYYYMM format: To specify last month

YYYYMMDD format: To specify last trading day

strike (float) – The option’s strike price.

right (str) – Put or call option. Valid values are ‘P’, ‘PUT’, ‘C’ or ‘CALL’.

exchange (str) – Destination exchange.

multiplier (str) – The contract multiplier.

currency (str) – Underlying currency.

dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.contract.MutualFund(**kwargs)[source]
Mutual fund.

dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.contract.Warrant(**kwargs)[source]
Warrant option.

dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.contract.Bag(**kwargs)[source]
Bag contract.

dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.contract.Crypto(symbol='', exchange='', currency='', **kwargs)[source]
Crypto currency contract.

Parameters
:
symbol (str) – Symbol name.

exchange (str) – Destination exchange.

currency (str) – Underlying currency.

dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.contract.TagValue(tag, value)[source]
Create new instance of TagValue(tag, value)

tag: str
value: str
classib_async.contract.ComboLeg(conId=0, ratio=0, action='', exchange='', openClose=0, shortSaleSlot=0, designatedLocation='', exemptCode=-1)[source]
conId: int= 0
ratio: int= 0
action: str= ''
exchange: str= ''
openClose: int= 0
shortSaleSlot: int= 0
designatedLocation: str= ''
exemptCode: int= -1
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.contract.DeltaNeutralContract(conId=0, delta=0.0, price=0.0)[source]
conId: int= 0
delta: float= 0.0
price: float= 0.0
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.contract.TradingSession(start, end)[source]
Create new instance of TradingSession(start, end)

start: datetime
end: datetime
classib_async.contract.ContractDetails(contract=None, marketName='', minTick=0.0, orderTypes='', validExchanges='', priceMagnifier=0, underConId=0, longName='', contractMonth='', industry='', category='', subcategory='', timeZoneId='', tradingHours='', liquidHours='', evRule='', evMultiplier=0, mdSizeMultiplier=1, aggGroup=0, underSymbol='', underSecType='', marketRuleIds='', secIdList=<factory>, realExpirationDate='', lastTradeTime='', stockType='', minSize=0.0, sizeIncrement=0.0, suggestedSizeIncrement=0.0, cusip='', ratings='', descAppend='', bondType='', couponType='', callable=False, putable=False, coupon=0, convertible=False, maturity='', issueDate='', nextOptionDate='', nextOptionType='', nextOptionPartial=False, notes='')[source]
contract: Optional[Contract]= None
marketName: str= ''
minTick: float= 0.0
orderTypes: str= ''
validExchanges: str= ''
priceMagnifier: int= 0
underConId: int= 0
longName: str= ''
contractMonth: str= ''
industry: str= ''
category: str= ''
subcategory: str= ''
timeZoneId: str= ''
tradingHours: str= ''
liquidHours: str= ''
evRule: str= ''
evMultiplier: int= 0
mdSizeMultiplier: int= 1
aggGroup: int= 0
underSymbol: str= ''
underSecType: str= ''
marketRuleIds: str= ''
secIdList: List[TagValue]
realExpirationDate: str= ''
lastTradeTime: str= ''
stockType: str= ''
minSize: float= 0.0
sizeIncrement: float= 0.0
suggestedSizeIncrement: float= 0.0
cusip: str= ''
ratings: str= ''
descAppend: str= ''
bondType: str= ''
couponType: str= ''
callable: bool= False
putable: bool= False
coupon: float= 0
convertible: bool= False
maturity: str= ''
issueDate: str= ''
nextOptionDate: str= ''
nextOptionType: str= ''
nextOptionPartial: bool= False
notes: str= ''
tradingSessions()[source]
Return type
:
List[TradingSession]

liquidSessions()[source]
Return type
:
List[TradingSession]

dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.contract.ContractDescription(contract=None, derivativeSecTypes=<factory>)[source]
contract: Optional[Contract]= None
derivativeSecTypes: List[str]
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.contract.ScanData(rank, contractDetails, distance, benchmark, projection, legsStr)[source]
rank: int
contractDetails: ContractDetails
distance: str
benchmark: str
projection: str
legsStr: str
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

Ticker
Access to realtime market information.

classib_async.ticker.Ticker(contract=None, time=None, marketDataType=1, minTick=nan, bid=nan, bidSize=nan, bidExchange='', ask=nan, askSize=nan, askExchange='', last=nan, lastSize=nan, lastExchange='', prevBid=nan, prevBidSize=nan, prevAsk=nan, prevAskSize=nan, prevLast=nan, prevLastSize=nan, volume=nan, open=nan, high=nan, low=nan, close=nan, vwap=nan, low13week=nan, high13week=nan, low26week=nan, high26week=nan, low52week=nan, high52week=nan, bidYield=nan, askYield=nan, lastYield=nan, markPrice=nan, halted=nan, rtHistVolatility=nan, rtVolume=nan, rtTradeVolume=nan, rtTime=None, avVolume=nan, tradeCount=nan, tradeRate=nan, volumeRate=nan, shortableShares=nan, indexFuturePremium=nan, futuresOpenInterest=nan, putOpenInterest=nan, callOpenInterest=nan, putVolume=nan, callVolume=nan, avOptionVolume=nan, histVolatility=nan, impliedVolatility=nan, dividends=None, fundamentalRatios=None, ticks=<factory>, tickByTicks=<factory>, domBids=<factory>, domBidsDict=<factory>, domAsks=<factory>, domAsksDict=<factory>, domTicks=<factory>, bidGreeks=None, askGreeks=None, lastGreeks=None, modelGreeks=None, auctionVolume=nan, auctionPrice=nan, auctionImbalance=nan, regulatoryImbalance=nan, bboExchange='', snapshotPermissions=0)[source]
Current market data such as bid, ask, last price, etc. for a contract.

Streaming level-1 ticks of type TickData are stored in the ticks list.

Streaming level-2 ticks of type MktDepthData are stored in the domTicks list. The order book (DOM) is available as lists of DOMLevel in domBids and domAsks.

Streaming tick-by-tick ticks are stored in tickByTicks.

For options the OptionComputation values for the bid, ask, resp. last price are stored in the bidGreeks, askGreeks resp. lastGreeks attributes. There is also modelGreeks that conveys the greeks as calculated by Interactive Brokers’ option model.

Events:
updateEvent (ticker: Ticker)

events: ClassVar= ('updateEvent',)
contract: Optional[Contract]= None
time: Optional[datetime]= None
marketDataType: int= 1
minTick: float= nan
bid: float= nan
bidSize: float= nan
bidExchange: str= ''
ask: float= nan
askSize: float= nan
askExchange: str= ''
last: float= nan
lastSize: float= nan
lastExchange: str= ''
prevBid: float= nan
prevBidSize: float= nan
prevAsk: float= nan
prevAskSize: float= nan
prevLast: float= nan
prevLastSize: float= nan
volume: float= nan
open: float= nan
high: float= nan
low: float= nan
close: float= nan
vwap: float= nan
low13week: float= nan
high13week: float= nan
low26week: float= nan
high26week: float= nan
low52week: float= nan
high52week: float= nan
bidYield: float= nan
askYield: float= nan
lastYield: float= nan
markPrice: float= nan
halted: float= nan
rtHistVolatility: float= nan
rtVolume: float= nan
rtTradeVolume: float= nan
rtTime: Optional[datetime]= None
avVolume: float= nan
tradeCount: float= nan
tradeRate: float= nan
volumeRate: float= nan
shortableShares: float= nan
indexFuturePremium: float= nan
futuresOpenInterest: float= nan
putOpenInterest: float= nan
callOpenInterest: float= nan
putVolume: float= nan
callVolume: float= nan
avOptionVolume: float= nan
histVolatility: float= nan
impliedVolatility: float= nan
dividends: Optional[Dividends]= None
fundamentalRatios: Optional[FundamentalRatios]= None
ticks: List[TickData]
tickByTicks: List[Union[TickByTickAllLast, TickByTickBidAsk, TickByTickMidPoint]]
domBids: List[DOMLevel]
domBidsDict: dict[int, DOMLevel]
domAsks: List[DOMLevel]
domAsksDict: dict[int, DOMLevel]
domTicks: List[MktDepthData]
bidGreeks: Optional[OptionComputation]= None
askGreeks: Optional[OptionComputation]= None
lastGreeks: Optional[OptionComputation]= None
modelGreeks: Optional[OptionComputation]= None
auctionVolume: float= nan
auctionPrice: float= nan
auctionImbalance: float= nan
regulatoryImbalance: float= nan
bboExchange: str= ''
snapshotPermissions: int= 0
hasBidAsk()[source]
See if this ticker has a valid bid and ask.

Return type
:
bool

midpoint()[source]
Return average of bid and ask, or NaN if no valid bid and ask are available.

Return type
:
float

marketPrice()[source]
Return the first available one of :rtype: float

last price if within current bid/ask or no bid/ask available;

average of bid and ask (midpoint).

dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.ticker.TickerUpdateEvent(name='', _with_error_done_events=True)[source]
trades()[source]
Emit trade ticks.

Return type
:
Tickfilter

bids()[source]
Emit bid ticks.

Return type
:
Tickfilter

asks()[source]
Emit ask ticks.

Return type
:
Tickfilter

bidasks()[source]
Emit bid and ask ticks.

Return type
:
Tickfilter

midpoints()[source]
Emit midpoint ticks.

Return type
:
Tickfilter

classib_async.ticker.Tickfilter(tickTypes, source=None)[source]
Tick filtering event operators that emit(time, price, size).

on_source(ticker)[source]
Emit a new value to all connected listeners.

Parameters
:
args – Argument values to emit to listeners.

timebars(timer)[source]
Aggregate ticks into time bars, where the timing of new bars is derived from a timer event. Emits a completed Bar.

This event stores a BarList of all created bars in the bars property.

Parameters
:
timer (Event) – Event for timing when a new bar starts.

Return type
:
TimeBars

tickbars(count)[source]
Aggregate ticks into bars that have the same number of ticks. Emits a completed Bar.

This event stores a BarList of all created bars in the bars property.

Parameters
:
count (int) – Number of ticks to use to form one bar.

Return type
:
TickBars

volumebars(volume)[source]
Aggregate ticks into bars that have the same volume. Emits a completed Bar.

This event stores a BarList of all created bars in the bars property.

Parameters
:
count – Number of ticks to use to form one bar.

Return type
:
VolumeBars

classib_async.ticker.Midpoints(tickTypes, source=None)[source]
on_source(ticker)[source]
Emit a new value to all connected listeners.

Parameters
:
args – Argument values to emit to listeners.

classib_async.ticker.Bar(time, open=nan, high=nan, low=nan, close=nan, volume=0, count=0)[source]
time: Optional[datetime]
open: float= nan
high: float= nan
low: float= nan
close: float= nan
volume: int= 0
count: int= 0
classib_async.ticker.BarList(*args)[source]
classib_async.ticker.TimeBars(timer, source=None)[source]
Aggregate ticks into time bars, where the timing of new bars is derived from a timer event. Emits a completed Bar.

This event stores a BarList of all created bars in the bars property.

Parameters
:
timer – Event for timing when a new bar starts.

bars: BarList
on_source(time, price, size)[source]
Emit a new value to all connected listeners.

Parameters
:
args – Argument values to emit to listeners.

classib_async.ticker.TickBars(count, source=None)[source]
Aggregate ticks into bars that have the same number of ticks. Emits a completed Bar.

This event stores a BarList of all created bars in the bars property.

Parameters
:
count – Number of ticks to use to form one bar.

bars: BarList
on_source(time, price, size)[source]
Emit a new value to all connected listeners.

Parameters
:
args – Argument values to emit to listeners.

classib_async.ticker.VolumeBars(volume, source=None)[source]
Aggregate ticks into bars that have the same volume. Emits a completed Bar.

This event stores a BarList of all created bars in the bars property.

Parameters
:
count – Number of ticks to use to form one bar.

bars: BarList
on_source(time, price, size)[source]
Emit a new value to all connected listeners.

Parameters
:
args – Argument values to emit to listeners.

Objects
Object hierarchy.

classib_async.objects.ScannerSubscription(numberOfRows=-1, instrument='', locationCode='', scanCode='', abovePrice=1.7976931348623157e+308, belowPrice=1.7976931348623157e+308, aboveVolume=2147483647, marketCapAbove=1.7976931348623157e+308, marketCapBelow=1.7976931348623157e+308, moodyRatingAbove='', moodyRatingBelow='', spRatingAbove='', spRatingBelow='', maturityDateAbove='', maturityDateBelow='', couponRateAbove=1.7976931348623157e+308, couponRateBelow=1.7976931348623157e+308, excludeConvertible=False, averageOptionVolumeAbove=2147483647, scannerSettingPairs='', stockTypeFilter='')[source]
numberOfRows: int= -1
instrument: str= ''
locationCode: str= ''
scanCode: str= ''
abovePrice: float= 1.7976931348623157e+308
belowPrice: float= 1.7976931348623157e+308
aboveVolume: int= 2147483647
marketCapAbove: float= 1.7976931348623157e+308
marketCapBelow: float= 1.7976931348623157e+308
moodyRatingAbove: str= ''
moodyRatingBelow: str= ''
spRatingAbove: str= ''
spRatingBelow: str= ''
maturityDateAbove: str= ''
maturityDateBelow: str= ''
couponRateAbove: float= 1.7976931348623157e+308
couponRateBelow: float= 1.7976931348623157e+308
excludeConvertible: bool= False
averageOptionVolumeAbove: int= 2147483647
scannerSettingPairs: str= ''
stockTypeFilter: str= ''
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.objects.SoftDollarTier(name='', val='', displayName='')[source]
name: str= ''
val: str= ''
displayName: str= ''
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.objects.Execution(execId='', time=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc), acctNumber='', exchange='', side='', shares=0.0, price=0.0, permId=0, clientId=0, orderId=0, liquidation=0, cumQty=0.0, avgPrice=0.0, orderRef='', evRule='', evMultiplier=0.0, modelCode='', lastLiquidity=0, pendingPriceRevision=False)[source]
execId: str= ''
time: datetime= datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
acctNumber: str= ''
exchange: str= ''
side: str= ''
shares: float= 0.0
price: float= 0.0
permId: int= 0
clientId: int= 0
orderId: int= 0
liquidation: int= 0
cumQty: float= 0.0
avgPrice: float= 0.0
orderRef: str= ''
evRule: str= ''
evMultiplier: float= 0.0
modelCode: str= ''
lastLiquidity: int= 0
pendingPriceRevision: bool= False
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.objects.CommissionReport(execId='', commission=0.0, currency='', realizedPNL=0.0, yield_=0.0, yieldRedemptionDate=0)[source]
execId: str= ''
commission: float= 0.0
currency: str= ''
realizedPNL: float= 0.0
yield_: float= 0.0
yieldRedemptionDate: int= 0
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.objects.ExecutionFilter(clientId=0, acctCode='', time='', symbol='', secType='', exchange='', side='')[source]
clientId: int= 0
acctCode: str= ''
time: str= ''
symbol: str= ''
secType: str= ''
exchange: str= ''
side: str= ''
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.objects.BarData(date=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc), open=0.0, high=0.0, low=0.0, close=0.0, volume=0, average=0.0, barCount=0)[source]
date: Union[date, datetime]= datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
open: float= 0.0
high: float= 0.0
low: float= 0.0
close: float= 0.0
volume: float= 0
average: float= 0.0
barCount: int= 0
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.objects.RealTimeBar(time=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc), endTime=-1, open_=0.0, high=0.0, low=0.0, close=0.0, volume=0.0, wap=0.0, count=0)[source]
time: datetime= datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
endTime: int= -1
open_: float= 0.0
high: float= 0.0
low: float= 0.0
close: float= 0.0
volume: float= 0.0
wap: float= 0.0
count: int= 0
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.objects.TickAttrib(canAutoExecute=False, pastLimit=False, preOpen=False)[source]
canAutoExecute: bool= False
pastLimit: bool= False
preOpen: bool= False
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.objects.TickAttribBidAsk(bidPastLow=False, askPastHigh=False)[source]
bidPastLow: bool= False
askPastHigh: bool= False
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.objects.TickAttribLast(pastLimit=False, unreported=False)[source]
pastLimit: bool= False
unreported: bool= False
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.objects.HistogramData(price=0.0, count=0)[source]
price: float= 0.0
count: int= 0
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.objects.NewsProvider(code='', name='')[source]
code: str= ''
name: str= ''
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.objects.DepthMktDataDescription(exchange='', secType='', listingExch='', serviceDataType='', aggGroup=2147483647)[source]
exchange: str= ''
secType: str= ''
listingExch: str= ''
serviceDataType: str= ''
aggGroup: int= 2147483647
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.objects.PnL(account='', modelCode='', dailyPnL=nan, unrealizedPnL=nan, realizedPnL=nan)[source]
account: str= ''
modelCode: str= ''
dailyPnL: float= nan
unrealizedPnL: float= nan
realizedPnL: float= nan
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.objects.TradeLogEntry(time, status='', message='', errorCode=0)[source]
time: datetime
status: str= ''
message: str= ''
errorCode: int= 0
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.objects.PnLSingle(account='', modelCode='', conId=0, dailyPnL=nan, unrealizedPnL=nan, realizedPnL=nan, position=0, value=nan)[source]
account: str= ''
modelCode: str= ''
conId: int= 0
dailyPnL: float= nan
unrealizedPnL: float= nan
realizedPnL: float= nan
position: int= 0
value: float= nan
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.objects.HistoricalSession(startDateTime='', endDateTime='', refDate='')[source]
startDateTime: str= ''
endDateTime: str= ''
refDate: str= ''
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.objects.HistoricalSchedule(startDateTime='', endDateTime='', timeZone='', sessions=<factory>)[source]
startDateTime: str= ''
endDateTime: str= ''
timeZone: str= ''
sessions: List[HistoricalSession]
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.objects.WshEventData(conId=2147483647, filter='', fillWatchlist=False, fillPortfolio=False, fillCompetitors=False, startDate='', endDate='', totalLimit=2147483647)[source]
conId: int= 2147483647
filter: str= ''
fillWatchlist: bool= False
fillPortfolio: bool= False
fillCompetitors: bool= False
startDate: str= ''
endDate: str= ''
totalLimit: int= 2147483647
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

classib_async.objects.AccountValue(account, tag, value, currency, modelCode)[source]
Create new instance of AccountValue(account, tag, value, currency, modelCode)

account: str
tag: str
value: str
currency: str
modelCode: str
classib_async.objects.TickData(time, tickType, price, size)[source]
Create new instance of TickData(time, tickType, price, size)

time: datetime
tickType: int
price: float
size: float
classib_async.objects.HistoricalTick(time, price, size)[source]
Create new instance of HistoricalTick(time, price, size)

time: datetime
price: float
size: float
classib_async.objects.HistoricalTickBidAsk(time, tickAttribBidAsk, priceBid, priceAsk, sizeBid, sizeAsk)[source]
Create new instance of HistoricalTickBidAsk(time, tickAttribBidAsk, priceBid, priceAsk, sizeBid, sizeAsk)

time: datetime
tickAttribBidAsk: TickAttribBidAsk
priceBid: float
priceAsk: float
sizeBid: float
sizeAsk: float
classib_async.objects.HistoricalTickLast(time, tickAttribLast, price, size, exchange, specialConditions)[source]
Create new instance of HistoricalTickLast(time, tickAttribLast, price, size, exchange, specialConditions)

time: datetime
tickAttribLast: TickAttribLast
price: float
size: float
exchange: str
specialConditions: str
classib_async.objects.TickByTickAllLast(tickType, time, price, size, tickAttribLast, exchange, specialConditions)[source]
Create new instance of TickByTickAllLast(tickType, time, price, size, tickAttribLast, exchange, specialConditions)

tickType: int
time: datetime
price: float
size: float
tickAttribLast: TickAttribLast
exchange: str
specialConditions: str
classib_async.objects.TickByTickBidAsk(time, bidPrice, askPrice, bidSize, askSize, tickAttribBidAsk)[source]
Create new instance of TickByTickBidAsk(time, bidPrice, askPrice, bidSize, askSize, tickAttribBidAsk)

time: datetime
bidPrice: float
askPrice: float
bidSize: float
askSize: float
tickAttribBidAsk: TickAttribBidAsk
classib_async.objects.TickByTickMidPoint(time, midPoint)[source]
Create new instance of TickByTickMidPoint(time, midPoint)

time: datetime
midPoint: float
classib_async.objects.MktDepthData(time, position, marketMaker, operation, side, price, size)[source]
Create new instance of MktDepthData(time, position, marketMaker, operation, side, price, size)

time: datetime
position: int
marketMaker: str
operation: int
side: int
price: float
size: float
classib_async.objects.DOMLevel(price, size, marketMaker)[source]
Create new instance of DOMLevel(price, size, marketMaker)

price: float
size: float
marketMaker: str
classib_async.objects.PriceIncrement(lowEdge, increment)[source]
Create new instance of PriceIncrement(lowEdge, increment)

lowEdge: float
increment: float
classib_async.objects.PortfolioItem(contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, account)[source]
Create new instance of PortfolioItem(contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, account)

contract: Contract
position: float
marketPrice: float
marketValue: float
averageCost: float
unrealizedPNL: float
realizedPNL: float
account: str
classib_async.objects.Position(account, contract, position, avgCost)[source]
Create new instance of Position(account, contract, position, avgCost)

account: str
contract: Contract
position: float
avgCost: float
classib_async.objects.Fill(contract, execution, commissionReport, time)[source]
Create new instance of Fill(contract, execution, commissionReport, time)

contract: Contract
execution: Execution
commissionReport: CommissionReport
time: datetime
classib_async.objects.OptionComputation(tickAttrib, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice)[source]
Create new instance of OptionComputation(tickAttrib, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice)

tickAttrib: int
impliedVol: Optional[float]
delta: Optional[float]
optPrice: Optional[float]
pvDividend: Optional[float]
gamma: Optional[float]
vega: Optional[float]
theta: Optional[float]
undPrice: Optional[float]
classib_async.objects.OptionChain(exchange, underlyingConId, tradingClass, multiplier, expirations, strikes)[source]
Create new instance of OptionChain(exchange, underlyingConId, tradingClass, multiplier, expirations, strikes)

exchange: str
underlyingConId: int
tradingClass: str
multiplier: str
expirations: List[str]
strikes: List[float]
classib_async.objects.Dividends(past12Months, next12Months, nextDate, nextAmount)[source]
Create new instance of Dividends(past12Months, next12Months, nextDate, nextAmount)

past12Months: Optional[float]
next12Months: Optional[float]
nextDate: Optional[date]
nextAmount: Optional[float]
classib_async.objects.NewsArticle(articleType, articleText)[source]
Create new instance of NewsArticle(articleType, articleText)

articleType: int
articleText: str
classib_async.objects.HistoricalNews(time, providerCode, articleId, headline)[source]
Create new instance of HistoricalNews(time, providerCode, articleId, headline)

time: datetime
providerCode: str
articleId: str
headline: str
classib_async.objects.NewsTick(timeStamp, providerCode, articleId, headline, extraData)[source]
Create new instance of NewsTick(timeStamp, providerCode, articleId, headline, extraData)

timeStamp: int
providerCode: str
articleId: str
headline: str
extraData: str
classib_async.objects.NewsBulletin(msgId, msgType, message, origExchange)[source]
Create new instance of NewsBulletin(msgId, msgType, message, origExchange)

msgId: int
msgType: int
message: str
origExchange: str
classib_async.objects.FamilyCode(accountID, familyCodeStr)[source]
Create new instance of FamilyCode(accountID, familyCodeStr)

accountID: str
familyCodeStr: str
classib_async.objects.SmartComponent(bitNumber, exchange, exchangeLetter)[source]
Create new instance of SmartComponent(bitNumber, exchange, exchangeLetter)

bitNumber: int
exchange: str
exchangeLetter: str
classib_async.objects.ConnectionStats(startTime, duration, numBytesRecv, numBytesSent, numMsgRecv, numMsgSent)[source]
Create new instance of ConnectionStats(startTime, duration, numBytesRecv, numBytesSent, numMsgRecv, numMsgSent)

startTime: float
duration: float
numBytesRecv: int
numBytesSent: int
numMsgRecv: int
numMsgSent: int
classib_async.objects.BarDataList(*args)[source]
List of BarData that also stores all request parameters.

Events:

updateEvent (bars: BarDataList, hasNewBar: bool)

reqId: int
contract: Contract
endDateTime: Union[datetime, date, str, None]
durationStr: str
barSizeSetting: str
whatToShow: str
useRTH: bool
formatDate: int
keepUpToDate: bool
chartOptions: List[TagValue]
classib_async.objects.RealTimeBarList(*args)[source]
List of RealTimeBar that also stores all request parameters.

Events:

updateEvent (bars: RealTimeBarList, hasNewBar: bool)

reqId: int
contract: Contract
barSize: int
whatToShow: str
useRTH: bool
realTimeBarsOptions: List[TagValue]
classib_async.objects.ScanDataList(*args)[source]
List of ScanData that also stores all request parameters.

Events:
updateEvent (ScanDataList)

reqId: int
subscription: ScannerSubscription
scannerSubscriptionOptions: List[TagValue]
scannerSubscriptionFilterOptions: List[TagValue]
classib_async.objects.DynamicObject(**kwargs)[source]
classib_async.objects.FundamentalRatios(**kwargs)[source]
See: https://web.archive.org/web/20200725010343/https://interactivebrokers.github.io/tws-api/fundamental_ratios_tags.html

classib_async.wrapper.RequestError(reqId, code, message)[source]
Exception to raise when the API reports an error that can be tied to a single request.

Parameters
:
reqId (int) – Original request ID.

code (int) – Original error code.

message (str) – Original error message.

Utilities
Utilities.

ib_async.util.globalErrorEvent(*args)= Event<Event, []>
Event to emit global exceptions.

ib_async.util.df(objs, labels=None)[source]
Create pandas DataFrame from the sequence of same-type objects.

Parameters
:
labels (Optional[List[str]]) – If supplied, retain only the given labels and drop the rest.

ib_async.util.dataclassAsDict(obj)[source]
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

ib_async.util.dataclassAsTuple(obj)[source]
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

ib_async.util.dataclassNonDefaults(obj)[source]
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

ib_async.util.dataclassUpdate(obj, *srcObjs, **kwargs)[source]
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

ib_async.util.dataclassRepr(obj)[source]
Provide a culled representation of the given dataclass instance, showing only the fields with a non-default value.

Return type
:
str

ib_async.util.isnamedtupleinstance(x)[source]
From https://stackoverflow.com/a/2166841/6067848

ib_async.util.tree(obj)[source]
Convert object to a tree of lists, dicts and simple values. The result can be serialized to JSON.

ib_async.util.barplot(bars, title='', upColor='blue', downColor='red')[source]
Create candlestick plot for the given bars. The bars can be given as a DataFrame or as a list of bar objects.

ib_async.util.allowCtrlC()[source]
Allow Control-C to end program.

ib_async.util.logToFile(path, level=20)[source]
Create a log handler that logs to the given file.

ib_async.util.logToConsole(level=20)[source]
Create a log handler that logs to the console.

ib_async.util.isNan(x)[source]
Not a number test.

Return type
:
bool

ib_async.util.formatSI(n)[source]
Format the integer or float n to 3 significant digits + SI prefix.

Return type
:
str

classib_async.util.timeit(title='Run')[source]
Context manager for timing.

ib_async.util.run(*awaitables, timeout=None)[source]
By default run the event loop forever.

When awaitables (like Tasks, Futures or coroutines) are given then run the event loop until each has completed and return their results.

An optional timeout (in seconds) can be given that will raise asyncio.TimeoutError if the awaitables are not ready within the timeout period.

ib_async.util.schedule(time, callback, *args)[source]
Schedule the callback to be run at the given time with the given arguments. This will return the Event Handle.

Parameters
:
time (Union[time, datetime]) – Time to run callback. If given as datetime.time then use today as date.

callback (Callable) – Callable scheduled to run.

args – Arguments for to call callback with.

ib_async.util.sleep(secs=0.02)[source]
Wait for the given amount of seconds while everything still keeps processing in the background. Never use time.sleep().

Parameters
:
secs (float) – Time in seconds to wait.

Return type
:
bool

ib_async.util.timeRange(start, end, step)[source]
Iterator that waits periodically until certain time points are reached while yielding those time points.

Parameters
:
start (Union[time, datetime]) – Start time, can be specified as datetime.datetime, or as datetime.time in which case today is used as the date

end (Union[time, datetime]) – End time, can be specified as datetime.datetime, or as datetime.time in which case today is used as the date

step (float) – The number of seconds of each period

Return type
:
Iterator[datetime]

ib_async.util.waitUntil(t)[source]
Wait until the given time t is reached.

Parameters
:
t (Union[time, datetime]) – The time t can be specified as datetime.datetime, or as datetime.time in which case today is used as the date.

Return type
:
bool

asyncib_async.util.timeRangeAsync(start, end, step)[source]
Async version of timeRange().

Return type
:
AsyncIterator[datetime]

asyncib_async.util.waitUntilAsync(t)[source]
Async version of waitUntil().

Return type
:
bool

ib_async.util.patchAsyncio()[source]
Patch asyncio to allow nested event loops.

ib_async.util.getLoop()[source]
Get the asyncio event loop for the current thread.

ib_async.util.startLoop()[source]
Use nested asyncio event loop for Jupyter notebooks.

ib_async.util.useQt(qtLib='PyQt5', period=0.01)[source]
Run combined Qt5/asyncio event loop.

Parameters
:
qtLib (str) –

Name of Qt library to use:

PyQt5

PyQt6

PySide2

PySide6

period (float) – Period in seconds to poll Qt.

ib_async.util.formatIBDatetime(t)[source]
Format date or datetime to string that IB uses.

Return type
:
str

ib_async.util.parseIBDatetime(s)[source]
Parse string in IB date or datetime format to datetime.

Return type
:
Union[date, datetime]

FlexReport
Access to account statement webservice.

exceptionib_async.flexreport.FlexError[source]
classib_async.flexreport.FlexReport(token=None, queryId=None, path=None)[source]
To obtain a token:

Login to web portal

Go to Settings

Click on “Configure Flex Web Service”

Generate token

Download a report by giving a valid token and queryId, or load from file by giving a valid path.

data: bytes
root: Element
topics()[source]
Get the set of topics that can be extracted from this report.

extract(topic, parseNumbers=True)[source]
Extract items of given topic and return as list of objects.

The topic is a string like TradeConfirm, ChangeInDividendAccrual, Order, etc.

Return type
:
list

df(topic, parseNumbers=True)[source]
Same as extract but return the result as a pandas DataFrame.

download(token, queryId)[source]
Download report for the given token and queryId.

load(path)[source]
Load report from XML file.

save(path)[source]
Save report to XML file.

IBC
classib_async.ibcontroller.IBC(twsVersion=0, gateway=False, tradingMode='', twsPath='', twsSettingsPath='', ibcPath='', ibcIni='', javaPath='', userid='', password='', fixuserid='', fixpassword='', on2fatimeout='')[source]
Programmatic control over starting and stopping TWS/Gateway using IBC (https://github.com/IbcAlpha/IBC).

Parameters
:
twsVersion (int) – (required) The major version number for TWS or gateway.

gateway (bool) –

True = gateway

False = TWS

tradingMode (str) – ‘live’ or ‘paper’.

userid (str) – IB account username. It is recommended to set the real username/password in a secured IBC config file.

password (str) – IB account password.

twsPath (str) –

Path to the TWS installation folder. Defaults:

Linux: ~/Jts

OS X: ~/Applications

Windows: C:\Jts

twsSettingsPath (str) –

Path to the TWS settings folder. Defaults:

Linux: ~/Jts

OS X: ~/Jts

Windows: Not available

ibcPath (str) –

Path to the IBC installation folder. Defaults:

Linux: /opt/ibc

OS X: /opt/ibc

Windows: C:\IBC

ibcIni (str) –

Path to the IBC configuration file. Defaults:

Linux: ~/ibc/config.ini

OS X: ~/ibc/config.ini

Windows: %%HOMEPATH%%\DocumentsIBC\config.ini

javaPath (str) – Path to Java executable. Default is to use the Java VM included with TWS/gateway.

fixuserid (str) – FIX account user id (gateway only).

fixpassword (str) – FIX account password (gateway only).

on2fatimeout (str) – What to do if 2-factor authentication times out; Can be ‘restart’ or ‘exit’.

This is not intended to be run in a notebook.

To use IBC on Windows, the proactor (or quamash) event loop must have been set:

import asyncio
asyncio.set_event_loop(asyncio.ProactorEventLoop())
Example usage:

ibc = IBC(976, gateway=True, tradingMode='live',
    userid='edemo', password='demouser')
ibc.start()
IB.run()
IbcLogLevel: ClassVar= 10
twsVersion: int= 0
gateway: bool= False
tradingMode: str= ''
twsPath: str= ''
twsSettingsPath: str= ''
ibcPath: str= ''
ibcIni: str= ''
javaPath: str= ''
userid: str= ''
password: str= ''
fixuserid: str= ''
fixpassword: str= ''
on2fatimeout: str= ''
start()[source]
Launch TWS/IBG.

terminate()[source]
Terminate TWS/IBG.

asyncstartAsync()[source]
asyncterminateAsync()[source]
asyncmonitorAsync()[source]
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

Watchdog
classib_async.ibcontroller.Watchdog(controller, ib, host='127.0.0.1', port=7497, clientId=1, connectTimeout=2, appStartupTime=30, appTimeout=20, retryDelay=2, readonly=False, account='', raiseSyncErrors=False, probeContract=Forex('EURUSD', exchange='IDEALPRO'), probeTimeout=4)[source]
Start, connect and watch over the TWS or gateway app and try to keep it up and running. It is intended to be used in an event-driven application that properly initializes itself upon (re-)connect.

It is not intended to be used in a notebook or in imperative-style code. Do not expect Watchdog to magically shield you from reality. Do not use Watchdog unless you understand what it does and doesn’t do.

Parameters
:
controller (IBC) – (required) IBC instance.

ib (IB) – (required) IB instance to be used. Do not connect this instance as Watchdog takes care of that.

host (str) – Used for connecting IB instance.

port (int) – Used for connecting IB instance.

clientId (int) – Used for connecting IB instance.

connectTimeout (float) – Used for connecting IB instance.

readonly (bool) – Used for connecting IB instance.

appStartupTime (float) – Time (in seconds) that the app is given to start up. Make sure that it is given ample time.

appTimeout (float) – Timeout (in seconds) for network traffic idle time.

retryDelay (float) – Time (in seconds) to restart app after a previous failure.

probeContract (Contract) – Contract to use for historical data probe requests (default is EURUSD).

probeTimeout (float); Timeout (in seconds)

The idea is to wait until there is no traffic coming from the app for a certain amount of time (the appTimeout parameter). This triggers a historical request to be placed just to see if the app is still alive and well. If yes, then continue, if no then restart the whole app and reconnect. Restarting will also occur directly on errors 1100 and 100.

Example usage:

def onConnected():
    print(ib.accountValues())

ibc = IBC(974, gateway=True, tradingMode='paper')
ib = IB()
ib.connectedEvent += onConnected
watchdog = Watchdog(ibc, ib, port=4002)
watchdog.start()
ib.run()
Events:
startingEvent (watchdog: Watchdog)

startedEvent (watchdog: Watchdog)

stoppingEvent (watchdog: Watchdog)

stoppedEvent (watchdog: Watchdog)

softTimeoutEvent (watchdog: Watchdog)

hardTimeoutEvent (watchdog: Watchdog)

events= ['startingEvent', 'startedEvent', 'stoppingEvent', 'stoppedEvent', 'softTimeoutEvent', 'hardTimeoutEvent']
controller: IBC
ib: IB
host: str= '127.0.0.1'
port: int= 7497
clientId: int= 1
connectTimeout: float= 2
appStartupTime: float= 30
appTimeout: float= 20
retryDelay: float= 2
readonly: bool= False
account: str= ''
raiseSyncErrors: bool= False
probeContract: Contract= Forex('EURUSD', exchange='IDEALPRO')
probeTimeout: float= 4
start()[source]
stop()[source]
asyncrunAsync()[source]
dict()
Return dataclass values as dict. This is a non-recursive variant of dataclasses.asdict.

Return type
:
dict

nonDefaults()
For a dataclass instance get the fields that are different from the default values and return as dict.

Return type
:
dict

tuple()
Return dataclass values as tuple. This is a non-recursive variant of dataclasses.astuple.

Return type
:
tuple

update(*srcObjs, **kwargs)
Update fields of the given dataclass object from zero or more dataclass source objects and/or from keyword arguments.

Return type
:
object

