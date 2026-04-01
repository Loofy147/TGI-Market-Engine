import numpy as np

class BTCTopologicalEncoder:
    """
    Projecting BTC Market Dynamics into the Z_64^4 Manifold.
    Uses Locality Sensitive Hashing (LSH) to preserve market symmetry.
    """
    def __init__(self, m: int = 64):
        self.m = m
        # Deterministic seed for reproducibility in testing
        np.random.seed(42)
        # Projection vectors for the 4 dimensions
        self.projection_matrix = np.random.randn(4, 4)

    def encode_tick(self, price_delta: float, vol_velocity: float, flow_imbalance: float, time_decay: float) -> tuple:
        """
        Encodes a BTC tick into the 4-dimensional residue vector (r1, r2, r3, r4).
        """
        # 1. Normalize and Vectorize
        raw_state = np.array([price_delta, vol_velocity, flow_imbalance, time_decay])

        # 2. Symmetry-Preserving Transform
        # Projecting semantic market features onto the manifold coordinates
        projected = np.dot(self.projection_matrix, raw_state)

        # 3. Discretization into the Z_m^4 Torus
        # Each coordinate must be an integer in [0, m-1]
        # We use a scaling factor to ensure we capture nuance before modulus
        coords = np.mod(np.floor(projected * 10).astype(int), self.m)

        # Convert to tuple for hashability/immutability
        residues = tuple(coords.tolist())

        # 4. Global Parity
        parity_sum = sum(residues) % self.m

        return residues, parity_sum
