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

def test_parity_wall_detection():
    engine = ElectricityEngine(m=256, k=2)
    # 256.00 / 100 = 2.56
    # floor(2.56 * 100) % 256 = 0
    lower, upper = engine.find_nearest_parity_walls(2.56)
    assert lower == 2.56
    assert upper == 2.56 + 2.56

    lower, upper = engine.find_nearest_parity_walls(3.00)
    # 3.00 * 100 = 300
    # 300 / 256 = 1.17 -> lower_n = 1
    # lower_wall = 1 * 256 / 100 = 2.56
    # upper_wall = 2 * 256 / 100 = 5.12
    assert lower == 2.56
    assert upper == 5.12

def test_sniping_levels():
    engine = ElectricityEngine(m=256, k=2)
    analysis = engine.analyze({"1m": 3.00})
    # tick_size = 0.01
    # sniping_levels = { "lower": 2.56 + 0.20*0.01, "upper": 5.12 - 0.20*0.01 }
    # sniping_levels = { "lower": 2.562, "upper": 5.118 }
    assert analysis["sniping_levels"]["lower"] == pytest.approx(2.562)
    assert analysis["sniping_levels"]["upper"] == pytest.approx(5.118)

def test_sniping_zone():
    engine = ElectricityEngine(m=256, k=2)
    # gcd(R, 256) == 256 means R % 256 == 0
    prices = {"15m": 2.56, "5m": 5.12, "1m": 10.24} # Residues will be 0
    analysis = engine.analyze(prices)
    assert analysis["is_sniping_zone"] is True
