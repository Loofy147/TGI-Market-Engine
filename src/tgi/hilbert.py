import numpy as np
from typing import Dict, Any, List, Tuple

class HilbertMarketKernel:
    """
    Hilbert Stratification Kernel (k -> infinity).
    Represents the market as a continuous wave function Psi in a Hilbert Space.
    Trades the eigenstates (natural resonant frequencies) of liquidity.
    """
    def __init__(self, resolution: int = 256):
        self.resolution = resolution
        # Psi: Complex wave function over the price-manifold [0, 1]
        # Initial state: Ground state (uniform probability)
        self.psi = np.ones(resolution, dtype=complex) / np.sqrt(resolution)
        self.x = np.linspace(0, 1, resolution)
        self.history = []

    def apply_operator(self, price: float, volume: float, side: str):
        """
        Applies a position operator (price) and energy operator (volume)
        to the wave function.
        """
        # Map price to [0, 1] range based on local history
        self.history.append(price)
        if len(self.history) > 100:
            self.history.pop(0)

        p_min, p_max = min(self.history), max(self.history)
        p_range = p_max - p_min if p_max > p_min else 1.0
        normalized_p = (price - p_min) / p_range

        # Position index
        idx = int(normalized_p * (self.resolution - 1))

        # Gaussian perturbation: Volume acts as a weight on the wave function
        # Buy: Increases amplitude (constructive interference)
        # Sell: Decreases amplitude/shifts phase (destructive interference)
        width = 0.05 * self.resolution
        gauss = np.exp(-0.5 * ((np.arange(self.resolution) - idx) / width)**2)

        strength = volume / 1000.0
        phase_shift = np.pi / 4 if side.upper() == 'BUY' else -np.pi / 4

        # Wave function evolution: Psi_new = normalize(Psi + interaction)
        interaction = strength * gauss * np.exp(1j * phase_shift)
        self.psi += interaction
        self.psi /= np.linalg.norm(self.psi)

    def calculate_eigenstates(self) -> List[Dict[str, Any]]:
        """
        Identifies the high-probability eigenstates (resonant frequencies).
        The market 'materializes' liquidity at these exact nodes.
        """
        # Probability density |Psi|^2
        prob_density = np.abs(self.psi)**2

        # Find all local maxima (including boundaries)
        eigenstates = []
        p_min, p_max = (min(self.history), max(self.history)) if self.history else (0.0, 1.0)
        p_range = p_max - p_min if p_max > p_min else 1.0

        for i in range(self.resolution):
            is_peak = True
            if i > 0 and prob_density[i] < prob_density[i-1]:
                is_peak = False
            if i < self.resolution - 1 and prob_density[i] < prob_density[i+1]:
                is_peak = False

            if is_peak:
                price_val = self.x[i] * p_range + p_min
                eigenstates.append({
                    "price": round(float(price_val), 4),
                    "probability": round(float(prob_density[i]), 6),
                    "index": i
                })

        # Sort by probability (strength of the eigenstate)
        eigenstates.sort(key=lambda x: x['probability'], reverse=True)
        return eigenstates

    def get_market_energy(self) -> float:
        """
        Calculates the expectation value of the Hamiltonian (simplified).
        High energy = High turbulence / volatility.
        """
        # Energy E = - Sum( Psi* * d^2/dx^2 Psi )
        d2_psi = np.gradient(np.gradient(self.psi))
        energy = -np.sum(np.conj(self.psi) * d2_psi).real
        return float(energy)


class EigenstateEncoder:
    """
    Encoder for the Hilbert Stratification: Maps discrete tick streams
    into a continuous wave function and identifies 'Zero-Energy' nodes.
    """
    def __init__(self, asset: str = "BTCUSD", resolution: int = 256):
        self.asset = asset
        self.kernel = HilbertMarketKernel(resolution=resolution)

    def process_tick(self, price: float, volume: float, side: str) -> Dict[str, Any]:
        """
        Maps [Price, Volume, Side] into the wave function Psi.
        """
        # Evolve the wave function based on tick interaction
        self.kernel.apply_operator(price, volume, side)

        # Calculate resulting eigenstates and energy
        eigenstates = self.kernel.calculate_eigenstates()
        energy = self.kernel.get_market_energy()

        # Identify the most probable eigenstate (The Core Node)
        core_node = eigenstates[0] if eigenstates else {"price": price, "probability": 1.0}

        # Logic: If energy > 0.5, the wave is highly turbulent (Regime Shift)
        # If energy < 0.1, the wave is in a stable eigenstate (Laminar Flow)
        status = "STABLE_EIGENSTATE" if energy < 0.1 else "HIGH_ENERGY_TURBULENCE"
        if energy > 0.5:
            status = "WAVE_PHASE_SHIFT"

        return {
            "asset": self.asset,
            "current_price": price,
            "core_eigenstate": core_node['price'],
            "eigenstate_prob": core_node['probability'],
            "market_energy": round(energy, 6),
            "status": status,
            "eigenstates": eigenstates[:3], # Top 3 resonant frequencies
            "signal": "MATERIALIZE_LIQUIDITY" if status != "WAVE_PHASE_SHIFT" else "ABSORB_VARIANCE"
        }

    def predict_materialization(self) -> float:
        """
        Returns the exact price where the wave function dictates liquidity
        must exist (the highest amplitude node).
        """
        eigenstates = self.kernel.calculate_eigenstates()
        return eigenstates[0]['price'] if eigenstates else 0.0
