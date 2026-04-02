import sys
import os
import random
import math

# Add the parent directory to the path to import tgi
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from tgi.non_commutative import TwistedFiberEncoder

def main():
    print("--- Moaziz-TGI Twisted Fiber Backtest ---")
    print("Strategy: Front-running Structural Snaps via Holonomy Accumulation")
    print("-" * 60)

    # Simulation setup
    encoder = TwistedFiberEncoder(asset="XAUUSD")
    start_price = 2700.0

    position = 0 # Flat
    entry_price = 0.0
    pnl = 0.0
    trades = 0
    snaps_detected = 0

    # Backtest for 200 ticks
    for i in range(200):
        # We simulate "Twisted Order Flow":
        # Sequences of large institutional accumulation followed by retail selling
        if i % 10 < 5:
            side = 'BUY'
            volume = 1200.0 # Institutional accumulation (upper triangular)
            price = start_price + (i * 0.1) # Small price upward pressure
        else:
            side = 'SELL'
            volume = 400.0 # Retail selling (lower triangular)
            price = start_price + (i * 0.1) - random.uniform(0.1, 0.5)

        analysis = encoder.process_tick(price, volume, side)

        # 1. Trading Logic based on Structural Status
        if position == 0:
            if analysis['signal'] == "FRONT_RUN":
                # Enter Long on structural snap imminent
                position = 1
                entry_price = price
                snaps_detected += 1
                print(f"[{i+1}] FRONT-RUN LONG at ${entry_price:.2f} | Holonomy: {analysis['holonomy']:.6f}")
        elif position == 1:
            # Simple take profit on price expansion (structural reset simulated)
            if price - entry_price > 2.0:
                exit_price = price
                trade_pnl = exit_price - entry_price
                pnl += trade_pnl
                trades += 1
                print(f"[{i+1}] TAKE PROFIT at ${exit_price:.2f} | PnL: ${trade_pnl:.2f}")
                position = 0
                encoder.kernel.reset() # Reset manifold after structural snap
            elif price - entry_price < -5.0:
                # Stop loss
                exit_price = price
                trade_pnl = exit_price - entry_price
                pnl += trade_pnl
                trades += 1
                print(f"[{i+1}] STOP LOSS at ${exit_price:.2f} | PnL: ${trade_pnl:.2f}")
                position = 0
                encoder.kernel.reset()

    print("-" * 60)
    print("Backtest Results (Twisted Fiber):")
    print(f"Total Trades: {trades}")
    print(f"Total PnL: ${pnl:.2f}")
    print(f"Structural Snaps Front-Run: {snaps_detected}")

if __name__ == "__main__":
    random.seed(42)
    main()
