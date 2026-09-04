# HSCMM-SBox

Supplementary code and data for the manuscript:

**A Secure S-Box Construction Approach Using Hybrid Sinusoidal Cubic Modular Map and Hybrid Optimization Techniques**

## Overview

This repository contains the Python implementations and supplementary data associated with the proposed one-dimensional Hybrid Sinusoidal Cubic Modular Map (HSCMM) and the S-box construction and optimization framework presented in the manuscript.

The framework combines chaotic-map-based S-box generation with hybrid optimization involving a Genetic Algorithm (GA), Hill Climbing (HC), and an affine transformation. Nonlinearity is used as a principal optimization criterion.

The resulting S-boxes are evaluated using the following cryptographic criteria:

- Nonlinearity (NL)
- Bit Independence Criterion – Nonlinearity (BIC-NL)
- Strict Avalanche Criterion (SAC)
- Bit Independence Criterion – SAC (BIC-SAC)
- Linear Approximation Probability (LAP) bias
- Differential Approximation Probability (DAP)

## Repository Structure

HSCMM-SBox/
- `sbox.py` — main S-box generation and hybrid optimization implementation
- `105NL.py` — high-nonlinearity S-box search
- `ChaoticCode.pdf` — supplementary material related to the chaotic-map analysis
- `S-Box/SBOX_100_AvgNL.txt` — 100 generated and optimized S-boxes
- `S-Box/sboxes_summary.csv` — cryptographic evaluation results

## Code

### sbox.py

The main implementation includes:

- HSCMM-based initial S-box generation
- Walsh-Hadamard-transform-based nonlinearity evaluation
- Genetic Algorithm optimization
- Hill Climbing optimization
- Affine transformation/optimization
- Generation and storage of 100 S-boxes
- Resume support for previously generated S-boxes

The generated S-boxes are stored in `S-Box/SBOX_100_AvgNL.txt`.

### 105NL.py

This program searches for an HSCMM-generated S-box with high nonlinearity and evaluates candidate S-boxes using nonlinearity and average nonlinearity measures.

## Data

### SBOX_100_AvgNL.txt

Contains 100 generated and optimized S-boxes together with their average nonlinearity values.

### sboxes_summary.csv

Contains cryptographic evaluation results for the S-boxes.

The columns are:

- `index` — S-box index
- `NL` — Nonlinearity
- `BIC_NL` — Bit Independence Criterion – Nonlinearity
- `SAC` — Strict Avalanche Criterion
- `BIC_SAC` — Bit Independence Criterion – SAC
- `LAP_bias` — Linear Approximation Probability bias
- `DAP` — Differential Approximation Probability

## Requirements

The Python programs require Python 3 and NumPy.

Install the required package using:

```bash
python3 -m pip install -r requirements.txt

```

## Running the Code

Run the S-box generation and hybrid optimization procedure using:

`python3 sbox.py`

Run the high-nonlinearity S-box search using:

`python3 105NL.py`

## Methodology

The computational workflow implemented in this repository is:

1. Generate initial 8-bit S-box candidates using the HSCMM chaotic map.
2. Evaluate candidate S-boxes using Walsh-Hadamard-transform-based nonlinearity.
3. Improve candidate S-boxes using Genetic Algorithm and Hill Climbing optimization.
4. Apply affine transformation/optimization to further refine the S-boxes.
5. Evaluate the final S-boxes using NL, BIC-NL, SAC, BIC-SAC, LAP bias, and DAP.
6. Store the resulting S-boxes and summary metrics in the supplementary data files.

## Citation

If you use this code or data, please cite the associated manuscript:

*A Secure S-Box Construction Approach Using Hybrid Sinusoidal Cubic Modular Map and Hybrid Optimization Techniques*.

Full bibliographic details will be added after publication.

## License and Contribution Guidelines

The software in this repository is released under the MIT License. See `LICENSE` for details.

Contributions that improve reproducibility, documentation, or the implementation are welcome. Please open an issue or submit a pull request describing the proposed change.
