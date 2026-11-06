#!/usr/bin/env python3
"""
Bootstrap Cycle Explorer — Frobenius loops in the Linear A corpus.

Bootstrap sequence (LATFF codes):
  lp → ba → br → fa → cv → lt → dt → lp
  ISCRIB → AREV → FSPLIT → AFWD → FFUSE → CLINK → IFIX → ISCRIB

Performs:
  - Bigram transition matrix (Markov chain structure)
  - Bootstrap sequence closure detection per tablet
  - Section-level cycle density comparison (Haghia Triada / Knossos / Zakros / Other)
  - Spectral gap of the transition matrix

Usage:
    python programs/bootstrap_explorer.py data/linear_a_latff_sample.txt [--max-mismatches 1]
"""

from __future__ import annotations
import argparse
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from linear_a_engine import compile_corpus, PRIMITIVES, BOOTSTRAP_SEQUENCE, SECTIONS

MNEMONIC_TO_CODE = {meta['mnemonic']: code for code, meta in PRIMITIVES.items()}
ALL_CODES = list(PRIMITIVES.keys())

BOOTSTRAP_CODES = BOOTSTRAP_SEQUENCE[:-1]  # drop trailing repeat


def extract_code_stream(result: dict) -> list[str]:
    stream = []
    for tab_name in sorted(result['pages'].keys(),
                            key=lambda x: int(re.sub(r'\D', '', x) or 0)):
        for instr in result['pages'][tab_name]['instructions']:
            m = re.search(r'\|\s*(\w+)', instr)
            if m:
                code = MNEMONIC_TO_CODE.get(m.group(1))
                if code:
                    stream.append(code)
    return stream


def build_bigram_matrix(stream: list[str]) -> dict:
    counts: dict[str, Counter] = defaultdict(Counter)
    for i in range(len(stream) - 1):
        counts[stream[i]][stream[i + 1]] += 1
    matrix: dict[str, dict[str, float]] = {}
    for src, targets in counts.items():
        total = sum(targets.values())
        matrix[src] = {tgt: cnt / total for tgt, cnt in targets.items()}
    return matrix


def spectral_gap(matrix: dict) -> float:
    codes = ALL_CODES
    n = len(codes)
    idx = {c: i for i, c in enumerate(codes)}
    M = [[0.0] * n for _ in range(n)]
    for src, targets in matrix.items():
        if src not in idx:
            continue
        for tgt, prob in targets.items():
            if tgt in idx:
                M[idx[src]][idx[tgt]] = prob
    v = [1.0 / n] * n
    for _ in range(200):
        nv = [sum(M[j][i] * v[j] for j in range(n)) for i in range(n)]
        norm = math.sqrt(sum(x * x for x in nv))
        if norm < 1e-12:
            break
        v = [x / norm for x in nv]
    lam1 = sum(sum(M[j][i] * v[j] for j in range(n)) * v[i] for i in range(n))
    v2 = [(-1) ** i / n for i in range(n)]
    for _ in range(200):
        nv2 = [sum(M[j][i] * v2[j] for j in range(n)) for i in range(n)]
        proj = sum(nv2[i] * v[i] for i in range(n))
        nv2 = [nv2[i] - proj * v[i] for i in range(n)]
        norm = math.sqrt(sum(x * x for x in nv2))
        if norm < 1e-12:
            break
        v2 = [x / norm for x in nv2]
    lam2 = sum(sum(M[j][i] * v2[j] for j in range(n)) * v2[i] for i in range(n))
    return abs(lam1) - abs(lam2)


def find_bootstrap_windows(stream: list[str], max_miss: int) -> list[tuple[int, int, int]]:
    results = []
    L = len(BOOTSTRAP_CODES)
    for start in range(len(stream) - L + 1):
        window = stream[start:start + L]
        misses = sum(1 for a, b in zip(window, BOOTSTRAP_CODES) if a != b)
        if misses <= max_miss:
            results.append((start, start + L - 1, misses))
    return results


def section_of_tablet(tab_name: str) -> str:
    n = int(re.sub(r'\D', '', tab_name) or 0)
    for sec_range, sec_name, _color in SECTIONS:
        if n in sec_range:
            return sec_name
    return 'other_palatial'


def main():
    ap = argparse.ArgumentParser(description='Bootstrap Cycle Explorer — Linear A')
    ap.add_argument('transcription', help='Path to Linear A LATFF file')
    ap.add_argument('--max-mismatches', type=int, default=1)
    args = ap.parse_args()

    result = compile_corpus(args.transcription)
    stream = extract_code_stream(result)

    print(f"\nLinear A Bootstrap Cycle Explorer")
    print(f"{'─' * 60}")
    print(f"Total instructions: {len(stream)}")
    print(f"Bootstrap sequence: {' → '.join(BOOTSTRAP_CODES)}")

    matrix = build_bigram_matrix(stream)
    gap = spectral_gap(matrix)
    print(f"\nBigram transition matrix: {len(matrix)} sources")
    print(f"Spectral gap: {gap:.6f}")
    if gap > 0.3:
        print("  → High gap: strong Markovian memory")
    elif gap > 0.1:
        print("  → Moderate gap: semi-structured transitions")
    else:
        print("  → Low gap: near-uniform mixing")

    windows = find_bootstrap_windows(stream, args.max_mismatches)
    print(f"\nBootstrap windows (≤{args.max_mismatches} mismatch): {len(windows)}")
    for start, end, miss in windows[:10]:
        print(f"  positions {start:5d}–{end:5d}  mismatches={miss}")

    print(f"\nPer-tablet bootstrap closure:")
    page_counts: Counter = Counter()
    for tab_name, tab_data in sorted(result['pages'].items(),
                                      key=lambda x: int(re.sub(r'\D', '', x[0]) or 0)):
        tab_stream = []
        for instr in tab_data['instructions']:
            m = re.search(r'\|\s*(\w+)', instr)
            if m:
                code = MNEMONIC_TO_CODE.get(m.group(1))
                if code:
                    tab_stream.append(code)
        n_hits = len(find_bootstrap_windows(tab_stream, args.max_mismatches))
        sec = section_of_tablet(tab_name)
        page_counts[sec] += n_hits
        if n_hits:
            print(f"  {tab_name:8s}  [{sec:16s}]  {n_hits} closure(s)")

    print(f"\nSection closure density:")
    section_tabs: Counter = Counter()
    for tab_name in result['pages']:
        section_tabs[section_of_tablet(tab_name)] += 1
    for _range, sec, _color in SECTIONS:
        total = section_tabs.get(sec, 0)
        hits = page_counts.get(sec, 0)
        density = hits / max(total, 1)
        bar = '█' * int(density * 20)
        print(f"  {sec:20s}  {hits:3d}/{total:3d}  {bar} {density:.3f}")


if __name__ == '__main__':
    main()
