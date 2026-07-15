"""
The twelve Linear A sign families as categorical opcodes.

Linear A (Minoan, ~2000–1450 BCE) has a syllabic inventory of ~90 CV signs
and ~150 ideographic signs. Twelve visual-structural families are identified
following the GORILA sign classification. The correspondence is structural:
each family maps to the same categorical primitive it occupies in the Voynich
(EVA) and Rohonc (RTFF) systems.

Transcription codes (LATFF — Linear A Tablet Folio Format):
  cu  cup/vessel forms         → VINIT   (initiating/containing)
  hk  hook/arm forms           → TANCH   (terminal curved stroke)
  fa  forward-arc forms        → AFWD    (open outward curve)
  ba  backward-arc forms       → AREV    (open inward curve)
  lt  lattice/compound forms   → CLINK   (joined multi-element)
  lp  loop/knot forms          → ISCRIB  (self-closing)
  br  branching forms          → FSPLIT  (forking strokes)
  cv  convergent/triangular    → FFUSE   (strokes to a point)
  vt  vertical-stroke forms    → EVALT   (dominant vertical)
  hz  horizontal-stroke forms  → EVALF   (dominant horizontal)
  cl  closed/circle forms      → ENGAGR  (fully enclosed)
  dt  dot/fraction marks       → IFIX    (terminal point mark)

──────────────────────────────────────────────────────────────────────────────
Crystal imscription (IG notation, SYMBOL_REFERENCE.md)
⟨ Ð  Þ  Ř  Φ  ƒ  Ç  Γ  ɢ  ⊙  Ħ  Σ  Ω ⟩

Linear A:
  ⟨ 𐑨  𐑶  𐑽  𐑹  ƒ^ż  Ç^W  𐑲  ɢ^ˌ  ⊙  𐑖  𐑳  𐑭 ⟩
  Tier: O_∞  (⊙ + 𐑹)

The exOS OS imscription is the component-wise MEET of five ancient writing
systems (Hebrew, Sanskrit, Egyptian, Cuneiform, Basque), expressed in exOS
notation as [D=1,T=3,R=2,P=4,F=2,K=1,G=2,Γ=2,Φ=1,H=2,S=2,Ω=2].

Translated into IG notation (SYMBOL_REFERENCE.md):

  exOS primitive → IG primitive   (value mapping)
  ─────────────────────────────────────────────────────────────────────
  D  Dimensionality  →  Ð        wedge(0)   triangle(1)  infty(2)   holo(3)
                                  𐑛        𐑨          𐑼        𐑦
  T  Topology        →  Þ        net(0)  in(1)  bowtie(2)  box(3)  odot(4)
                                  𐑡     𐑰    𐑥        𐑶     𐑸
  R  Relational mode →  Ř        super(0)  cat(1)  dagger(2)  lr(3)
                                  𐑩       𐑑     𐑽        𐑾
  P  Parity/symmetry →  Φ        asym(0)  psi(1)  pm(2)  sym(3)  pm_sym(4)
     [NOTE: exOS P ≡ IG Φ;        𐑗      𐑿     𐑬    𐑯     𐑹
      exOS Φ ≡ IG ⊙]
  F  Fidelity        →  ƒ        ell(0)  eth(1)  hbar(2)
                                  ƒ^ì     ƒ^ð     ƒ^ż
  K  Kinetics        →  Ç        fast(0)  mod(1)  slow(2)  trap(3)  MBL(4)
                                  Ç^-      Ç^W     Ç^@      Ç^Ù      Ç^λ
  G  Scope/gran.     →  Γ        beth(0)  gimel(1)  aleph(2)
                                  𐑚      𐑔       𐑲
  Γ  Interaction gr. →  ɢ        and(0)  or(1)  seq(2)  broad(3)
     [exOS Γ ≡ IG ɢ]              ɢ^∧     ɢ^˝    ɢ^ˌ     ɢ^Ş
  Φ  Criticality     →  ⊙        sub(0)  c(1)  c_cmplx(2)  EP(3)  sup(4)
     [exOS Φ ≡ IG ⊙]              𐑢     ⊙   𐑮         𐑻    𐑣
  H  Chirality  →  Ħ        H0(0)  H1(1)  H2(2)  H_inf(3)
                                  𐑓     𐑒    𐑖    𐑫
  S  Stoichiometry   →  Σ        1:1(0)  n:n(1)  n:m(2)
                                  𐑙     𐑕     𐑳
  Ω  Winding         →  Ω        trivial(0)  Z2(1)  Z(2)
                                  𐑷         𐑴    𐑭
  ─────────────────────────────────────────────────────────────────────

OS imscription (MEET of five systems) in IG notation:
  ⟨ 𐑨  𐑶  𐑽  𐑹  ƒ^ż  Ç^W  𐑲  ɢ^ˌ  ⊙  𐑖  𐑳  𐑭 ⟩
  Tier: O_∞  (⊙ + 𐑹)

Voynich crystal imscription in IG notation (from voynich-engine):
  ⟨ 𐑦  𐑸  𐑾  𐑹  ƒ^ì  Ç^Ù  𐑲  ɢ^Ş  ⊙  𐑫  𐑙  𐑭 ⟩
  Tier: O_∞

Rohonc crystal imscription in IG notation:
  ⟨ 𐑨  𐑶  𐑽  𐑹  ƒ^ì  Ç^@  𐑲  ɢ^ˌ  ⊙  𐑖  𐑳  𐑭 ⟩
  Tier: O_∞  (⊙ + 𐑹)

Linear A = OS imscription exactly. Adding Linear A as a sixth system to the
exOS MEET leaves the invariant core unchanged. The grammar was already
complete. The Minoan system is not a derivative of the five — it IS the
structural core they all share.

IG distances (exOS weighted metric, weights from aleph.rs):
  d(Linear A, OS imscription) = 0.00   — identical
  d(Linear A, Rohonc)         ≈ 2.10   — ƒ and Ç differ (ƒ^ż↔ƒ^ì, Ç^W↔Ç^@)
  d(Linear A, Voynich)        ≈ 4.31   — six primitives differ
  d(Rohonc,   OS imscription) ≈ 2.10   — same two primitives as Linear A↔Rohonc
  d(Rohonc,   Voynich)        ≈ 3.55
──────────────────────────────────────────────────────────────────────────────
"""

