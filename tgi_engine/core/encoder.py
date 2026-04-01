import math

class LSHEncoder:
    """
    Projects live tick data onto the Z_m^4 Torus.
    Quantizes continuous market signals into discrete residues r_1, r_2, r_3, r_4.
    """
    def __init__(self, m: int = 1024):
        self.m = m

    def quantize(self, value: float, min_val: float, max_val: float) -> int:
        """
        Maps a continuous value to a residue r in [0, m-1].
        """
        if max_val == min_val:
            return 0

        # Normalize to [0, 1]
        normalized = (value - min_val) / (max_val - min_val)
        normalized = max(0.0, min(1.0, normalized))

        # Scale to [0, m-1]
        residue = int(round(normalized * (self.m - 1)))
        return residue % self.m

    def encode_tick(self, price_delta: float, vol_accel: float, liq_imbalance: float, volatility: float,
                    ranges: dict) -> tuple:
        """
        Encodes a single tick into the 4-dimensional residue vector (r1, r2, r3, r4).
        'ranges' should provide (min, max) for each dimension for normalization.
        """
        r1 = self.quantize(price_delta, *ranges['price_delta'])
        r2 = self.quantize(vol_accel, *ranges['vol_accel'])
        r3 = self.quantize(liq_imbalance, *ranges['liq_imbalance'])
        r4 = self.quantize(volatility, *ranges['volatility'])

        return (r1, r2, r3, r4)
