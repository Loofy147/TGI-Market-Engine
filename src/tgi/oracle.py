import numpy as np
from .kernel import TGIMarketKernel

class MarketOracle:
    """
    Execution Adapter for the Moaziz System.
    Links the TGI Kernel to live market feeds.
    """
    def __init__(self):
        # Initialize manifolds for primary assets
        self.kernels = {
            "BTC": TGIMarketKernel("BTC", m=64),
            "GOLD": TGIMarketKernel("GOLD", m=256)
        }

    def process_market_tick(self, asset: str, raw_data: dict):
        """
        Processes a single tick through the manifold.
        raw_data keys: 'price_delta', 'vol', 'flow', 'time'
        """
        kernel = self.kernels.get(asset)
        if not kernel:
            raise ValueError(f"No manifold defined for {asset}")

        # Vectorize features
        features = np.array([
            raw_data['price_delta'],
            raw_data['vol'],
            raw_data['flow'],
            raw_data['time']
        ])

        # Execute Topological Deduction
        analysis = kernel.analyze_topology(features)

        # 3. Apply Closure Lemma (k-1 Reduction)
        # If status is collapse, we solve for hidden flow (r3) to observe weight
        if analysis['status'] == "H2_OBSTRUCTION_COLLAPSE":
            # Algebraic inference of hidden liquidity weight to reach sum mod m == 0
            # (current_sum + hidden) % m = 0 -> hidden = (m - current_sum) % m
            # coordinates are [r1, r2, r3, r4]
            coords = analysis['coordinates']
            current_sum_minus_r3 = (sum(coords) - coords[2]) % kernel.m
            hidden_weight = (kernel.m - current_sum_minus_r3) % kernel.m
            analysis['hidden_flow_detected'] = int(hidden_weight)

        return analysis

    def multi_timeframe_sync(self, asset: str, data_1m, data_5m, data_15m):
        """
        Verifies parity alignment across three temporal fibers.
        """
        t1 = self.process_market_tick(asset, data_1m)
        t5 = self.process_market_tick(asset, data_5m)
        t15 = self.process_market_tick(asset, data_15m)

        # Systemic Signal: Only act if 1m and 15m status are aligned
        is_aligned = (t1['status'] == t15['status'])

        return {
            "asset": asset,
            "aligned": is_aligned,
            "m1": t1['status'],
            "m5": t5['status'],
            "m15": t15['status'],
            "final_action": t1['signal'] if is_aligned else "WAIT"
        }
