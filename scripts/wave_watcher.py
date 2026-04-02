import sys
import os
import argparse
import random
import time

# Add the parent directory to the path to import tgi
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from tgi.hilbert import EigenstateEncoder

def main():
    parser = argparse.ArgumentParser(description="Moaziz-TGI Wave Watcher (Hilbert Stratification)")
    parser.add_argument("--asset", type=str, default="BTCUSD", help="Asset name")
    parser.add_argument("--ticks", type=int, default=15, help="Number of ticks to simulate")

    args = parser.parse_args()

    encoder = EigenstateEncoder(asset=args.asset)

    print(f"--- Moaziz-TGI Wave Watcher: {args.asset} ---")
    print("Mapping Discrete Ticks to a Continuous Hilbert Space Wave Function")
    print("-" * 60)

    # Initial price history setup
    for i in range(50):
        encoder.process_tick(65000.0 + random.uniform(-10.0, 10.0), 100.0, 'BUY')

    for i in range(args.ticks):
        side = random.choice(['BUY', 'SELL'])
        volume = random.uniform(500.0, 2000.0)
        price = 65000.0 + random.uniform(-20.0, 20.0)

        analysis = encoder.process_tick(price, volume, side)

        print(f"Tick {i+1}: {side} | Vol: {volume:.2f} | Price: ${price:.2f}")
        print(f"  Core Eigenstate: ${analysis['core_eigenstate']:.2f} (Prob: {analysis['eigenstate_prob']:.4f})")
        print(f"  Market Energy (Turbulence): {analysis['market_energy']:.6f}")
        print(f"  Manifold Status: {analysis['status']}")

        # Display other resonant frequencies
        other_states = [f"${s['price']:.2f}" for s in analysis['eigenstates'][1:]]
        if other_states:
             print(f"  Secondary Resonances: {', '.join(other_states)}")

        if analysis['signal'] == "MATERIALIZE_LIQUIDITY":
             print(f"  [SIGNAL] MATERIALIZE LIQUIDITY at Core Node!")
        print("-" * 30)
        time.sleep(0.05)

    print("-" * 60)
    print("Final Wave Function Analysis (Psi Summary):")
    print(f"  Resolution: {encoder.kernel.resolution} bits")
    print(f"  Price Prediction Node: ${encoder.predict_materialization():.2f}")

if __name__ == "__main__":
    random.seed(42) # Deterministic simulation
    main()
