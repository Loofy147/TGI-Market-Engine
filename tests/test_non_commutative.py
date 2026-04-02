import pytest
import numpy as np
from tgi.non_commutative import NonCommutativeKernel, TwistedFiberEncoder

def test_non_commutative_property():
    kernel = NonCommutativeKernel()

    # Sequence A: Buy then Sell
    kernel.apply_tick('BUY', 100.0)
    kernel.apply_tick('SELL', 100.0)
    state_a = kernel.state.copy()

    kernel.reset()

    # Sequence B: Sell then Buy
    kernel.apply_tick('SELL', 100.0)
    kernel.apply_tick('BUY', 100.0)
    state_b = kernel.state.copy()

    # In a non-commutative manifold, AB != BA
    assert not np.array_equal(state_a, state_b)

def test_holonomy_accumulation():
    kernel = NonCommutativeKernel()
    # A single BUY(v) + SELL(v) loop
    v = 1.0 # 1000 normalized to 1
    kernel.apply_tick('BUY', 1000.0)
    kernel.apply_tick('SELL', 1000.0)

    holonomy = kernel.calculate_holonomy()
    # Matrix A = [[1, 1], [0, 1]]
    # Matrix B = [[1, 0], [-1, 1]]
    # AB = [[1, 1], [0, 1]] * [[1, 0], [-1, 1]] = [[1-1, 1], [-1, 1]] = [[0, 1], [-1, 1]]
    # Trace = 1. Holonomy = |1 - 2| = 1.
    assert holonomy == pytest.approx(1.0)

def test_twisted_fiber_encoder():
    encoder = TwistedFiberEncoder(asset="BTCUSD")
    analysis = encoder.process_tick(65000.0, 500.0, "BUY")

    assert analysis['asset'] == "BTCUSD"
    assert analysis['side'] == "BUY"
    assert analysis['volume'] == 500.0
    assert analysis['holonomy'] == 0.0 # Trace of [[1, 0.5], [0, 1]] is 2

def test_structural_snap_signal():
    encoder = TwistedFiberEncoder()
    # Force a snap through a loop
    encoder.process_tick(100.0, 1000.0, "BUY")
    analysis = encoder.process_tick(100.0, 1000.0, "SELL")

    assert analysis['holonomy'] == pytest.approx(1.0)
    assert analysis['status'] == "SINGULAR_SNAP_IMMINENT"
    assert analysis['signal'] == "FRONT_RUN"

def test_loop_closure_deduction():
    encoder = TwistedFiberEncoder()
    holonomy = encoder.check_loop_closure(1000.0, 1000.0)
    assert holonomy == pytest.approx(1.0)
