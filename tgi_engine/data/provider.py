import random
import time
from typing import Dict, Iterator

class TickDataProvider:
    """
    Simulates 1-second BTC/USD tick data.
    Provides price delta, volume acceleration, liquidity imbalance, and volatility.
    """
    def __init__(self, base_price: float = 65000.0):
        self.price = base_price
        self.vol_accel = 100.0
        self.liq_imbalance = 0.0
        self.volatility = 0.02

    def get_tick(self) -> Dict:
        """
        Generates a single tick with randomized movement.
        """
        # Price Delta: -10 to +10
        price_delta = random.uniform(-10.0, 10.0)
        self.price += price_delta

        # Vol Accel: 50 to 500
        self.vol_accel = random.uniform(50.0, 500.0)

        # Liq Imbalance: -1.0 to 1.0 (delta between bid/ask depth)
        self.liq_imbalance = random.uniform(-1.0, 1.0)

        # Volatility: 0.01 to 0.1
        self.volatility = random.uniform(0.01, 0.1)

        return {
            "price_delta": price_delta,
            "vol_accel": self.vol_accel,
            "liq_imbalance": self.liq_imbalance,
            "volatility": self.volatility,
            "current_price": self.price
        }

    def stream_ticks(self, interval: float = 1.0) -> Iterator[Dict]:
        """
        Generator for a stream of ticks.
        """
        while True:
            yield self.get_tick()
            time.sleep(interval)
