from math import exp, erf, sqrt, pi


def normal_pdf(x: float) -> float:
    return exp(-0.5 * x ** 2) / sqrt(2 * pi)


def normal_cdf(x: float) -> float:
    return 0.5 * (1 + erf(x / sqrt(2)))