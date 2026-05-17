"""
Animated full-corpus IMASM CFG — Linear A.

Uses the complete compiled instruction stream (all tablets concatenated).
Register ID aliasing across tablets creates genuine cycles: cross-tablet
back-edges form the looping nested structure.

Animation:
  Phase 1 — build: nodes appear in instruction order; tablet-boundary
             crossings flash white; hub nodes grow large.
  Phase 2 — flow wave: Gaussian pulse travels through execution order;
             cross-tablet back-edges light up amber when the wave fires
             through them; hub nodes (high degree) pulse harder.

Output: docs/animated_cfg_corpus.gif
"""

from __future__ import annotations
import io
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import networkx as nx

from linear_a_engine.compiler import compile_corpus
from linear_a_engine.callgraph import build_graph, largest_component

TRANSCRIPTION = root / "data" / "linear_a_latff_sample.txt"
OUT = root / "docs" / "animated_cfg_corpus.gif"

BG = "#0d0d1a"

_FAMILY_COLOR: dict[str, str] = {
    "FSPLIT": "#4e79a7",
    "FFUSE":  "#4e79a7",
    "AFWD":   "#f28e2b",
    "AREV":   "#f28e2b",
    "CLINK":  "#f28e2b",
    "ISCRIB": "#59a14f",
    "IFIX":   "#59a14f",
    "EVALT":  "#e15759",
    "EVALF":  "#e15759",
    "ENGAGR": "#e15759",
    "VINIT":  "#9c9c9c",
    "TANCH":  "#9c9c9c",
}
_FROBENIUS    = {"FSPLIT", "FFUSE"}
_PULSE_WHITE  = np.array(mcolors.to_rgba("#ffffff"))
_PULSE_AMBER  = np.array(mcolors.to_rgba("#ffb347"))
_TABLET_FLASH = np.array(mcolors.to_rgba("#cc44ff"))


def parse_flat_instructions(
    sections: dict,
) -> tuple[list[tuple[int, str]], list[int]]:
    parsed: list[tuple[int, str]] = []
    boundaries: list[int] = []
    for section_data in sections.values():
        boundaries.append(len(parsed))
        for line in section_data["instructions"]:
            m = re.match(r"\s*0x[0-9a-fA-F]+\s*\|\s*(\w+)\s+%r(\d+)", line)
            if m:
                parsed.append((int(m.group(2)), m.group(1)))
    return parsed, boundaries


def render_frame(
    ax: plt.Axes,
    all_nodes: list[int],
    pos: dict,
    edges: list,
    mnem_map: dict[int, str],
    base_colors: np.ndarray,
    base_sizes: np.ndarray,
    crosstablet_edge_set: set[tuple[int, int]],
    revealed: set[int] | None,
    tablet_flash: bool,
    pulse_center: int | None,
    pulse_sigma: int,
    N: int,
    title_str: str,
) -> None:
    ax.clear()
    ax.set_facecolor(BG)
    ax.set_axis_off()
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.15)
    ax.set_title(title_str, color="white", fontsize=8, pad=6)

    xs = np.array([pos[n][0] for n in all_nodes])
    ys = np.array([pos[n][1] for n in all_nodes])

    if revealed is not None:
        for u, v, d in edges:
            if u not in revealed or v not in revealed:
                continue
            is_ct = (u, v) in crosstablet_edge_set or (v, u) in crosstablet_edge_set
            is_fr = mnem_map.get(u, "") in _FROBENIUS or mnem_map.get(v, "") in _FROBENIUS
            if is_ct:
                col, lw, al = "#cc44ff", 2.0, 0.80
            elif is_fr:
                col, lw, al = "#f28e2b", 1.8, 0.65
            else:
                col, lw, al = "#3a5f80", 0.8, 0.30
            ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]],
                    color=col, lw=lw, alpha=al, zorder=1)

        vis_idx = [i for i, n in enumerate(all_nodes) if n in revealed]
        if not vis_idx:
            return

        colors = base_colors[vis_idx].copy()
        sizes  = base_sizes[vis_idx].copy()

        if tablet_flash:
            colors = np.ones_like(colors) * _TABLET_FLASH
            sizes  = sizes * 1.8

        ax.scatter(xs[vis_idx], ys[vis_idx],
                   c=colors, s=sizes, zorder=3, linewidths=0)

    else:
        dists   = np.abs(np.arange(N) - pulse_center)
        dists   = np.minimum(dists, N - dists)
        weights = np.exp(-0.5 * (dists / pulse_sigma) ** 2)

        active_ct_nodes: set[int] = set()
        for idx, n in enumerate(all_nodes):
            if weights[idx] > 0.4:
                active_ct_nodes.add(n)

        for u, v, d in edges:
            is_ct = (u, v) in crosstablet_edge_set or (v, u) in crosstablet_edge_set
            is_fr = mnem_map.get(u, "") in _FROBENIUS or mnem_map.get(v, "") in _FROBENIUS
            near  = u in active_ct_nodes or v in active_ct_nodes

            if is_ct and near:
                col, lw, al = "#ffb347", 2.8, 0.90
            elif is_ct:
                col, lw, al = "#cc44ff", 1.6, 0.55
            elif is_fr:
                col, lw, al = "#f28e2b", 1.6, 0.55
            else:
                col, lw, al = "#3a5f80", 0.7, 0.22
            ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]],
                    color=col, lw=lw, alpha=al, zorder=1)

        blended = np.empty_like(base_colors)
        for i, n in enumerate(all_nodes):
            w = weights[i]
            is_hub_ct = any(
                (n, nb) in crosstablet_edge_set or (nb, n) in crosstablet_edge_set
                for nb in list(active_ct_nodes)[:8]
            )
            target = _PULSE_AMBER if is_hub_ct and w > 0.2 else _PULSE_WHITE
            blended[i] = base_colors[i] * (1 - w) + target * w
        blended = np.clip(blended, 0, 1)

        sizes = base_sizes + base_sizes * 1.5 * weights

        ax.scatter(xs, ys, c=blended, s=sizes, zorder=3, linewidths=0)


