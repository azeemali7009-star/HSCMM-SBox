# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 01:03:13 2025

"""

import numpy as np
import math

# =============================
# Fixed Parameters
# =============================
a = 0.9
c = 0.15
b = 9.12
ITER = 500
SBOX_SIZE = 256  # 16x16 S-box

# =============================
# Chaotic Map Function
# =============================
def chaotic_map(x):
    return (a * math.sin(2 * math.pi * x) + b * (x - 0.5)**3 + c * x) % 1.0

# =============================
# Generate S-box from initial value x0
# =============================
def generate_sbox(x0):
    x = x0
    seq = []
    # Transient iterations
    for _ in range(ITER):
        x = chaotic_map(x)
    # Generate unique S-box values
    while len(seq) < SBOX_SIZE:
        x = chaotic_map(x)
        val = int(x * 256)
        if val not in seq:
            seq.append(val)
    return np.array(seq)

# =============================
# Walsh-Hadamard Transform
# =============================
def walsh_hadamard(f):
    f = np.array([1 if x else -1 for x in f])
    h = f.copy()
    size = 1
    while size < len(f):
        for i in range(0, len(f), size*2):
            for j in range(i, i+size):
                x = h[j]
                y = h[j + size]
                h[j] = x + y
                h[j + size] = x - y
        size *= 2
    return h

# =============================
# Maximum Nonlinearity
# =============================
def sbox_nonlinearity(sbox):
    max_corr = 0
    for bit in range(8):
        f = [(sbox[i] >> bit) & 1 for i in range(256)]
        wh = walsh_hadamard(f)
        max_corr = max(max_corr, np.max(np.abs(wh)))
    return 128 - max_corr // 2

# =============================
# Average Nonlinearity
# =============================
def sbox_average_nonlinearity(sbox):
    nl_list = []
    for bit in range(8):
        f = [(sbox[i] >> bit) & 1 for i in range(256)]
        wh = walsh_hadamard(f)
        max_corr = np.max(np.abs(wh))
        nl_bit = 128 - max_corr // 2
        nl_list.append(nl_bit)
    return sum(nl_list) / len(nl_list)

# =============================
# Search Best Initial Value
# =============================
best_nl = -1
best_x0 = None
best_sbox = None

for x0 in np.arange(0.01, 0.99, 0.01):
    try:
        sbox = generate_sbox(x0)
        nl = sbox_nonlinearity(sbox)
        if nl > best_nl:
            best_nl = nl
            best_x0 = x0
            best_sbox = sbox
    except:
        pass

# =============================
# Results
# =============================
print("Best Initial Value x0:", best_x0)
print("Maximum Nonlinearity (NL):", best_nl)
print("Average Nonlinearity (Avg NL):", sbox_average_nonlinearity(best_sbox))
print("\n16x16 S-box:\n")
print(best_sbox.reshape(16, 16))
