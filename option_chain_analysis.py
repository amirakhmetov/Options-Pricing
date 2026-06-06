import yfinance as yf
from datetime import date, datetime

from historical_volatility import get_close_price
from implied_vol import implied_volatility_bisection


def get_target_expiration(ticker, min_days=30):
    """
    Find the first expiration date with at least min_days
    remaining until maturity.
    """

    current_date = date.today()

    for expiration_str in ticker.options:
        expiration_date = datetime.strptime(expiration_str, "%Y-%m-%d").date()

        days_to_expiration = (expiration_date - current_date).days

        if days_to_expiration >= min_days:
            return expiration_str, days_to_expiration

    raise ValueError(
        f"No expiration found with at least {min_days} days to maturity."
    )


def get_option_chain(ticker_symbol: str):
    """
    Load the option chain for the first expiration
    with at least 30 days to maturity.
    """

    ticker = yf.Ticker(ticker_symbol)
    expiration, days_to_expiration = get_target_expiration(ticker)
    chain = ticker.option_chain(expiration)

    return ticker, chain, days_to_expiration


def get_call_data(ticker_symbol: str):
    """
    Return the at-the-money call option closest to
    the current underlying price.
    """

    _, chain, days_to_expiration = (get_option_chain(ticker_symbol))
    calls = chain.calls[["strike", "bid", "ask", "lastPrice", "impliedVolatility"]]
    spot = get_close_price(ticker_symbol)

    closest_index = (calls["strike"] - spot).abs().idxmin()
    result = calls.loc[closest_index].copy()

    result["days_to_expiration"] = days_to_expiration

    return result


def get_put_data(ticker_symbol: str):
    """
    Return the at-the-money put option closest to
    the current underlying price.
    """

    _, chain, days_to_expiration = (get_option_chain(ticker_symbol))

    puts = chain.calls[["strike", "bid", "ask", "lastPrice", "impliedVolatility"]]

    spot = get_close_price(ticker_symbol)

    closest_index = (puts["strike"] - spot).abs().idxmin()

    result = puts.loc[closest_index].copy()

    result["days_to_expiration"] = (days_to_expiration)

    return result


def get_all_calls(ticker_symbol: str, min_moneyness=0.8, max_moneyness=1.2):
    """
    Return all call options for the selected expiration,
    including recovered implied volatility and market
    midpoint prices.
    """

    ticker, chain, days_to_expiration = (get_option_chain(ticker_symbol))

    spot = get_close_price(ticker_symbol)

    dividend_yield = (ticker.info.get("dividendYield", 0) / 100)

    calls_data = chain.calls[["strike", "bid", "ask", "lastPrice", "impliedVolatility"]].copy()

    calls_data["days_to_expiration"] = (days_to_expiration)

    calls_data["moneyness"] = (calls_data["strike"] / spot)

    calls_data = calls_data[
        (calls_data["moneyness"] >= min_moneyness) & (calls_data["moneyness"] <= max_moneyness)].copy()

    calls_data["market_mid"] = (calls_data["bid"] + calls_data["ask"]) / 2

    recovered_ivs = []

    for _, row in calls_data.iterrows():
        recovered_iv = (
            implied_volatility_bisection(
                market_price=row["market_mid"],
                spot=spot,
                strike=row["strike"],
                risk_free_rate=0.05,
                time_to_maturity=row["days_to_expiration"] / 365,
                dividend_yield=dividend_yield,
                option_type="call"
            )
        )

        recovered_ivs.append(recovered_iv)

    calls_data["recovered_iv"] = recovered_ivs



    return calls_data

#
# aapl = get_all_calls("AAPL")
#
# print(aapl['price_diff'])
