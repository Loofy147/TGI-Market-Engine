import sys
import os
import random
import math

# Add the parent directory to the path to import tgi
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from tgi.hilbert import EigenstateEncoder

def main():
    print("--- Moaziz-TGI Hilbert Stratification Backtest ---")
    print("Strategy: Liquidity Materialization at Wave Function Nodes")
    print("-" * 60)

    # Simulation setup
    encoder = EigenstateEncoder(asset="BTCUSD", resolution=512)
    start_price = 65000.0

    # Pre-fill history to establish baseline manifold
    for i in range(100):
        encoder.process_tick(start_price + random.uniform(-50.0, 50.0), 100.0, 'BUY')

    position = 0 # Flat
    entry_price = 0.0
    pnl = 0.0
    trades = 0
    energy_alerts = 0

    # Backtest for 150 ticks
    for i in range(150):
        # We simulate "Wave Market":
        # Price fluctuates around natural resonant nodes
        price = start_price + 20.0 * math.sin(i * 0.1) + random.uniform(-2.0, 2.0)
        volume = random.uniform(500.0, 1500.0)
        side = 'BUY' if random.random() > 0.4 else 'SELL'

        analysis = encoder.process_tick(price, volume, side)

        # 1. Trading Logic based on Eigenstate Materialization
        if position == 0:
            # We "materialize" liquidity at the core node if probability is high (> 0.02)
            # and market energy is low (Laminar Flow)
            if analysis['eigenstate_prob'] > 0.02 and analysis['status'] == "STABLE_EIGENSTATE":
                # We place a limit order exactly at the resonant node
                limit_price = analysis['core_eigenstate']

                # Check if price hits the node (simplified)
                if abs(price - limit_price) < 1.0:
                    position = 1
                    entry_price = price
                    print(f"[{i+1}] MATERIALIZE LONG at Node: ${limit_price:.2f} | Prob: {analysis['eigenstate_prob']:.4f}")

        elif position == 1:
            # Simple take profit on price expansion or phase shift out
            if price - entry_price > 15.0:
                out_price = price
                trade_pnl = out_price - entry_price
                pnl += trade_pnl
                trades += 1
                print(f"[{i+1}] TAKE PROFIT at ${out_price:.2f} | PnL: ${trade_pnl:.2f}")
                position = 0
            elif analysis['status'] == "WAVE_PHASE_SHIFT":
                # Phase shift detected: manifold is breaking; out immediately
                out_price = price
                trade_pnl = out_price - entry_price
                pnl += trade_pnl
                trades += 1
                energy_alerts += 1
                print(f"[{i+1}] PHASE SHIFT OUT at ${out_price:.2f} | PnL: ${trade_pnl:.2f} | Energy: {analysis['market_energy']:.6f}")
                position = 0

    print("-" * 60)
    print("Backtest Results (Hilbert Stratification):")
    print(f"Total Trades: {trades}")
    print(f"Total PnL: ${pnl:.2f}")
    print(f"Wave Phase Shift Outs: {energy_alerts}")

if __name__ == "__main__":
    random.seed(42)
    main()
