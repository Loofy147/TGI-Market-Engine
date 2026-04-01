import math
from typing import Tuple, Dict, List

class TGIMarketEngine:
    """
    Core engine that implements Parity Harmony, H^2 Parity Obstruction,
    and the Closure Lemma for BTC/USD markets (m=64).
    """
    def __init__(self, m: int = 64):
        self.m = m

    def check_topological_protection(self, residues: Tuple[int, int, int, int]) -> bool:
        """
        Determines if a trend is topologically protected (Trend Following).
        Conditions:
          1. Sum mod m satisfies parity (Sum mod m = S, where gcd(S, m) = 1)
          2. Each residue is coprime to m.
        Note: The user described harmony as gcd(Sum, m) = 1 for 'Bull Signal'.
        """
        r1, r2, r3, r4 = residues

        # Parity condition for protection: Sum mod m is coprime to m
        total_sum = sum(residues)
        S = total_sum % self.m
        parity_protected = (math.gcd(S, self.m) == 1)

        # Coprimality condition for each coordinate
        coprimality_check = all(math.gcd(ri, self.m) == 1 for ri in residues)

        return parity_protected and coprimality_check

    def detect_h2_obstruction(self, residues: Tuple[int, int, int, int]) -> Dict:
        """
        Checks for a 'Parity Wall' (Reversal Signal).
        When sum of residues starts diverging from required parity or
        loses coprimality with m.
        """
        r1, r2, r3, r4 = residues
        total_sum = sum(residues)
        S = total_sum % self.m

        # A wall is hit when coprimality with m is lost or S == 0 (Closure point reached)
        coprimality_lost = any(math.gcd(ri, self.m) != 1 for ri in residues)
        parity_wall = (S == 0)

        is_obstructed = coprimality_lost or parity_wall

        return {
            "is_obstructed": is_obstructed,
            "parity_residue": S,
            "status": "PARITY_WALL" if is_obstructed else "TOPOLOGICAL_HARMONY"
        }

    def solve_closure_lemma(self, r1: int, r2: int, r4: int) -> int:
        """
        Algebraically deduces the missing dimension r3 (Hidden Liquidity)
        to satisfy the Closure Lemma (sum mod m == 0).
        """
        # (r1 + r2 + r3 + r4) % m = 0
        current_sum = (r1 + r2 + r4) % self.m
        r3 = (self.m - current_sum) % self.m
        return r3
