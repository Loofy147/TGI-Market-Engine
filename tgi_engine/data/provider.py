import random
import time
from typing import Dict, Iterator

class TickDataProvider:
    """
    Simulates high-velocity BTC/USD tick data for the Z_64^4 Manifold.
    Provides r1-r4 mapped financial proxies.
    """
    def __init__(self, base_price: float = 65000.0):
        self.price = base_price
        self.vol_velocity = 100.0
        self.flow_imbalance = 0.0
        self.time_decay = 0.01

    def get_tick(self) -> Dict:
        """
        Generates a single tick for BTC.
        """
        # Price Delta: -500 to +500 (Volatile range)
        price_delta = random.uniform(-500.0, 500.0)
        self.price += price_delta

        # Vol Velocity: 50 to 1000
        self.vol_velocity = random.uniform(50.0, 1000.0)

        # Flow Imbalance (Bid vs Ask Depth): -1.0 to 1.0
        self.flow_imbalance = random.uniform(-1.0, 1.0)

        # Time Decay/Volatility component: 0.001 to 0.1
        self.time_decay = random.uniform(0.001, 0.1)

        return {
            "price_delta": price_delta,
            "vol_velocity": self.vol_velocity,
            "flow_imbalance": self.flow_imbalance,
            "time_decay": self.time_decay,
            "current_price": self.price
        }

    def simulate_volatility_spike(self, duration: int = 10) -> Iterator[Dict]:
        """
        Simulates a volatility breakout.
        """
        for i in range(duration):
            # Increasingly large price moves and volume velocity
            price_delta = 500.0 + (i * 100.0)
            self.price += price_delta
            yield {
                "price_delta": price_delta,
                "vol_velocity": 1000.0 + (i * 200.0),
                "flow_imbalance": 0.5 + (i * 0.05),
                "time_decay": 0.1 + (i * 0.01),
                "current_price": self.price
            }
