import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

# Ensure 'src' is in the path
sys.path.append('src')

from tgi.kernel import TGIMarketKernel
from tgi.batch_processor import TGIBatchMapper

def generate_historical_data(asset: str, rows: int = 10000):
    """
    Generates synthetic historical data for BTC or GOLD.
    """
    print(f"Generating {rows} historical rows for {asset}...")
    np.random.seed(42 if asset == "BTC" else 24)

    data = {
        'price_delta': np.random.normal(0, 50, rows),
        'vol': np.random.uniform(100, 5000, rows),
        'flow': np.random.uniform(-1, 1, rows),
        'time': np.random.uniform(0.001, 0.1, rows)
    }

    # Simulate some structured 'liquidity traps' (repeated coords)
    if asset == "BTC":
        # Force some H2 obstructions
        data['price_delta'][100:150] = 500.0
        data['vol'][100:150] = 2000.0
        data['flow'][100:150] = 0.8

    df = pd.DataFrame(data)
    file_name = f"data_{asset.lower()}_historical.parquet"
    df.to_parquet(file_name)
    return file_name

def main():
    # 1. Generate BTC and GOLD historical archives
    btc_file = generate_historical_data("BTC", 5000)
    gold_file = generate_historical_data("GOLD", 5000)

    assets = [
        ("BTC", 64, btc_file),
        ("GOLD", 256, gold_file)
    ]

    print("\n--- TGI Topological Archaeologist Report ---")
    print(f"Timestamp: {datetime.now().isoformat()}\n")

    for asset_name, m, file_path in assets:
        kernel = TGIMarketKernel(asset_name, m=m)
        mapper = TGIBatchMapper(kernel)

        # Load and Process
        df = mapper.load_data(file_path)
        feature_cols = ['price_delta', 'vol', 'flow', 'time']
        mapper.process_batch(df, feature_cols)

        # Results
        density = mapper.calculate_empirical_truth_density()
        anchors = mapper.identify_multi_year_parity_anchors(threshold=5)
        backtest = mapper.backtest_closure_lemma_accuracy(df, feature_cols)
        refinement = mapper.refine_modulus_m()

        print(f"Asset: {asset_name} (m={m})")
        print(f"  - Empirical Truth Density (Nb): {density:.6f}")
        print(f"  - Multi-Year Parity Anchors: {len(anchors)} detected")
        if anchors:
            print(f"    Sample Anchor: {anchors[0]['coordinate']} (Freq: {anchors[0]['frequency']})")
        print(f"  - Closure Lemma Accuracy: {backtest['accuracy_pct']:.2f}% ({backtest['interpretation']})")
        print(f"  - Modulus Refinement: {refinement['regime_shift']} -> Suggested m: {refinement['suggested_m']}")
        print("-" * 40)

if __name__ == "__main__":
    main()
