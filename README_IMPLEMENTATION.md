# TGI Market Engine Implementation

## Overview
This engine implements the TGI Mind logic for the STRATOS monorepo, providing O(1) algebraic deduction for market states.

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
