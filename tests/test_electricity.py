import pytest
import math
from tgi.electricity import ElectricityEngine

def test_mapping_determinism():
    engine = ElectricityEngine(m=256, k=2)
    price = 4748.0
    residue = engine.map_price_to_residue(price)
    # 4748 * 100 = 474800
    # 474800 % 256 = 176
    assert residue == 176

def test_distance_to_obstruction_coprime():
    engine = ElectricityEngine(m=256, k=2)
    # Residues that are coprime to 256 (e.g., odd numbers)
    residues = {"15m": 1, "5m": 3, "1m": 5}
    d_omega = engine.calculate_distance_to_obstruction(residues)
    # (0.5 * 1/256) + (0.3 * 1/256) + (0.2 * 1/256) = 1/256
    assert d_omega == pytest.approx(1/256)
    assert engine.get_manifold_state(d_omega) == "Harmonious (Coprime)"

def test_trapdoor_trigger():
    engine = ElectricityEngine(m=256, k=2)
    # gcd(64, 256) = 64. 64 >= 256/8 (32)
    residues = {"15m": 1, "5m": 1, "1m": 64}
    action = engine.get_trade_action(0.1, residues)
    assert action == "IMMEDIATE EXIT (Trapdoor Snapped)"

def test_logic_gate_thresholds():
    engine = ElectricityEngine(m=256, k=2)
    # Harmonious
    assert engine.get_trade_action(0.04, {"1m": 1}) == "Hold/Trend Follow"
    # Torsion
    assert engine.get_trade_action(0.10, {"1m": 1}) == "Tighten Stops"
    # Singularity
    assert engine.get_trade_action(0.25, {"1m": 1}) == "IMMEDIATE EXIT / REVERSE"

def test_btc_example_from_prompt():
    engine = ElectricityEngine(m=256, k=2)
    # prompt: D_Omega = 0.28, Signal ABORT, gcd(64, 256) at 1m

    residues = {"15m": 128, "5m": 1, "1m": 64}
    prices = {tf: float(r) / 100 for tf, r in residues.items()} # Simple price mapping

    analysis = engine.analyze(prices)
    # D_Omega = 0.5 * (128/256) + 0.3 * (1/256) + 0.2 * (64/256)
    # D_Omega = 0.5 * 0.5 + 0.3 * 0.00390625 + 0.2 * 0.25
    # D_Omega = 0.25 + 0.001171875 + 0.05 = 0.30117...
    assert analysis["d_omega"] > 0.20
    assert analysis["action"] == "IMMEDIATE EXIT (Trapdoor Snapped)" # Trapdoor takes precedence

def test_sniping_zone():
    engine = ElectricityEngine(m=256, k=2)
    # gcd(R, 256) == 256 means R % 256 == 0
    prices = {"15m": 2.56, "5m": 5.12, "1m": 10.24} # Residues will be 0
    analysis = engine.analyze(prices)
    assert analysis["is_sniping_zone"] is True
