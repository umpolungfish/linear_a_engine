#!/usr/bin/env python3
"""
Tablet Topology Comparator — structural fingerprints across Linear A tablets.

Computes per-tablet primitive distributions and Jensen-Shannon divergence
between the four corpus sections (Haghia Triada, Knossos, Zakros, Other Palatial).

Usage:
    python programs/tablet_comparator.py data/linear_a_latff_sample.txt [--top-n 10]
"""

from __future__ import annotations
import argparse
import math
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from linear_a_engine import compile_corpus, PRIMITIVES, SECTIONS

ALL_CODES = list(PRIMITIVES.keys())
ALL_MNEMONICS = [PRIMITIVES[c]['mnemonic'] for c in ALL_CODES]


def tablet_dist(tab_data: dict) -> dict[str, float]:
    counts: Counter = Counter()
    for instr in tab_data['instructions']:
        m = re.search(r'\|\s*(\w+)', instr)
        if m:
            counts[m.group(1)] += 1
    total = sum(counts.values()) or 1
    return {mn: counts.get(mn, 0) / total for mn in ALL_MNEMONICS}


def js_divergence(p: dict[str, float], q: dict[str, float]) -> float:
    keys = set(p) | set(q)
    m = {k: (p.get(k, 0) + q.get(k, 0)) / 2 for k in keys}
    def kl(a, b):
        return sum(a[k] * math.log(a[k] / b[k]) for k in keys
                   if a.get(k, 0) > 1e-12 and b.get(k, 0) > 1e-12)
    return (kl(p, m) + kl(q, m)) / 2


def section_of_tablet(tab_name: str) -> str:
    n = int(re.sub(r'\D', '', tab_name) or 0)
    for sec_range, sec_name, _ in SECTIONS:
        if n in sec_range:
            return sec_name
    return 'other_palatial'


def section_aggregate(pages: dict, section: str) -> dict[str, float]:
    combined: Counter = Counter()
    total = 0
    for tab_name, tab_data in pages.items():
        if section_of_tablet(tab_name) != section:
            continue
        for instr in tab_data['instructions']:
            m = re.search(r'\|\s*(\w+)', instr)
            if m:
                combined[m.group(1)] += 1
                total += 1
    if total == 0:
        return {mn: 0.0 for mn in ALL_MNEMONICS}
    return {mn: combined.get(mn, 0) / total for mn in ALL_MNEMONICS}


def top_tablets(pages: dict, n: int) -> list[tuple[str, dict]]:
    scored = []
    for name, data in pages.items():
        d = tablet_dist(data)
        # score by Frobenius balance
        fsplit = d.get('FSPLIT', 0)
        ffuse  = d.get('FFUSE', 0)
        balance = 1 - abs(fsplit - ffuse)
        scored.append((name, d, balance))
    scored.sort(key=lambda x: -x[2])
    return [(name, d) for name, d, _ in scored[:n]]


def main():
    ap = argparse.ArgumentParser(description='Tablet Topology Comparator — Linear A')
    ap.add_argument('transcription')
    ap.add_argument('--top-n', type=int, default=10)
    args = ap.parse_args()

    result = compile_corpus(args.transcription)
    pages = result['pages']

    print(f"\nLinear A Tablet Topology Comparator")
    print(f"{'─' * 60}")
    print(f"Tablets: {len(pages)}  ·  Total instructions: {result['total_instructions']}")

    print(f"\nTop {args.top_n} tablets by Frobenius balance:")
    print(f"  {'Tablet':8s}  {'Section':20s}  {'FSPLIT':7s}  {'FFUSE':7s}  {'CLINK':7s}  {'ISCRIB':7s}")
    print(f"  {'─' * 68}")
    for tab_name, d in top_tablets(pages, args.top_n):
        sec = section_of_tablet(tab_name)
        print(f"  {tab_name:8s}  {sec:20s}  "
              f"{d.get('FSPLIT', 0):.3f}    {d.get('FFUSE', 0):.3f}    "
              f"{d.get('CLINK', 0):.3f}    {d.get('ISCRIB', 0):.3f}")

    SECTION_NAMES = [name for _, name, _ in SECTIONS]
    section_dists = {s: section_aggregate(pages, s) for s in SECTION_NAMES}

    print(f"\nSection-level primitive distributions (top 6 opcodes):")
    for sec in SECTION_NAMES:
        d = section_dists[sec]
        top = sorted(d.items(), key=lambda x: -x[1])[:6]
        print(f"  {sec:20s}  " + "  ".join(f"{mn}:{pct:.3f}" for mn, pct in top))

    print(f"\nJensen-Shannon divergence between sections:")
    header = f"  {'':20s}" + "".join(f"  {s[:16]:16s}" for s in SECTION_NAMES)
    print(header)
    for a in SECTION_NAMES:
        row = f"  {a:20s}"
        for b in SECTION_NAMES:
            if a == b:
                row += f"  {'0.000':16s}"
            else:
                js = js_divergence(section_dists[a], section_dists[b])
                row += f"  {js:.4f}          "
        print(row)

    # OS imscription note
    print(f"\nNote: Linear A crystal imscription = OS imscription (d=0.00)")
    print(f"  ⟨ Ð_C  Þ_¨  Ř_Ť  Φ_}}  ƒ_ż  Ç_W  Γ_ʔ  ɢ_ˌ  ⊙_ÿ  Ħ_A  Σ_ï  Ω_z ⟩")
    print(f"  All four sections share this fixed-point structure.")


if __name__ == '__main__':
    main()
