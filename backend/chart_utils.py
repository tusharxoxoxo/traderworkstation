import pandas as pd
import numpy as np
import mplfinance as mpf
from typing import Optional, Tuple, Dict


def calculate_sma(data: pd.DataFrame, period: int = 20) -> pd.Series:
    """Calculate Simple Moving Average"""
    return data["close"].rolling(window=period).mean()


def calculate_ema(data: pd.DataFrame, period: int = 20) -> pd.Series:
    """Calculate Exponential Moving Average"""
    return data["close"].ewm(span=period, adjust=False).mean()


def calculate_rsi(data: pd.DataFrame, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index"""
    delta = data["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def plot_candlestick_chart(
    data: pd.DataFrame,
    title: str = "Price Chart",
    ma_periods: Optional[Tuple[int, ...]] = (20,),
    volume: bool = True,
    rsi: bool = True,
) -> None:
    """Plot candlestick chart with optional indicators"""
    # Prepare data
    df = data.copy()
    df.index = pd.to_datetime(df.index)

    # Calculate indicators
    if ma_periods:
        for period in ma_periods:
            df[f"SMA_{period}"] = calculate_sma(df, period)

    if rsi:
        df["RSI"] = calculate_rsi(df)

    # Prepare plot style and indicators
    mc = mpf.make_marketcolors(
        up="g", down="r", edge="inherit", wick="inherit", volume="in"
    )
    s = mpf.make_mpf_style(marketcolors=mc)

    # Prepare additional plots
    plots = []
    if ma_periods:
        for period in ma_periods:
            plots.append(
                mpf.make_addplot(
                    df[f"SMA_{period}"], panel=0, title=f"SMA{period}", color="blue"
                )
            )

    if rsi:
        plots.append(
            mpf.make_addplot(
                df["RSI"], panel=1, title="RSI", color="purple", ylim=(0, 100)
            )
        )

    # Create the plot
    mpf.plot(
        df,
        type="candle",
        style=s,
        title=title,
        volume=volume,
        addplot=plots if plots else None,
        panel_ratios=(2, 0.5) if rsi else (2, 0.5) if volume else None,
        figsize=(12, 8),
    )
