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
