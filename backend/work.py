from ib_async import *
import pandas as pd
from chart_utils import plot_candlestick_chart


class MarketDataVisualizer:
    def __init__(self):
        self.ib = IB()
        self.ib.connect("127.0.0.1", 7497, clientId=2)
        self.ib.reqMarketDataType(4)  # Use delayed data
        self.timeframes = {
            "1min": "1 min",
            "5min": "5 mins",
            "1hour": "1 hour",
            "1day": "1 day",
        }

    def get_historical_data(self, contract, timeframe="1hour", duration="30 D"):
        try:
            # Try with MIDPOINT data first
            bars = self.ib.reqHistoricalData(
                contract,
                endDateTime="",
                durationStr=duration,
                barSizeSetting=self.timeframes[timeframe],
                whatToShow="MIDPOINT",
                useRTH=True,
            )
            if not bars:
                # If no MIDPOINT data, try with BID_ASK
                bars = self.ib.reqHistoricalData(
                    contract,
                    endDateTime="",
                    durationStr=duration,
                    barSizeSetting=self.timeframes[timeframe],
                    whatToShow="BID_ASK",
                    useRTH=True,
                )
            return util.df(bars) if bars else pd.DataFrame()
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return pd.DataFrame()

    def plot_market_data(self, contract, timeframe="1hour", duration="30 D"):
        df = self.get_historical_data(contract, timeframe, duration)
        if df.empty:
            print(f"No data available for {contract.symbol} with {timeframe} timeframe")
            return
        plot_candlestick_chart(
            df,
            title=f"{contract.symbol} {timeframe} Chart",
            ma_periods=(10, 20),
            volume=True,
            rsi=True,
        )


# Example usage
if __name__ == "__main__":
    try:
        visualizer = MarketDataVisualizer()
        # Create Forex contract for EUR/USD
        contract = Forex("EURUSD")
        contract.exchange = "IDEALPRO"

        # Plot different timeframes
        for timeframe in ["1hour", "1day"]:
            visualizer.plot_market_data(contract, timeframe=timeframe)
    except Exception as e:
        print(f"Error during execution: {e}")
