import sys
import os

# Add the parent directory to the path to import tgi_engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tgi_engine.core.encoder import BTCTopologicalEncoder
from tgi_engine.core.engine import TGIMarketEngine
from tgi_engine.data.provider import TickDataProvider

def main():
    m = 64
    encoder = BTCTopologicalEncoder(m=m)
    engine = TGIMarketEngine(m=m)
    provider = TickDataProvider(base_price=65000.0)

    print(f"--- BTC Topological Backtest Simulation ---")
    print(f"Asset: BTC/USD | Modulus m: {m} (Thin Fibers)")

    # Simulate a volatility spike (10 steps)
    print("\n--- Phase 1: Volatility Breakout (Price 5k -> 0k) ---")
    for i, tick in enumerate(provider.simulate_volatility_spike(10)):
        residues, parity = encoder.encode_tick(
            tick['price_delta'],
            tick['vol_velocity'],
            tick['flow_imbalance'],
            tick['time_decay']
        )

        protected = engine.check_topological_protection(residues)
        status = engine.detect_h2_obstruction(residues)

        print(f"Step {i+1}: Price: ${tick['current_price']:.2f}")
        print(f"  Residues: {residues} | Parity S: {status['parity_residue']}")
        print(f"  Status: {status['status']} | Protected: {protected}")
        if status['is_obstructed']:
            print(f"  [SIGNAL] H2 Parity Wall Detected - Trend Potential Reversal")
        elif protected:
            print(f"  [SIGNAL] Topological Protection - Trend Locked")
        print("-" * 25)

    # Phase 2: Closure Lemma Check for Hidden Orders
    print("\n--- Phase 2: Closure Lemma Analysis (Hidden Liquidity) ---")
    # r1 (Momentum), r2 (Velocity), r4 (Time)
    r1, r2, r4 = 17, 43, 21
    r3_hidden = engine.solve_closure_lemma(r1, r2, r4)
    print(f"Observed r1={r1}, r2={r2}, r4={r4} -> Deduced r3 (Hidden Order Flow): {r3_hidden}")
    print(f"Full Manifold Vector: {(r1, r2, r3_hidden, r4)} (Sum mod 64 = 0)")

if __name__ == "__main__":
    main()