PRIMITIVES: dict[str, dict] = {
    'cu': {'opcode': 0x0, 'mnemonic': 'VINIT',  'operation': 'Initial object ∅',              'family': 'logical'},
    'hk': {'opcode': 0x1, 'mnemonic': 'TANCH',  'operation': 'Terminal anchor ⊤',             'family': 'logical'},
    'fa': {'opcode': 0x2, 'mnemonic': 'AFWD',   'operation': 'Morphism →',                    'family': 'logical'},
    'ba': {'opcode': 0x3, 'mnemonic': 'AREV',   'operation': 'Contravariant inversion ←',     'family': 'logical'},
    'lt': {'opcode': 0x4, 'mnemonic': 'CLINK',  'operation': 'Composition ∘',                 'family': 'logical'},
    'lp': {'opcode': 0x5, 'mnemonic': 'ISCRIB', 'operation': 'Identity id',                   'family': 'logical'},
    'br': {'opcode': 0x6, 'mnemonic': 'FSPLIT', 'operation': 'Frobenius co-multiplication δ', 'family': 'frobenius'},
    'cv': {'opcode': 0x7, 'mnemonic': 'FFUSE',  'operation': 'Frobenius multiplication μ',    'family': 'frobenius'},
    'vt': {'opcode': 0x8, 'mnemonic': 'EVALT',  'operation': 'Lattice: True',                 'family': 'dialetheia'},
    'hz': {'opcode': 0x9, 'mnemonic': 'EVALF',  'operation': 'Lattice: False',                'family': 'dialetheia'},
    'cl': {'opcode': 0xA, 'mnemonic': 'ENGAGR', 'operation': 'Lattice: Both (paradox)',       'family': 'dialetheia'},
    'dt': {'opcode': 0xB, 'mnemonic': 'IFIX',   'operation': 'Linear tape write',             'family': 'linear'},
}

FLUX = {
    '00': 'Void',
    '01': 'True',
    '10': 'False',
    '11': 'Both',
}

BOOTSTRAP_SEQUENCE = ['lp', 'ba', 'br', 'fa', 'cv', 'lt', 'dt', 'lp']

# Linear A tablet sections (primary corpus: Haghia Triada; secondary: Knossos, Zakros)
SECTIONS = [
    (range(1,   40),  'haghia_triada',  'darkgoldenrod'),
    (range(40,  80),  'knossos',        'royalblue'),
    (range(80,  120), 'zakros',         'seagreen'),
    (range(120, 160), 'other_palatial', 'mediumpurple'),
]

# ── Crystal imscriptions (IG notation, numeric form) ─────────────────────────
# Index order: [Ð, Þ, Ř, Φ, ƒ, Ç, Γ, ɢ, ⊙, Ħ, Σ, Ω]
# Tier condition: ⊙ (index 8 = 1) AND 𐑹 (index 3 = 4) → O_∞

LINEAR_A_IMSCRIPTION = [1, 3, 2, 4, 2, 1, 2, 2, 1, 2, 2, 2]   # = OS_IMSCRIPTION exactly
OS_IMSCRIPTION       = [1, 3, 2, 4, 2, 1, 2, 2, 1, 2, 2, 2]
ROHONC_IMSCRIPTION   = [1, 3, 2, 4, 0, 2, 2, 2, 1, 2, 2, 2]
VOYNICH_IMSCRIPTION  = [3, 4, 3, 4, 0, 3, 2, 3, 1, 3, 0, 2]

# exOS distance weights (aleph.rs WEIGHTS, positions 0–11)
IG_WEIGHTS           = [10000, 10000, 10000, 12000, 9000, 8000, 10000, 10000, 11000, 8000, 10000, 7000]
