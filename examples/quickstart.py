"""
Linear A Engine — quickstart example.

Compiles the sample LATFF transcription, runs the VM for 5000 steps,
and generates sectional call graphs for all four corpus sections.
"""

from pathlib import Path
from linear_a_engine import (
    compile_corpus,
    UniversalEngine,
    generate_sectional_graphs,
)

DATA = Path(__file__).parent.parent / 'data' / 'linear_a_latff_sample.txt'

print('=== LINEAR A ENGINE — QUICKSTART ===\n')

result = compile_corpus(DATA, verbose=True)
print(f'\nTablets compiled  : {result["page_count"]}')
print(f'Total instructions: {result["total_instructions"]}')
print(f'Total registers   : {result["total_registers"]}')
print(f'Entropy delta     : {result["entropy_delta"]:.8f} J/K')

print('\nPeak tablets by register density:')
from linear_a_engine.compiler import peak_tablets
for name, regs in peak_tablets(result, n=5):
    print(f'  {name}: {regs} registers')

engine = UniversalEngine.from_compilation(result)
print(f'\nRunning 5000 steps...')
for snap in engine.run(steps=5000, report_every=1000):
    print(f'  step {snap["step"]:5d} | active {snap["active_registers"]:4d} | '
          f'paradoxes {snap["paradox_stabilizations"]:3d}')

print()
engine.report()

print('\nGenerating sectional graphs...')
generate_sectional_graphs(result, output_dir='linear_a_graphs', min_nodes=3)
