import sys
import os
import random
import math

# Add the parent directory to the path to import tgi
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from tgi.electricity import ElectricityEngine

class SimpleTickProvider:
    """
    Mock tick data generator for backtesting.
    """
    def __init__(self, start_price: float = 65000.0, step: float = 0.5):
        self.price = start_price
        self.step = step

    def get_tick(self) -> float:
        # Random walk price movement
        self.price += random.uniform(-self.step, self.step)
        return self.price

def main():
    m = 256
    k = 2
    engine = ElectricityEngine(m=m, k=k)
    provider = SimpleTickProvider(start_price=65000.0, step=1.0)

    print(f"--- Moaziz-TGI Electricity Backtest ---")
    print(f"Modulus m: {m} | Precision k: {k}")
    print("-" * 50)

    # Simulation state
    position = 0 # 0: Flat, 1: Long, -1: Short
    entry_price = 0.0
    pnl = 0.0
    trades = 0
    trapdoor_exits = 0
    sniping_wins = 0

    # Backtest for 100 ticks
    for i in range(100):
        # Simulate three timeframes (rudder, sail, hull)
        # For simplicity, we use the same price for all timeframes in the backtest
        # but with slightly different jitter to simulate fiber dispersion.
        current_price = provider.get_tick()
        prices = {
            "1m": current_price,
            "5m": current_price + random.uniform(-0.1, 0.1),
            "15m": current_price + random.uniform(-0.5, 0.5)
        }

        analysis = engine.analyze(prices)
        action = analysis["action"]

        # 1. Check Exit Conditions
        if position != 0:
            if "IMMEDIATE EXIT" in action:
                # Close trade
                exit_price = current_price
                trade_pnl = (exit_price - entry_price) if position == 1 else (entry_price - exit_price)
                pnl += trade_pnl
                print(f"[{i+1}] EXIT {('LONG' if position == 1 else 'SHORT')} at ${exit_price:.2f} | PnL: ${trade_pnl:.2f} | Reason: {action}")
                position = 0
                trades += 1
                if "Trapdoor" in action:
                    trapdoor_exits += 1

        # 2. Check Entry Conditions (Sniping Parity Walls)
        if position == 0:
            lower_wall, upper_wall = analysis["parity_walls"]
            sniping_levels = analysis["sniping_levels"]

            # Logic: If price is within 0.5 of a wall, we snipe a bounce
            if abs(current_price - sniping_levels["lower"]) < 0.2:
                # Snipe Long off lower wall
                position = 1
                entry_price = current_price
                print(f"[{i+1}] SNIPE LONG at ${entry_price:.2f} (Lower Wall: ${lower_wall:.2f})")
                sniping_wins += 1
            elif abs(current_price - sniping_levels["upper"]) < 0.2:
                # Snipe Short off upper wall
                position = -1
                entry_price = current_price
                print(f"[{i+1}] SNIPE SHORT at ${entry_price:.2f} (Upper Wall: ${upper_wall:.2f})")
                sniping_wins += 1
            elif analysis["all_coprime"]:
                # Coordinated Reset Entry
                # For simulation, we'll go with the 15m trend (simplified)
                position = 1
                entry_price = current_price
                print(f"[{i+1}] HARMONIOUS ENTRY: LONG at ${entry_price:.2f} | D_Omega: {analysis['d_omega']}")

    print("-" * 50)
    print(f"Backtest Results:")
    print(f"Total Trades: {trades}")
    print(f"Total PnL: ${pnl:.2f}")
    print(f"Trapdoor Exits: {trapdoor_exits}")
    print(f"Sniping Entries: {sniping_wins}")

if __name__ == "__main__":
    random.seed(42) # Deterministic simulation
    main()