def fig_to_pil(fig: plt.Figure, dpi: int) -> Image.Image:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, facecolor=BG, bbox_inches="tight")
    buf.seek(0)
    return Image.open(buf).copy()


def main(
    build_frames: int = 60,
    flow_frames: int = 100,
    fps: int = 18,
    dpi: int = 110,
    figsize: tuple[float, float] = (9, 9),
) -> None:
    print("Compiling corpus …")
    result = compile_corpus(TRANSCRIPTION)
    sections = result["pages"]
    section_count = result["page_count"]
    print(f"  {section_count} tablets, {result['total_registers']} total registers")

    parsed, boundaries = parse_flat_instructions(sections)

    all_instr: list[str] = []
    for data in sections.values():
        all_instr.extend(data["instructions"])

    print("Building graph …")
    G = build_graph(all_instr)
    C = largest_component(G)
    print(f"  Largest component: {C.number_of_nodes()} nodes, {C.number_of_edges()} edges")

    crosstablet_edge_set: set[tuple[int, int]] = set()
    for u, v, d in C.edges(data=True):
        if v < u:
            crosstablet_edge_set.add((u, v))
    print(f"  Cross-tablet back-edges: {len(crosstablet_edge_set)}")

    seen: set[int] = set()
    node_order: list[int] = []
    for r, _ in parsed:
        if r in C.nodes() and r not in seen:
            seen.add(r)
            node_order.append(r)
    N = len(node_order)

    mnem_map: dict[int, str] = {}
    for r, m in parsed:
        if r not in mnem_map:
            mnem_map[r] = m

    edges = list(C.edges(data=True))
    degrees = dict(C.degree())

    print(f"  Layout ({N} nodes) …")
    pos = nx.spring_layout(C, k=0.04, iterations=300, seed=42)

    base_colors = np.array([
        mcolors.to_rgba(_FAMILY_COLOR.get(mnem_map.get(n, ""), "#cccccc"))
        for n in node_order
    ])
    max_deg = max(degrees.values()) if degrees else 1
    base_sizes = np.array([
        12 + 60 * (np.log1p(degrees.get(n, 1)) / np.log1p(max_deg)) ** 1.5
        for n in node_order
    ])

    tablet_node_positions: set[int] = set()
    for bi in boundaries:
        if bi < len(parsed):
            r = parsed[bi][0]
            if r in seen and r in node_order:
                tablet_node_positions.add(node_order.index(r))

    pulse_sigma   = max(8, N // 16)
    pulse_centers = np.linspace(0, N - 1, flow_frames).astype(int)
    total_frames  = build_frames + flow_frames

    print(f"  Rendering {total_frames} frames …")
    fig, ax = plt.subplots(figsize=figsize, facecolor=BG)
    frames_pil: list[Image.Image] = []

    for f in range(total_frames):
        print(f"\r  {(f+1)/total_frames*100:5.1f}%  frame {f+1}/{total_frames}", end="", flush=True)

        if f < build_frames:
            frac     = (f + 1) / build_frames
            k        = max(1, int(frac * N))
            revealed = set(node_order[:k])
            flash    = any(abs(k - fp) <= 1 for fp in tablet_node_positions)
            tab_idx  = sum(1 for bi in boundaries if (bi // max(1, len(parsed) // N)) < k)
            title = (
                f"Linear A — full corpus | build {k}/{N} nodes | "
                f"tablet ~{tab_idx}/{section_count} | "
                f"{len(crosstablet_edge_set)} cross-tablet loops"
            )
            render_frame(
                ax, node_order, pos, edges, mnem_map,
                base_colors, base_sizes, crosstablet_edge_set,
                revealed=revealed, tablet_flash=flash,
                pulse_center=None, pulse_sigma=pulse_sigma, N=N,
                title_str=title,
            )
        else:
            fi     = f - build_frames
            center = pulse_centers[fi]
            node_at = node_order[center]
            mnem_at = mnem_map.get(node_at, "")
            title = (
                f"Linear A — full corpus | flow wave | "
                f"%r{node_at} {mnem_at} | "
                f"{len(crosstablet_edge_set)} cross-tablet loops"
            )
            render_frame(
                ax, node_order, pos, edges, mnem_map,
                base_colors, base_sizes, crosstablet_edge_set,
                revealed=None, tablet_flash=False,
                pulse_center=center, pulse_sigma=pulse_sigma, N=N,
                title_str=title,
            )

        frames_pil.append(fig_to_pil(fig, dpi))

    print()
    plt.close(fig)

    duration_ms = 1000 // fps
    OUT.parent.mkdir(parents=True, exist_ok=True)
    print(f"Assembling GIF → {OUT} …")
    frames_rgb = [f.convert("RGB") for f in frames_pil]
    frames_rgb[0].save(
        str(OUT),
        save_all=True,
        append_images=frames_rgb[1:],
        duration=duration_ms,
        loop=0,
        optimize=False,
    )
    sz = OUT.stat().st_size / (1024 * 1024)
    print(f"Done: {OUT}  ({sz:.1f} MB)")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--build-frames", type=int, default=60)
    ap.add_argument("--flow-frames",  type=int, default=100)
    ap.add_argument("--fps",  type=int, default=18)
    ap.add_argument("--dpi",  type=int, default=110)
    args = ap.parse_args()
    main(
        build_frames=args.build_frames,
        flow_frames=args.flow_frames,
        fps=args.fps,
        dpi=args.dpi,
    )
