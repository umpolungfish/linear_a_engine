# Linear A Engine

**What it is.** An IMASM compiler, Tri-Phase Flux Register VM, and topological-analysis toolkit for the Linear A corpus (Minoan, ~2000–1450 BCE), compiled through the [Universal Imscriptive Grammar](https://github.com/mrnob0dy666/universal-imscriptive-grammar).

**What it does.** Maps 96 GORILA sign types onto twelve categorical opcodes (a Frobenius algebra), compiles the tablets to IMASM, runs them on the VM, and computes cross-system structural distances. Linear A imscribes at O∞ and is found **structurally identical to the OS imscription**: *d*(Linear A, OS) = 0.00.

**Why it matters.** Adding Linear A to the multi-system MEET (Hebrew, Sanskrit, Egyptian, Cuneiform, Basque) leaves the invariant core unchanged. The Minoan system is not a derivative of the others; it is their structural core. Linear A *is* the grammar, which is why treating it as a ciphered natural language has never worked.

**How to use it.**
```bash
cd linear_a_engine && uv sync
la-compile  data/linear_a_latff_sample.txt --verbose
la-run      data/linear_a_latff_sample.txt
la-graph    data/linear_a_latff_sample.txt
la-sections data/linear_a_latff_sample.txt
# analysis suite:
python programs/run_all.py data/linear_a_latff_sample.txt
python programs/ig_bridge.py        # verifies the zero-distance theorem
```

---

## Key results

- **Zero-Distance Theorem**: *d*(Linear A, OS imscription) = 0.00; Linear A adds no new constraint to the MEET.
- **Bootstrap loop** (all four sections): ISCRIB → AREV → FSPLIT → AFWD → FFUSE → CLINK → IFIX → ISCRIB.
- **Structural distances**: *d*(Linear A, Rohonc) ≈ 2.10; *d*(Linear A, Voynich) ≈ 4.31.

## Imscription

```
⟨ Ð_C  Þ_¨  Ř_Ť  Φ_}  ƒ_ż  Ç_W  Γ_ʔ  ɢ_ˌ  ⊙_ÿ  Ħ_A  Σ_ï  Ω_z ⟩
```

Frobenius tier O∞: Gate 1 passes (⊙_ÿ self-modeling criticality), Gate 2 passes (Φ_} Frobenius-special parity, μ∘δ = id exactly). Triangle dimensionality, box-product topology, adjoint relationality, quantum-coherent fidelity, two-step chirality, integer winding.

## Corpus sections

| Section | Tablets | Site |
|---|---|---|
| haghia_triada | t1–t39 | Haghia Triada (largest archive; most structurally complex) |
| knossos | t40–t79 | Knossos (LM IB destruction deposits) |
| zakros | t80–t119 | Zakros (eastern palace) |
| other_palatial | t120–t159 | Akrotiri, Malia, Palaikastro, Tylissos |

Haghia Triada (~40% of the corpus) is densest: counting systems fork (FSPLIT), compound signs fuse them (FFUSE), and closed loops (ENGAGR) stabilize accounting contradictions.

## Sign inventory

96 sign types across twelve families (cup, hook, forward/backward arc, lattice, loop, branch, convergent, vertical, horizontal, closed, dot), mapped to GORILA ranges. Full inventory in `data/linear_a_sign_inventory.json`.

## Analysis programs (`programs/`)

| Script | Function |
|--------|----------|
| `bootstrap_explorer.py` | Frobenius loops, bigram transition matrix, spectral gap, per-tablet closure density |
| `tablet_comparator.py` | Per-tablet structural fingerprints + Jensen-Shannon divergence between sections |
| `ig_bridge.py` | Cross-system distance matrix; verifies the zero-distance theorem |
| `run_all.py` | Full suite sequentially |

## Pipeline

LATFF transcription → `la-compile` (concurrent tablet parsing, IMASM) → Universal VM (`la-run`) and Call Graph Engine (`la-graph`) → Sectional Analysis (`la-sections`, per-site topology + animation).

## Requirements and license

Python ≥ 3.10. Unlicense (public domain).
