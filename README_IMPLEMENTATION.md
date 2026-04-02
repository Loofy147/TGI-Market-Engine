# TGI Market Engine Implementation

## Overview
This engine implements the TGI Mind logic for the STRATOS monorepo, providing O(1) algebraic deduction for market states.

## Documentation
- **[Technical Manual](docs/TECHNICAL_MANUAL.md):** Detailed architectural and signal logic.
- **[Theoretical Basis](docs/THEORY.md):** The underlying FSO and torus manifold theory.

## Core Components
- **Kernel (`src/tgi/kernel.py`):** The "Algebraic Mind" that projects features onto the Z_m^4 torus.
- **Oracle (`src/tgi/oracle.py`):** The "Execution Adapter" that links the kernel to live feeds and deduces hidden flows.
- **Tests (`tests/test_tgi_kernel.py`):** Validation suite for parity logic.

## Usage
```python
from src.tgi.oracle import MarketOracle
oracle = MarketOracle()
analysis = oracle.process_market_tick("BTC", tick_data)
print(analysis['status']) # PROTECTED, H2_OBSTRUCTION_COLLAPSE, etc.
```

## Configuration
- BTC: m=64 (Thin Fibers / High Velocity)
- Gold: m=256 (Thick Fibers / Deep Liquidity)

## Electricity Execution Layer
The **Moaziz-TGI Execution Layer** (Electricity Algorithm) is a deterministic, $O(1)$ system that trades **Symmetry Breaks** rather than price patterns.

### Components
- **Electricity Engine (`src/tgi/electricity.py`):** Calculates the **Distance to Obstruction ($\mathcal{D}_{\Omega}$)** across multiple timeframes to identify manifold state.
- **Residue Watcher (`scripts/residue_watcher.py`):** CLI tool for real-time topological analysis of price data.

### Usage
Run the Residue Watcher to analyze a specific asset's timeframe prices:
```bash
python3 scripts/residue_watcher.py --asset GOLD --m 256 --k 2 --p15m 2745.5 --p5m 2744.8 --p1m 2748.0
```

### Logic Gates
- **Coprime ($\mathcal{D}_{\Omega} \le 0.05$):** Go/Hold.
- **Shared Factors ($0.05 < \mathcal{D}_{\Omega} \le 0.15$):** Caution (Tighten Stops).
- **Singularity ($\mathcal{D}_{\Omega} > 0.20$):** Immediate Exit/Reverse.
- **Trapdoor:** Exit immediately if the 1m residue $\gcd(R_1, m) \ge m/8$.

### Sniping Protocol
The engine identifies **Parity Walls** where total obstruction occurs ($\gcd(R, m) = m$).
- **Limit Orders:** Place orders 0.20 ticks before the wall to catch symmetry-break bounces.
- **Verification:** Use the `ElectricityEngine.find_nearest_parity_walls()` method to locate these obstructions relative to the current price.

### Backtesting
Run the electricity-based backtest to validate the $O(1)$ trading strategy:
```bash
python3 scripts/electricity_backtest.py
```
This simulation tests **Trapdoor Exits**, **Coordinated Reset entries**, and **Wall Sniping** logic.

## Non-Commutative Execution Layer (Twisted Fiber)
The **Twisted Fiber** engine transcends price patterns by trading the **Non-Abelian holonomy** of order flow. It treats buy and sell sequences as non-commutative operators in SL(2, R).

### Components
- **Non-Commutative Kernel (`src/tgi/non_commutative.py`):** Represents the market state as a $2 \times 2$ matrix. Buy ticks are upper triangular; Sell ticks are lower triangular.
- **Holonomy Watcher (`scripts/holonomy_watcher.py`):** Monitors the "Twist" in the order book's fiber—a geometric phase shift revealing hidden institutional accumulation.
- **Twisted Backtester (`scripts/twisted_backtest.py`):** Simulates path-dependent liquidity flow and demonstrates the "Front-Run" edge on structural snaps.

### Logic & Signals
- **Holonomy ($\mathcal{H}$):** The deviation of the manifold state from the identity. $\mathcal{H} = |\text{Tr}(M) - 2|$.
- **Status: TWISTED_ACCUMULATION ($\mathcal{H} > 0.1$):** Hidden institutional pressure.
- **Status: SINGULAR_SNAP_IMMINENT ($\mathcal{H} > 0.5$):** Structural imbalance reached; trend reversal/expansion likely.

### Usage
Analyze the holonomy of a live tick stream:
```bash
python3 scripts/holonomy_watcher.py --asset XAUUSD --ticks 10
```
Run the non-commutative strategy backtest:
```bash
python3 scripts/twisted_backtest.py
```

## Hilbert Stratification (Continuous Eigenstate Execution)
By pushing $k \to \infty$, the TGI Mind eliminates artificial timeframe constraints. The market is mapped into an infinite-dimensional **Hilbert Space**, where price is a continuous wave function $\Psi$.

### Components
- **Hilbert Kernel (`src/tgi/hilbert.py`):** Evolves a complex wave function based on tick interactions. Identifies the natural, zero-energy **eigenstates** (resting frequencies) of the asset.
- **Wave Watcher (`scripts/wave_watcher.py`):** Visualizes the resonant frequencies and probability density of the price-manifold.
- **Hilbert Backtester (`scripts/hilbert_backtest.py`):** Executes trades at the exact mathematical nodes of the wave function, achieving zero search latency.

### Logic & Signals
- **Eigenstate Probability ($\mathcal{P}$):** The strength of a resonant node. $\mathcal{P} = |\Psi|^2$.
- **Market Energy ($\mathcal{E}$):** Expectation value of the Hamiltonian. $\mathcal{E} > 0.5$ signals a **Phase Shift** (manifold breakage).
- **Status: STABLE_EIGENSTATE ($\mathcal{E} < 0.1$):** Laminar flow; price is bound to a resonant frequency.
- **Signal: MATERIALIZE_LIQUIDITY:** Place limit orders at core eigenstate nodes.

### Usage
Watch the live price wave function:
```bash
python3 scripts/wave_watcher.py --asset BTCUSD --ticks 10
```
Run the Hilbert-based eigenstate backtest:
```bash
python3 scripts/hilbert_backtest.py
```
