import sys
import os
import argparse
import random
import time

# Add the parent directory to the path to import tgi
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from tgi.non_commutative import TwistedFiberEncoder

def main():
    parser = argparse.ArgumentParser(description="Moaziz-TGI Holonomy Watcher (Twisted Fiber)")
    parser.add_argument("--asset", type=str, default="XAUUSD", help="Asset name")
    parser.add_argument("--ticks", type=int, default=10, help="Number of ticks to simulate")

    args = parser.parse_args()

    encoder = TwistedFiberEncoder(asset=args.asset)

    print(f"--- Moaziz-TGI Holonomy Watcher: {args.asset} ---")
    print("Mapping Tick Streams to SL(2, R) Non-Commutative State Space")
    print("-" * 60)

    # Simulate a "Hidden Accumulation" scenario:
    # High volume fragmented buying, low volume retail selling.
    # We'll simulate a loop of 1000 buy then 1000 sell volume
    # across multiple ticks.

    start_price = 2745.0

    for i in range(args.ticks):
        # Randomize side and volume
        side = random.choice(['BUY', 'SELL'])
        volume = random.uniform(100.0, 1500.0)
        price = start_price + random.uniform(-0.5, 0.5)

        analysis = encoder.process_tick(price, volume, side)

        print(f"Tick {i+1}: {side} | Vol: {volume:.2f} | Price: ${price:.2f}")
        print(f"  Holonomy (The Twist): {analysis['holonomy']:.6f}")
        print(f"  Structural Status: {analysis['status']}")
        if analysis['signal'] == "FRONT_RUN":
            print(f"  [SIGNAL] FRONT_RUN: Structural snap imminent!")
        print("-" * 30)
        time.sleep(0.1)

    print("-" * 60)
    print("Final Manifold Coordinates (Matrix State):")
    for row in analysis['matrix_state']:
        print(f"  {row}")

if __name__ == "__main__":
    random.seed(42) # Deterministic simulation
    main()
