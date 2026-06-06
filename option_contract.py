from dataclasses import dataclass
from typing import Literal

OptionType = Literal["call", "put"]

@dataclass(frozen=True)
class OptionContract:
    spot: float  # S
    strike: float  # K
    volatility: float  # sigma
    time_to_maturity: float  # T
    risk_free_rate: float  # r
    dividend_yield: float = 0.0  # q
    option_type: OptionType = "call"

    def validate(self) -> None:
        if self.spot <= 0:
            raise ValueError("Spot must be positive")
        if self.strike <= 0:
            raise ValueError("Strike must be positive")
        if self.volatility <= 0:
            raise ValueError("Volatility must be positive")
        if self.time_to_maturity <= 0:
            raise ValueError("Time to maturity must be positive")
        if self.option_type not in ["call", "put"]:
            raise ValueError("Option type must be 'call' or 'put'")

