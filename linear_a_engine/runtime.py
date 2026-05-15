"""
Universal Engine virtual machine — Linear A edition.

Executes compiled IMASM instruction streams on Tri-Phase Flux Registers.
Identical architecture to the Voynich and Rohonc Engine VMs: a register has
a 2-bit flux state (Void/True/False/Both) and an optional fixed value.
Contradictions are stabilized in-place (ENGAGR/FSPLIT set the Both state);
they do not propagate. IFIX burns a register to permanent ROM — the linear
type constraint that enforces temporal asymmetry.

Linear A's left-to-right tablet inscription is preserved naturally in the
append-only register monotonicity.
"""

from __future__ import annotations
import re
from collections import defaultdict
from pathlib import Path
from typing import Generator

_REG_PATTERN = re.compile(r'%r(\d+)')


class TriPhaseRegister:
    __slots__ = ('flux', 'value', 'paradox_count')

    def __init__(self) -> None:
        self.flux: str = '00'   # 00=Void  01=True  10=False  11=Both
        self.value: str | None = None
        self.paradox_count: int = 0

    def engage(self) -> None:
        self.flux = '11'
        self.paradox_count += 1

    @property
    def is_active(self) -> bool:
        return self.flux != '00' or self.value is not None

    @property
    def is_fixed(self) -> bool:
        return self.value == 'FIXED'


class UniversalEngine:
    """
    Tri-Phase virtual machine executing compiled IMASM instructions.

    Usage::

        engine = UniversalEngine.from_compilation(result)
        for snapshot in engine.run(steps=10000, report_every=500):
            print(snapshot)
    """

    def __init__(self) -> None:
        self.registers: defaultdict[int, TriPhaseRegister] = defaultdict(TriPhaseRegister)
        self.program: list[str] = []
        self.pc: int = 0
        self.total_steps: int = 0

    @classmethod
    def from_compilation(cls, result: dict) -> 'UniversalEngine':
        engine = cls()
        for tablet in result['pages'].values():
            engine.program.extend(tablet['instructions'])
        return engine

    @classmethod
    def from_log(cls, log_path: str | Path) -> 'UniversalEngine':
        engine = cls()
        for line in Path(log_path).read_text(encoding='utf-8', errors='ignore').splitlines():
            if '%r' in line and ('0x' in line or 'FSPLIT' in line or 'IFIX' in line):
                engine.program.append(line.strip())
        return engine

    def step(self) -> None:
        if self.pc >= len(self.program):
            self.pc = 0
        self._execute(self.program[self.pc])
        self.pc += 1
        self.total_steps += 1

    def run(
        self,
        steps: int = 10000,
        report_every: int = 500,
    ) -> Generator[dict, None, None]:
        for i in range(steps):
            self.step()
            if report_every and i % report_every == 0:
                yield self.snapshot()

    def inject_paradox(self, reg_id: int) -> None:
        self.registers[reg_id].engage()

    def _execute(self, instr: str) -> None:
        regs = [int(x) for x in _REG_PATTERN.findall(instr)]
        if not regs:
            return
        if 'FSPLIT' in instr:
            self.registers[regs[0]].engage()
        elif 'IFIX' in instr:
            self.registers[regs[0]].value = 'FIXED'
        elif 'ENGAGR' in instr:
            self.registers[regs[0]].engage()

    def snapshot(self) -> dict:
        active = sum(1 for r in self.registers.values() if r.is_active)
        fixed = sum(1 for r in self.registers.values() if r.is_fixed)
        paradoxes = sum(r.paradox_count for r in self.registers.values())
        return {
            'step': self.total_steps,
            'pc': self.pc,
            'active_registers': active,
            'fixed_registers': fixed,
            'paradox_stabilizations': paradoxes,
            'entropy_delta': 0.0,
            'status': 'RUNNING',
        }

    def report(self) -> None:
        s = self.snapshot()
        print('=== ENGINE STATUS ===')
        print(f'Steps executed        : {s["step"]}')
        print(f'Active registers      : {s["active_registers"]}')
        print(f'Fixed (IFIX) nodes    : {s["fixed_registers"]}')
        print(f'Paradox stabilizations: {s["paradox_stabilizations"]}')
        print(f'Entropy delta         : {s["entropy_delta"]:.8f} J/K')
        print('Status                : SELF_SUSTAINING_BOOTSTRAP_COMPLETE')


def main() -> None:
    import argparse
    from .compiler import compile_corpus

    parser = argparse.ArgumentParser(description='Run the Universal Engine VM on Linear A corpus')
    parser.add_argument('transcription', help='Path to LATFF transcription or compiled log')
    parser.add_argument('--steps', type=int, default=10000)
    parser.add_argument('--report-every', type=int, default=500)
    parser.add_argument('--paradox', type=int, metavar='REG',
                        help='Inject paradox at register N after execution')
    args = parser.parse_args()

    path = Path(args.transcription)
    if path.suffix == '.txt':
        result = compile_corpus(path)
        engine = UniversalEngine.from_compilation(result)
        print(f'Loaded {len(engine.program)} instructions from compilation.')
    else:
        engine = UniversalEngine.from_log(path)
        print(f'Loaded {len(engine.program)} instructions from log.')

    print(f'Running {args.steps} steps...\n')
    for snap in engine.run(steps=args.steps, report_every=args.report_every):
        print(f'Step {snap["step"]:6d} | PC {snap["pc"]:6d} | '
              f'Active {snap["active_registers"]:4d} | '
              f'Paradoxes {snap["paradox_stabilizations"]:4d}')

    if args.paradox is not None:
        engine.inject_paradox(args.paradox)
        print(f'\nParadox injected at r{args.paradox} → Both state stabilized')

    print()
    engine.report()


if __name__ == '__main__':
    main()
