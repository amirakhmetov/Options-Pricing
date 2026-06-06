import matplotlib.pyplot as plt

from option_contract import OptionContract
from black_scholes import black_scholes_price
from binomial_tree import binomial_tree_price


def plot_binomial_convergence():

    option = OptionContract(
        spot=100,
        strike=100,
        time_to_maturity=1,
        risk_free_rate=0.05,
        volatility=0.20,
        dividend_yield=0,
        option_type="call"
    )

    bs_price = black_scholes_price(option)

    steps_list = [10, 50, 100, 500, 1000, 2000]
    errors = []

    for steps in steps_list:

        tree_price = binomial_tree_price(option,steps)

        error = abs(tree_price - bs_price)

        errors.append(error)

    plt.figure(figsize=(8, 5))

    plt.plot(steps_list, errors, marker="o")

    plt.xlabel("Number of Binomial Steps")
    plt.ylabel("Absolute Pricing Error")
    plt.title("Binomial Tree Convergence to Black-Scholes")
    plt.grid(True)

    plt.show()

print(plot_binomial_convergence())