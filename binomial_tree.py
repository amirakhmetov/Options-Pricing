from option_contract import OptionContract
from math import exp, sqrt

def binomial_tree_price(
        contract: OptionContract,
        steps: int = 200,
        american: bool = False
) -> float:
    # """
    #     Price a vanilla option using the Cox-Ross-Rubinstein binomial tree.
    #
    #     Set american=True to allow early exercise.
    #     """
    if steps <= 0:
        raise ValueError("Steps must be positive")

    S = contract.spot
    K = contract.strike
    T = contract.time_to_maturity
    r = contract.risk_free_rate
    q = contract.dividend_yield
    sigma = contract.volatility

    dt = T / steps
    u = exp(sigma * sqrt(dt))
    d = 1.0 / u
    growth = exp((r - q) * dt)
    p = (growth - d) / (u - d)

    if not (0.0 <= p <= 1.0):
        raise ValueError("Risk-neutral probability is outside [0, 1]")

    discount = exp(-r * dt)

    # Terminal payoffs
    values = []
    for j in range(steps + 1):
        stock_price = S * (u ** j) * (d ** (steps - j))
        if contract.option_type == "call":
            payoff = max(stock_price - K, 0)
        else:
            payoff = max(K - stock_price, 0)
        values.append(payoff)

    # Backward induction
    for i in range(steps - 1, -1, -1):
        next_values = []
        for j in range(i + 1):
            continuation_value = discount * (p * values[j + 1] + (1 - p) * values[j])

            if american:
                stock_price = S * (u ** j) * (d ** (i - j))
                if contract.option_type == "call":
                    exercise_value = max(stock_price - K, 0)
                else:
                    exercise_value = max(K - stock_price, 0)
                next_values.append(max(continuation_value, exercise_value))
            else:
                next_values.append(continuation_value)

        values = next_values
    return values[0]