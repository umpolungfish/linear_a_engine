#!/usr/bin/env python3
"""
Master Analysis Runner — runs all Linear A Engine analysis programs.

Usage:
    python programs/run_all.py data/linear_a_latff_sample.txt
"""

from __future__ import annotations
import argparse
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DEFAULT = REPO_ROOT / 'data' / 'linear_a_latff_sample.txt'

PROGRAMS = [
    {
        'name': 'Bootstrap Cycle Explorer',
        'script': 'programs/bootstrap_explorer.py',
        'args': ['--max-mismatches', '1'],
        'description': 'Frobenius cycles, spectral gap, closure density per section',
    },
    {
        'name': 'Tablet Topology Comparator',
        'script': 'programs/tablet_comparator.py',
        'args': ['--top-n', '10'],
        'description': 'Per-tablet structural fingerprints, JS divergence between sections',
    },
    {
        'name': 'IG Bridge',
        'script': 'programs/ig_bridge.py',
        'args': [],
        'description': 'Cross-system IG distance matrix (Linear A ↔ Rohonc ↔ Voynich)',
    },
]


def run_program(script: str, transcription: str, extra_args: list[str]) -> int:
    cmd = [sys.executable, script, transcription] + extra_args
    result = subprocess.run(cmd, cwd=REPO_ROOT)
    return result.returncode


def main():
    ap = argparse.ArgumentParser(description='Linear A Engine — master analysis runner')
    ap.add_argument('transcription', nargs='?', default=str(DATA_DEFAULT))
    args = ap.parse_args()

    print(f"\n{'═' * 65}")
    print(f"  Linear A Engine — Full Analysis Suite")
    print(f"  Transcription: {args.transcription}")
    print(f"{'═' * 65}")

    passed = failed = 0
    for prog in PROGRAMS:
        print(f"\n{'─' * 65}")
        print(f"  ▶  {prog['name']}")
        print(f"     {prog['description']}")
        print(f"{'─' * 65}")
        rc = run_program(prog['script'], args.transcription, prog['args'])
        if rc == 0:
            passed += 1
        else:
            failed += 1
            print(f"  [FAILED with exit code {rc}]")

    print(f"\n{'═' * 65}")
    print(f"  Complete: {passed} passed, {failed} failed")
    print(f"{'═' * 65}\n")
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
