# Linear A Engine — Usage Guide

**IMASM compiler and Universal Engine runtime for the Linear A corpus**

---

## Setup

```bash
cd ~/linear_a_engine
uv sync
```

All CLI commands are installed into `.venv/bin/`. They are also available as shell aliases after sourcing `~/.bashrc` (see [Shell Aliases](#shell-aliases)).

---

## CLI Commands

### Compile

Compile a Linear A LATFF transcription to IMASM:

```bash
la-compile data/linear_a_latff_sample.txt
la-compile data/linear_a_latff_sample.txt --log la_full_log.txt --verbose
```

### Run

Execute the compiled corpus on the Tri-Phase Flux Register VM:

```bash
la-run data/linear_a_latff_sample.txt
```

### Call Graph

Generate the IMASM call graph:

```bash
la-graph data/linear_a_latff_sample.txt
la-graph data/linear_a_latff_sample.txt --tablet t1
la-graph data/linear_a_latff_sample.txt --output la_graph.png
```

### Sectional Analysis

Generate per-section topology graphs (Haghia Triada / Knossos / Zakros / Other Palatial):

```bash
la-sections data/linear_a_latff_sample.txt
```

---

## Analysis Programs

Run from the repo root with `python programs/<script>.py`:

### Bootstrap Cycle Explorer

Locates Frobenius loops in the corpus. Computes the bigram transition matrix,
spectral gap, and per-tablet closure density across all four sections.

```bash
python programs/bootstrap_explorer.py data/linear_a_latff_sample.txt
python programs/bootstrap_explorer.py data/linear_a_latff_sample.txt --max-mismatches 2
```

### Tablet Topology Comparator

Per-tablet structural fingerprints ranked by Frobenius balance, plus Jensen-Shannon
divergence between the four corpus sections.

```bash
python programs/tablet_comparator.py data/linear_a_latff_sample.txt
python programs/tablet_comparator.py data/linear_a_latff_sample.txt --top-n 20
```

### IG Bridge

Cross-system structural distance matrix: Linear A ↔ Rohonc ↔ Voynich ↔ OS imscription.
Verifies the zero-distance theorem: d(Linear A, OS imscription) = 0.00.

```bash
python programs/ig_bridge.py
```

### Run All

Execute the full suite sequentially:

```bash
python programs/run_all.py data/linear_a_latff_sample.txt
```

---

## Crystal Imscription

```
⟨ Ð_C  Þ_¨  Ř_Ť  Φ_}  ƒ_ż  Ç_W  Γ_ʔ  ɢ_ˌ  ⊙_ÿ  Ħ_A  Σ_ï  Ω_z ⟩
Tier: O_∞   C score: 0.0   IG distance to OS imscription: 0.00
```

**Zero-distance theorem**: d(Linear A, OS imscription) = 0.00, conflicts: ∅.
Linear A is not a system that converges toward the grammar — it *is* the grammar.
The six-system MEET (Hebrew, Sanskrit, Egyptian, Cuneiform, Basque, Linear A) is
identical to the five-system MEET. Linear A adds no new constraint.

---

## LATFF Format

Linear A Tablet Folio Format:

```
<t1>
;H> cu hk fa ba lt lp br cv
;H> br cv vt hz cl dt cu hk
```

- `<t{N}>` — tablet marker
- `;H>` — symbol line
- 12 family codes: `cu hk fa ba lt lp br cv vt hz cl dt`
  - `cu` = VINIT (initial object ∅)  — distinct from Rohonc's `cr`
  - `lt` = CLINK (composition ∘)    — distinct from Rohonc's `lg`

---

## Bootstrap Sequence

```
lp → ba → br → fa → cv → lt → dt → lp
ISCRIB → AREV → FSPLIT → AFWD → FFUSE → CLINK → IFIX → ISCRIB
```

Same categorical structure as Rohonc (`lg`) and Voynich (`d`). Different surface tokens,
identical grammar.

---

## Shell Aliases

After `source ~/.bashrc`:

```bash
la-compile   # compile LATFF to IMASM
la-run       # execute on Tri-Phase VM
la-graph     # generate call graph
la-sections  # sectional topology analysis
```

Interactive REPL (unified across all three manuscript engines):

```bash
ms-eval                             # enter unified REPL
ms-eval --expr "linear_a t1"        # single expression
ms-eval --expr ":near linear_a:t1"  # nearest neighbors
ms-eval --expr ":ig_bridge"         # distance matrix
```

---

## Four Sections

| Section | Tablets | Site | Dominant character |
|---------|---------|------|--------------------|
| haghia_triada | t1–t39 | Haghia Triada | Administrative recursive: FSPLIT, CLINK, ENGAGR |
| knossos | t40–t79 | Knossos | LM IB destruction deposits |
| zakros | t80–t119 | Zakros (ZA) | Eastern palace archive |
| other_palatial | t120–t159 | Akrotiri, Malia, Palaikastro, Tylissos | Mixed palatial sites |

The Haghia Triada tablets (~40% of known corpus) are the most structurally complex:
counting systems generate forks (FSPLIT), compound signs fuse them (FFUSE),
and closed loops (ENGAGR) stabilize contradictions in the accounting.
