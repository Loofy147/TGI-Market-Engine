import sys
import os
import time
import argparse

# Add the parent directory to the path to import tgi
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from tgi.electricity import ElectricityEngine

def main():
    parser = argparse.ArgumentParser(description="Moaziz-TGI Residue Watcher Script")
    parser.add_argument("--asset", type=str, default="BTC", help="Asset name (BTC or Gold)")
    parser.add_argument("--m", type=int, default=256, help="Modulus m")
    parser.add_argument("--k", type=int, default=2, help="Precision constant k")
    parser.add_argument("--p15m", type=float, required=True, help="15m timeframe price")
    parser.add_argument("--p5m", type=float, required=True, help="5m timeframe price")
    parser.add_argument("--p1m", type=float, required=True, help="1m timeframe price")

    args = parser.parse_args()

    engine = ElectricityEngine(m=args.m, k=args.k)
    prices = {
        "15m": args.p15m,
        "5m": args.p5m,
        "1m": args.p1m
    }

    print(f"--- Moaziz-TGI Residue Watcher: {args.asset} ---")
    print(f"Modulus m: {args.m} | Precision k: {args.k}")
    print("-" * 40)

    analysis = engine.analyze(prices)

    print(f"Timeframe Prices: {prices}")
    print(f"Topological Residues: {analysis['residues']}")
    print(f"Distance to Obstruction (D_Omega): {analysis['d_omega']}")
    print(f"Manifold State: {analysis['state']}")
    print("-" * 40)
    print(f"SIGNAL: {analysis['action']}")

    if analysis['is_sniping_zone']:
        print("[!] SNIPING ZONE: Potential Symmetry Break at Parity Wall.")

    if analysis['all_coprime']:
        print("[+] COORDINATED RESET: Manifold is clear for entry.")
    elif analysis['action'] == "Hold/Trend Follow":
         print("[*] HARMONIOUS: Trend protected by coprimality.")

if __name__ == "__main__":
    main()
