import yfinance as yf
import pandas
import numpy as np


def get_price_data(ticker: str, period: str = "1y"):
    data = yf.download(ticker, period=period, auto_adjust=True, progress=False)

    if data.empty:
        raise ValueError(f"No price data found for {ticker}")

    close_prices = data["Close"]

    if hasattr(close_prices, "columns"):
        close_prices = close_prices.iloc[:, 0]

    return close_prices.dropna()


def daily_returns(ticker: str, period: str = "1y"):
    close_prices = get_price_data(ticker, period)
    returns = close_prices.pct_change().dropna()
    return returns


def historical_volatility(ticker: str, period: str = "1y"):
    returns = daily_returns(ticker, period)
    daily_vol = returns.std()
    annualized_vol = daily_vol * np.sqrt(252)
    return annualized_vol


def get_close_price(ticker: str):
    price = yf.download(ticker, period="1y", progress=False)["Close"].iloc[-1].item()
    return price

