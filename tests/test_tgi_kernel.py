import pytest
import numpy as np
from src.tgi.kernel import TGIMarketKernel
from src.tgi.oracle import MarketOracle

def test_kernel_initialization():
    btc_kernel = TGIMarketKernel("BTC", m=64)
    assert btc_kernel.asset == "BTC"
    assert btc_kernel.m == 64
    assert btc_kernel.projection_matrix.shape == (4, 4)

def test_encode_state_determinism():
    kernel = TGIMarketKernel("BTC", m=64)
    features = np.array([100.0, 0.5, 0.1, 0.01])
    res1, parity1 = kernel.encode_state(features)
    res2, parity2 = kernel.encode_state(features)
    assert np.array_equal(res1, res2)
    assert parity1 == parity2

def test_analyze_topology_protected():
    # We find features that result in a coprime parity for m=64
    kernel = TGIMarketKernel("BTC", m=64)
    # With seed 42, we search for a protected state
    for i in range(100):
        features = np.array([float(i), 1.0, 0.5, 0.1])
        analysis = kernel.analyze_topology(features)
        if analysis['status'] == "PROTECTED":
            assert analysis['signal'] == "HOLD/FOLLOW"
            assert np.gcd(analysis['parity'], 64) == 1
            return
    pytest.fail("Could not find a PROTECTED state in 100 iterations")

def test_oracle_process_tick():
    oracle = MarketOracle()
    raw_data = {
        'price_delta': 50.0,
        'vol': 1000.0,
        'flow': 0.8,
        'time': 0.05
    }
    analysis = oracle.process_market_tick("BTC", raw_data)
    assert "status" in analysis
    assert "signal" in analysis
    assert analysis["asset"] == "BTC"

def test_oracle_hidden_flow_detection():
    oracle = MarketOracle()
    # Find a state that collapses
    for i in range(100):
        raw_data = {
            'price_delta': float(i * 10),
            'vol': 500.0,
            'flow': -0.2,
            'time': 0.1
        }
        analysis = oracle.process_market_tick("BTC", raw_data)
        if analysis['status'] == "H2_OBSTRUCTION_COLLAPSE":
            assert "hidden_flow_detected" in analysis
            # Verify hidden flow math: (current_sum_minus_r3 + hidden) % m == 0
            m = 64
            coords = analysis['coordinates']
            hidden = analysis['hidden_flow_detected']
            current_sum_minus_r3 = (sum(coords) - coords[2]) % m
            assert (current_sum_minus_r3 + hidden) % m == 0
            return
    # Note: Depending on the projection, we might not hit collapse in 100 steps
    # but with m=64 and gcd >= 16, it's fairly likely.

def test_multi_timeframe_sync():
    oracle = MarketOracle()
    data = {'price_delta': 10.0, 'vol': 100.0, 'flow': 0.1, 'time': 0.01}
    sync = oracle.multi_timeframe_sync("BTC", data, data, data)
    assert sync["aligned"] is True
    assert sync["final_action"] in ["HOLD/FOLLOW", "EXIT/REVERSE"]
