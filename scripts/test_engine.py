import sys
import os
import math

# Add the parent directory to the path to import tgi_engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tgi_engine.core.encoder import LSHEncoder
from tgi_engine.core.engine import TGIMarketEngine
from tgi_engine.data.provider import TickDataProvider

def main():
    m = 1024
    encoder = LSHEncoder(m=m)
    engine = TGIMarketEngine(m=m)
    provider = TickDataProvider()

    # Dynamic ranges for quantization
    ranges = {
        'price_delta': (-10.0, 10.0),
        'vol_accel': (0.0, 500.0),
        'liq_imbalance': (-1.0, 1.0),
        'volatility': (0.0, 0.2)
    }

    print(f"--- TGI Engine Simulation Start ---")
    print(f"Modulus m: {m}")
    print(f"Testing the Closure Lemma first...")

    # Example: Deducing hidden liquidity
    r1, r2, r4 = 127, 451, 89
    r3_hidden = engine.solve_closure_lemma(r1, r2, r4)
    print(f"Observed r1={r1}, r2={r2}, r4={r4} -> Deduced r3 (Hidden Liquidity): {r3_hidden}")

    # Verify parity
    is_harmonious = engine.check_parity_harmony((r1, r2, r3_hidden, r4))
    print(f"Parity Check (Coprimality may fail if r1, r2, r4 aren't coprime): {is_harmonious}")

    print("\n--- Running Live Tick Simulation (10 ticks) ---")
    for i in range(10):
        tick = provider.get_tick()
        residues = encoder.encode_tick(
            tick['price_delta'],
            tick['vol_accel'],
            tick['liq_imbalance'],
            tick['volatility'],
            ranges
        )

        status = engine.detect_h2_obstruction(residues)

        print(f"Tick {i+1}: Price: ${tick['current_price']:.2f}")
        print(f"  Residues: {residues}")
        print(f"  Topological Status: {status['status']}")
        if status['is_obstructed']:
            print(f"  Obstructions: {status['violations']}")
        print("-" * 20)

if __name__ == "__main__":
    main()
