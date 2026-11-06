"""
Sectional call-graph generator — Linear A edition.

Produces per-tablet register-flow graphs colour-coded by corpus section
(haghia_triada, knossos, zakros, other_palatial). Optionally animates the
full engine execution as a tablet-by-tablet progression (requires ffmpeg).

Section boundaries follow the primary corpus distribution:
  t1–t39    haghia_triada  (largest palatial archive, HT tablets)
  t40–t79   knossos        (LM IB destruction deposits)
  t80–t119  zakros         (eastern palace archive)
  t120–t159 other_palatial (Akrotiri, Malia, Palaikastro, etc.)
"""

from __future__ import annotations
import re
from pathlib import Path

import networkx as nx

from .callgraph import build_graph, largest_component
from .primitives import SECTIONS

_REG_PATTERN = re.compile(r'%r(\d+)')


def classify_tablet(tablet: str) -> tuple[str, str]:
    """Return (section_name, colour) for a tablet identifier."""
    m = re.match(r't?(\d+)', tablet.lower())
    if not m:
        return 'other', 'gray'
    n = int(m.group(1))
    for rng, name, color in SECTIONS:
        if n in rng:
            return name, color
    return 'other', 'gray'


def _tablet_instructions(source) -> dict[str, list[str]]:
    if isinstance(source, dict):
        return {name: data['instructions'] for name, data in source['pages'].items()}

    path = Path(source)
    result: dict[str, list[str]] = {}
    current: str | None = None
    for line in path.read_text(encoding='utf-8', errors='ignore').splitlines():
        stripped = line.strip()
        if stripped.startswith('=== ') and stripped.endswith(' ==='):
            current = stripped[4:-4].lower()
            result[current] = []
        elif current is not None and '%r' in line:
            result[current].append(stripped)
    return result


def _sort_key(name: str) -> int:
    m = re.match(r't?(\d+)', name.lower())
    return int(m.group(1)) if m else 0


def _render_tablet(G, color: str, section: str, tablet: str, output_dir: Path, dpi: int) -> None:
    import matplotlib.pyplot as plt

    plt.figure(figsize=(24, 24))
    pos = nx.spring_layout(G, k=0.15, iterations=80, seed=42)
    nx.draw(G, pos,
            node_size=60, alpha=0.9, with_labels=True, font_size=8,
            node_color=color, edge_color='darkgoldenrod', arrows=True, arrowsize=12)
    plt.title(
        f"Linear A {tablet} — {section.upper()} corpus\n"
        f"({G.number_of_nodes()} nodes, {G.number_of_edges()} edges)",
        fontsize=16,
    )
    out = output_dir / f"{tablet}_{section}.png"
    plt.savefig(str(out), dpi=dpi, bbox_inches='tight')
    plt.close()


def _animate(tablet_nodes: dict[str, set[int]], G_full, output_dir: Path) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    print("Rendering animation (requires ffmpeg) ...")
    tab_list = sorted(tablet_nodes.keys(), key=_sort_key)
    all_nodes = list(G_full.nodes())
    pos = nx.spring_layout(G_full, k=0.1, iterations=100, seed=42)

    fig, ax = plt.subplots(figsize=(28, 28))

    def update(frame):
        ax.clear()
        current = tab_list[frame % len(tab_list)]
        highlight = tablet_nodes[current]
        section, color = classify_tablet(current)
        node_colors = [color if n in highlight else 'lightgray' for n in all_nodes]
        nx.draw(G_full, pos, ax=ax,
                node_size=40, alpha=0.85, with_labels=True, font_size=6,
                node_color=node_colors, edge_color='darkgoldenrod', arrows=True)
        ax.set_title(f"Engine — {current} [{section}] (frame {frame})", fontsize=14)
        return (ax,)

    ani = FuncAnimation(fig, update, frames=min(200, len(tab_list)), interval=300, repeat=True)
    out = str(output_dir / 'linear_a_full_execution_animation.mp4')
    ani.save(out, writer='ffmpeg', fps=4, dpi=200)
    plt.close()
    print(f"Animation saved: {out}")


def generate_sectional_graphs(
    source,
    output_dir: str | Path = 'linear_a_graphs',
    animate: bool = False,
    min_nodes: int = 5,
    dpi: int = 300,
) -> dict[str, tuple]:
    """
    Generate per-tablet register-flow graphs, colour-coded by corpus section.

    source:     compile_corpus() result dict, or path to a log file (str/Path)
    output_dir: directory for PNG files (and animation MP4 if animate=True)
    animate:    render a tablet-progression MP4 (requires ffmpeg)
    min_nodes:  skip tablets whose component has fewer nodes than this
    Returns:    {tablet_name: (full_graph, component_graph)}
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Generating sectional graphs → {output_dir}/")

    by_tablet = _tablet_instructions(source)
    results: dict[str, tuple] = {}
    tablet_nodes: dict[str, set[int]] = {}
    G_full = nx.DiGraph()

    for tablet, instructions in sorted(by_tablet.items(), key=lambda kv: _sort_key(kv[0])):
        G = build_graph(instructions)
        G_full = nx.compose(G_full, G)

        nodes = {int(r) for line in instructions for r in _REG_PATTERN.findall(line)}
        if nodes:
            tablet_nodes[tablet] = nodes

        C = largest_component(G)
        if C.number_of_nodes() < min_nodes:
            continue

        section, color = classify_tablet(tablet)
        _render_tablet(C, color, section, tablet, output_dir, dpi)
        results[tablet] = (G, C)
        print(f"  {tablet} [{section}] — {C.number_of_nodes()} nodes, {C.number_of_edges()} edges")

    print(f"\nFull composite graph: {G_full.number_of_nodes()} nodes, {G_full.number_of_edges()} edges")

    if animate:
        _animate(tablet_nodes, G_full, output_dir)

    print(f"\n=== {len(results)} sectional graphs written to {output_dir}/ ===")
    return results


def main() -> None:
    import argparse
    from .compiler import compile_corpus

    parser = argparse.ArgumentParser(description='Generate per-section Linear A call graphs')
    parser.add_argument('transcription', help='LATFF transcription or compiled log file')
    parser.add_argument('--output-dir', default='linear_a_graphs')
    parser.add_argument('--animate', action='store_true')
    parser.add_argument('--min-nodes', type=int, default=5, metavar='N')
    parser.add_argument('--dpi', type=int, default=300)
    args = parser.parse_args()

    path = Path(args.transcription)
    source = compile_corpus(path) if path.suffix == '.txt' else path

    generate_sectional_graphs(
        source,
        output_dir=args.output_dir,
        animate=args.animate,
        min_nodes=args.min_nodes,
        dpi=args.dpi,
    )


if __name__ == '__main__':
    main()
