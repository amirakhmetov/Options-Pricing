import matplotlib.pyplot as plt
from option_chain_analysis import get_all_calls

def plot_volatility_smile(ticker: str):
    calls_data = get_all_calls(ticker)

    plt.plot(
        calls_data["strike"],
        calls_data["impliedVolatility"],
        marker="o",
        label="Yahoo IV"
    )

    plt.plot(
        calls_data["strike"],
        calls_data["recovered_iv"],
        marker="x",
        label="Recovered IV"
    )

    plt.xlabel("Strike")
    plt.ylabel("Implied Volatility")
    plt.title("AAPL Implied Volatility Comparison")
    plt.legend()
    plt.grid(True)

    plt.show()

plot_volatility_smile("AAPL")