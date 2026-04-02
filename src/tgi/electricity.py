import math
from typing import Dict, Any, List

class ElectricityEngine:
    """
    Moaziz-TGI Execution Layer: The Electricity Parity Algorithm.
    Trades Symmetry Breaks rather than price patterns.
    """
    def __init__(self, m: int = 256, k: int = 2):
        self.m = m
        self.k = k  # Precision constant (e.g., 2 for Gold)
        self.weights = {
            "15m": 0.5,
            "5m": 0.3,
            "1m": 0.2
        }

    def map_price_to_residue(self, price: float) -> int:
        """
        Maps price to a residue modulo m: R_t = floor(P_t * 10^k) mod m
        """
        return math.floor(price * (10 ** self.k)) % self.m

    def calculate_distance_to_obstruction(self, residues: Dict[str, int]) -> float:
        """
        Calculates D_Omega = sum(w_t * gcd(R_t, m) / m)
        """
        d_omega = 0.0
        for tf, weight in self.weights.items():
            r_t = residues.get(tf, 0)
            gcd_val = math.gcd(r_t, self.m)
            d_omega += weight * (gcd_val / self.m)
        return d_omega

    def get_manifold_state(self, d_omega: float) -> str:
        """
        Maps D_Omega to manifold state.
        """
        if d_omega <= 0.05:
            return "Harmonious (Coprime)"
        elif d_omega <= 0.15:
            return "Torsion (Friction)"
        else:
            return "Singularity (Obstructed)"

    def get_trade_action(self, d_omega: float, residues: Dict[str, int]) -> str:
        """
        Deduces trade action based on D_Omega and execution protocols.
        """
        # Protocol 1: The Trapdoor (Exit)
        # If gcd(R1, m) >= m/8, exit immediately.
        r1 = residues.get("1m", 0)
        if math.gcd(r1, self.m) >= (self.m // 8):
            return "IMMEDIATE EXIT (Trapdoor Snapped)"

        # Protocol 2: The Logic Gate
        if d_omega > 0.20:
            return "IMMEDIATE EXIT / REVERSE"
        elif d_omega > 0.05:
            return "Tighten Stops"
        else:
            return "Hold/Trend Follow"

    def analyze(self, prices: Dict[str, float]) -> Dict[str, Any]:
        """
        Performs full topological analysis for a set of timeframe prices.
        """
        residues = {tf: self.map_price_to_residue(p) for tf, p in prices.items()}
        d_omega = self.calculate_distance_to_obstruction(residues)
        state = self.get_manifold_state(d_omega)
        action = self.get_trade_action(d_omega, residues)

        # Sniping Zone Check (gcd(R, m) == m means R % m == 0)
        is_sniping_zone = any(math.gcd(r, self.m) == self.m for r in residues.values())

        # Coordinated Reset Check
        all_coprime = all(math.gcd(r, self.m) == 1 for r in residues.values())

        return {
            "residues": residues,
            "d_omega": round(d_omega, 4),
            "state": state,
            "action": action,
            "is_sniping_zone": is_sniping_zone,
            "all_coprime": all_coprime
        }
