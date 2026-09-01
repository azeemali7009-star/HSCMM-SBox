import numpy as np
import math
import random
import os

# =====================================
# Parameters
# =====================================
a = 0.9
c = 0.15
b = 9.12
ITER = 500
POP_SIZE = 10
GENS = 25
SBOX_SIZE = 256
TOTAL_SBOXES = 100   # <<< REQUIRED
OUT_FILE = "S-Box/SBOX_100_AvgNL.txt"

# =====================================
# Chaotic Map
# =====================================
def chaotic_map(x):
    return (a * math.sin(2 * math.pi * x)
            + b * (x - 0.5)**3
            + c * x) % 1.0

# =====================================
# Generate Chaotic S-box
# =====================================
def generate_sbox(x0):
    x = x0
    s = []
    for _ in range(ITER):
        x = chaotic_map(x)
    while len(s) < 256:
        x = chaotic_map(x)
        v = int(x * 256)
        if v not in s:
            s.append(v)
    return np.array(s)

# =====================================
# Walsh-Hadamard Transform
# =====================================
def walsh_hadamard(f):
    f = np.array([1 if x else -1 for x in f])
    h = f.copy()
    size = 1
    while size < len(f):
        for i in range(0, len(f), size * 2):
            for j in range(i, i + size):
                x = h[j]
                y = h[j + size]
                h[j] = x + y
                h[j + size] = x - y
        size *= 2
    return h

# =====================================
# Average Nonlinearity
# =====================================
def avg_nl(sbox):
    nls = []
    for bit in range(8):
        f = [(sbox[i] >> bit) & 1 for i in range(256)]
        wh = walsh_hadamard(f)
        max_corr = np.max(np.abs(wh))
        nls.append(128 - max_corr // 2)
    return sum(nls) / 8

# =====================================
# Hill Climbing
# =====================================
def hill_climb(sbox, steps=2000):
    best = sbox.copy()
    best_nl = avg_nl(best)

    for _ in range(steps):
        i, j = random.sample(range(256), 2)
        cand = best.copy()
        cand[i], cand[j] = cand[j], cand[i]
        nl = avg_nl(cand)
        if nl > best_nl:
            best, best_nl = cand, nl
    return best

# =====================================
# Genetic Algorithm
# =====================================
def genetic_algorithm():
    population = [generate_sbox(random.random()) for _ in range(POP_SIZE)]

    for _ in range(GENS):
        population.sort(key=lambda s: avg_nl(s), reverse=True)
        new_pop = population[:2]  # elitism

        while len(new_pop) < POP_SIZE:
            p1, p2 = random.sample(population[:5], 2)
            cut = random.randint(60, 200)

            child = list(p1[:cut])
            for v in p2:
                if v not in child:
                    child.append(v)

            child = hill_climb(np.array(child))
            new_pop.append(child)

        population = new_pop

    return population[0]

# =====================================
# Affine Transformation
# =====================================
def affine_transform(sbox, A, b):
    out = np.zeros(256, dtype=int)
    for i in range(256):
        x = sbox[i]
        y = 0
        for bit in range(8):
            bit_val = bin(A[bit] & x).count("1") % 2
            y |= ((bit_val ^ ((b >> bit) & 1)) << bit)
        out[i] = y
    return out

# =====================================
# Affine Optimization
# =====================================
def affine_optimization(sbox, trials=600):
    best = sbox.copy()
    best_nl = avg_nl(best)

    for _ in range(trials):
        A = [random.randint(1, 255) for _ in range(8)]
        bb = random.randint(0, 255)

        cand = affine_transform(sbox, A, bb)
        nl = avg_nl(cand)

        if nl > best_nl:
            best, best_nl = cand, nl

        if best_nl >= 112:
            break

    return best

# =====================================
# Resume support: detect how many S-boxes are already saved
# =====================================
def detect_completed(path):
    if not os.path.exists(path):
        return 0
    count = 0
    with open(path, "r") as fh:
        for line in fh:
            if line.strip().startswith("S-box #"):
                try:
                    num = int(line.strip().split("#")[1])
                    count = max(count, num)
                except Exception:
                    continue
    return count

# =====================================
# MAIN: Generate 100 S-boxes
# =====================================
completed = detect_completed(OUT_FILE)
start_idx = completed + 1

mode = "a" if completed > 0 else "w"
with open(OUT_FILE, mode) as f:
    for k in range(start_idx, TOTAL_SBOXES + 1):
        print(f"Generating S-box {k}/{TOTAL_SBOXES} (resumed at {start_idx}) ...")

        sbox = genetic_algorithm()
        sbox = affine_optimization(sbox)
        nl = avg_nl(sbox)

        f.write("\n========================================\n")
        f.write(f"S-box #{k}\n")
        f.write(f"Average Nonlinearity = {nl}\n")
        f.write(np.array2string(sbox.reshape(16, 16)))
        f.write("\n")

print("\n✅ DONE: 100 S-boxes saved to 'S-Box/SBOX_100_AvgNL.txt'")
