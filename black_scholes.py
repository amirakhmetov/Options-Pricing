from option_contract import OptionContract
from normal_dist import normal_pdf, normal_cdf
from math import sqrt, exp, log

def d1(contract: OptionContract) -> float:
    contract.validate()
    S = contract.spot
    K = contract.strike
    sigma = contract.volatility
    r = contract.risk_free_rate
    T = contract.time_to_maturity
    q = contract.dividend_yield
    return (log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))


def d2(contract: OptionContract) -> float:
    return d1(contract) - contract.volatility * sqrt(contract.time_to_maturity)


def black_scholes_price(contract: OptionContract) -> float:
    contract.validate()
    S = contract.spot
    K = contract.strike
    r = contract.risk_free_rate
    T = contract.time_to_maturity
    q = contract.dividend_yield
    D1 = d1(contract)
    D2 = d2(contract)

    if contract.option_type == "call":
        return S * exp(-q * T) * normal_cdf(D1) - K * exp(-r * T) * normal_cdf(D2)
    return K * exp(-r * T) * normal_cdf(-D2) - S * exp(-q * T) * normal_cdf(-D1)


def greeks(contract: OptionContract) -> float:
    #     Notes:
    #     - Vega is price change for a 1.00 change in volatility.
    #       Divide by 100 if you want price change per 1 volatility point.
    #     - Theta is annualized.
    #     - Rho is price change for a 1.00 change in the risk-free rate.
    #       Divide by 100 if you want price change per 1 percentage point.

    contract.validate()
    S = contract.spot
    K = contract.strike
    sigma = contract.volatility
    r = contract.risk_free_rate
    T = contract.time_to_maturity
    q = contract.dividend_yield
    D1 = d1(contract)
    D2 = d2(contract)

    discount_q = exp(-q * T)
    discount_r = exp(-r * T)

    gamma = discount_q * normal_pdf(D1) / (S * sigma * sqrt(T))
    vega = S * discount_q * normal_pdf(D1) * sqrt(T)

    if contract.option_type == "call":
        delta = discount_q * normal_cdf(D1)
        theta = (-S * discount_q * normal_pdf(D1) * sigma / (2 * sqrt(T)) - r * K * discount_r * normal_cdf(
            D2) + q * S * discount_q * normal_cdf(D1))
        rho = K * T * discount_r * normal_cdf(D2)
    else:
        delta = -discount_q * normal_cdf(-D1)
        theta = (-S * discount_q * normal_pdf(D1) * sigma / (2 * sqrt(T)) + r * K * discount_r * normal_cdf(
            -D2) - q * S * discount_q * normal_cdf(-D1))
        rho = -K * T * discount_r * normal_cdf(-D2)

    return {
        "delta": delta,
        "gamma": gamma,
        "vega": vega,
        "theta": theta,
        "rho": rho,
    }