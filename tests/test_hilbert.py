import pytest
import numpy as np
from tgi.hilbert import HilbertMarketKernel, EigenstateEncoder

def test_kernel_normalization():
    kernel = HilbertMarketKernel(resolution=10)
    # Norm should be 1.0 (Unit probability)
    assert np.linalg.norm(kernel.psi) == pytest.approx(1.0)

    # After operator application, it should remain normalized
    kernel.apply_operator(100.0, 100.0, 'BUY')
    assert np.linalg.norm(kernel.psi) == pytest.approx(1.0)

def test_eigenstate_identification():
    kernel = HilbertMarketKernel(resolution=100)
    # Provide enough history for range mapping
    for i in range(10):
        kernel.apply_operator(100.0 + i, 10.0, 'BUY')

    # Apply a strong operator at a specific price (105.0)
    kernel.apply_operator(105.0, 5000.0, 'BUY')

    eigenstates = kernel.calculate_eigenstates()
    assert len(eigenstates) > 0
    # The strongest eigenstate should be around 105.0
    assert eigenstates[0]['price'] == pytest.approx(105.0, abs=0.5)

def test_market_energy_evolution():
    kernel = HilbertMarketKernel(resolution=64)
    # Initial state (uniform) has zero energy (zero gradient)
    energy_init = kernel.get_market_energy()
    assert energy_init == pytest.approx(0.0)

    # Interaction creates curvature in Psi, increasing energy (turbulence)
    kernel.apply_operator(100.0, 1000.0, 'BUY')
    energy_after = kernel.get_market_energy()
    assert energy_after > energy_init

def test_encoder_functionality():
    encoder = EigenstateEncoder(asset="GOLD", resolution=64)
    # Fill history
    for i in range(10):
        encoder.process_tick(2700.0 + i, 100.0, "BUY")

    analysis = encoder.process_tick(2705.0, 500.0, "SELL")
    assert analysis['asset'] == "GOLD"
    assert "core_eigenstate" in analysis
    assert "market_energy" in analysis
    assert analysis['status'] in ["STABLE_EIGENSTATE", "HIGH_ENERGY_TURBULENCE", "WAVE_PHASE_SHIFT"]

def test_prediction_materialization():
    encoder = EigenstateEncoder(resolution=10)
    # Simplified simulation
    for i in range(5):
        encoder.process_tick(10.0, 100.0, 'BUY')

    # Highest amplitude node should be around 10.0
    price = encoder.predict_materialization()
    assert price == pytest.approx(10.0, abs=1.0)
