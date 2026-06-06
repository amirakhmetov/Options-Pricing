from option_contract import OptionContract
from black_scholes import black_scholes_price
from historical_volatility import get_close_price
from option_chain_analysis import get_call_data
from implied_vol import implied_volatility_bisection
import yfinance as yf


def main():
    ticker = "AAPL"
    call_data = get_call_data(ticker)
    spot = get_close_price(ticker)
    market_mid = (call_data["bid"] + call_data["ask"]) / 2

    dividend_yield = yf.Ticker(ticker).info.get("dividendYield", 0) / 100

    recovered_iv = implied_volatility_bisection(
        market_price=market_mid,
        spot=spot,
        strike=call_data["strike"],
        time_to_maturity=call_data["days_to_expiration"] / 365,
        risk_free_rate=0.05,
        dividend_yield=dividend_yield,
        option_type="call"
    )

    option = OptionContract(
        spot=spot,
        strike=call_data["strike"],
        time_to_maturity=call_data["days_to_expiration"] / 365,
        risk_free_rate=0.05,
        volatility=recovered_iv,
        dividend_yield=dividend_yield,
        option_type="call"
    )

    repriced_value = black_scholes_price(option)

    print("\n=== Market Validation Demo ===")
    print(f"Ticker: {ticker}")
    print(f"Spot Price: {spot:.2f}")
    print(f"Strike: {call_data['strike']:.2f}")
    print(f"Days to Expiration: {call_data['days_to_expiration']}")
    print(f"Market Midpoint: {market_mid:.4f}")
    print(f"Recovered IV: {recovered_iv:.4%}")
    print(f"Repriced Value: {repriced_value:.4f}")
    print(f"Pricing Error: {repriced_value - market_mid:.8f}")


if __name__ == "__main__":
    main()