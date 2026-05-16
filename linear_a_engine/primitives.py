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
  ⟨ Ð_C  Þ_¨  Ř_Ť  Φ_}  ƒ^ż  Ç^W  Γ_ʔ  ɢ^ˌ  ⊙_ÿ  Ħ_A  Σ_ï  Ω_z ⟩
  Tier: O_∞  (⊙_ÿ + Φ_})

The exOS OS imscription is the component-wise MEET of five ancient writing
systems (Hebrew, Sanskrit, Egyptian, Cuneiform, Basque), expressed in exOS
notation as [D=1,T=3,R=2,P=4,F=2,K=1,G=2,Γ=2,Φ=1,H=2,S=2,Ω=2].

Translated into IG notation (SYMBOL_REFERENCE.md):

  exOS primitive → IG primitive   (value mapping)
  ─────────────────────────────────────────────────────────────────────
  D  Dimensionality  →  Ð        wedge(0)   triangle(1)  infty(2)   holo(3)
                                  Ð_ß        Ð_C          Ð_;        Ð_ω
  T  Topology        →  Þ        net(0)  in(1)  bowtie(2)  box(3)  odot(4)
                                  Þ_6     Þ_K    Þ_ò        Þ_¨     Þ_O
  R  Relational mode →  Ř        super(0)  cat(1)  dagger(2)  lr(3)
                                  Ř_¯       Ř_ý     Ř_Ť        Ř_=
  P  Parity/symmetry →  Φ        asym(0)  psi(1)  pm(2)  sym(3)  pm_sym(4)
     [NOTE: exOS P ≡ IG Φ;        Φ_ɐ      Φ_υ     Φ_F    Φ_˙     Φ_}
      exOS Φ ≡ IG ⊙]
  F  Fidelity        →  ƒ        ell(0)  eth(1)  hbar(2)
                                  ƒ^ì     ƒ^ð     ƒ^ż
  K  Kinetics        →  Ç        fast(0)  mod(1)  slow(2)  trap(3)  MBL(4)
                                  Ç^-      Ç^W     Ç^@      Ç^Ù      Ç^λ
  G  Scope/gran.     →  Γ        beth(0)  gimel(1)  aleph(2)
                                  Γ_β      Γ_γ       Γ_ʔ
  Γ  Interaction gr. →  ɢ        and(0)  or(1)  seq(2)  broad(3)
     [exOS Γ ≡ IG ɢ]              ɢ^∧     ɢ^˝    ɢ^ˌ     ɢ^Ş
  Φ  Criticality     →  ⊙        sub(0)  c(1)  c_cmplx(2)  EP(3)  sup(4)
     [exOS Φ ≡ IG ⊙]              ⊙_ž     ⊙_ÿ   ⊙_Æ         ⊙_3    ⊙_Ţ
  H  Chirality  →  Ħ        H0(0)  H1(1)  H2(2)  H_inf(3)
                                  Ħ_Ñ     Ħ_£    Ħ_A    Ħ_!
  S  Stoichiometry   →  Σ        1:1(0)  n:n(1)  n:m(2)
                                  Σ_S     Σ_ő     Σ_ï
  Ω  Winding         →  Ω        trivial(0)  Z2(1)  Z(2)
                                  Ω_Å         Ω_2    Ω_z
  ─────────────────────────────────────────────────────────────────────

OS imscription (MEET of five systems) in IG notation:
  ⟨ Ð_C  Þ_¨  Ř_Ť  Φ_}  ƒ^ż  Ç^W  Γ_ʔ  ɢ^ˌ  ⊙_ÿ  Ħ_A  Σ_ï  Ω_z ⟩
  Tier: O_∞  (⊙_ÿ + Φ_})

Voynich crystal imscription in IG notation (from voynich-engine):
  ⟨ Ð_ω  Þ_O  Ř_=  Φ_}  ƒ^ì  Ç^Ù  Γ_ʔ  ɢ^Ş  ⊙_ÿ  Ħ_!  Σ_S  Ω_z ⟩
  Tier: O_∞

Rohonc crystal imscription in IG notation:
  ⟨ Ð_C  Þ_¨  Ř_Ť  Φ_}  ƒ^ì  Ç^@  Γ_ʔ  ɢ^ˌ  ⊙_ÿ  Ħ_A  Σ_ï  Ω_z ⟩
  Tier: O_∞  (⊙_ÿ + Φ_})

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
# Tier condition: ⊙_ÿ (index 8 = 1) AND Φ_} (index 3 = 4) → O_∞

LINEAR_A_IMSCRIPTION = [1, 3, 2, 4, 2, 1, 2, 2, 1, 2, 2, 2]   # = OS_IMSCRIPTION exactly
OS_IMSCRIPTION       = [1, 3, 2, 4, 2, 1, 2, 2, 1, 2, 2, 2]
ROHONC_IMSCRIPTION   = [1, 3, 2, 4, 0, 2, 2, 2, 1, 2, 2, 2]
VOYNICH_IMSCRIPTION  = [3, 4, 3, 4, 0, 3, 2, 3, 1, 3, 0, 2]

# exOS distance weights (aleph.rs WEIGHTS, positions 0–11)
IG_WEIGHTS           = [10000, 10000, 10000, 12000, 9000, 8000, 10000, 10000, 11000, 8000, 10000, 7000]
