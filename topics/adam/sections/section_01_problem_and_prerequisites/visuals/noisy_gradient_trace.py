from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle
import numpy as np


mpl.rcParams["svg.hashsalt"] = "wheels-adam-noisy-gradient-trace"

OUT_DIR = Path(__file__).resolve().parent
SVG_PATH = OUT_DIR / "noisy_gradient_trace.svg"
PNG_PATH = OUT_DIR / "noisy_gradient_trace.png"


BLUE = "#2f6f9f"
GREEN = "#2f7d4f"
GOLD = "#d9ca9a"
GOLD_FILL = "#f3e7b5"
INK = "#202124"
MUTED = "#555b61"
PANEL_EDGE = "#d9d7ce"
BG = "#fbfbf8"


def add_arrow(ax, start, end, color, lw=2.1, mutation_scale=9):
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=mutation_scale,
        linewidth=lw,
        color=color,
        shrinkA=0,
        shrinkB=0,
        capstyle="round",
        joinstyle="round",
    )
    ax.add_patch(arrow)


def draw_loss_curve(ax, x_offset):
    xs = np.linspace(0.08, 0.92, 120)
    ys = 0.80 - 0.12 * np.sin(xs * np.pi * 1.25) - 0.52 * xs**1.55
    ax.plot(x_offset + xs * 0.34, ys, color=GOLD, lw=4, alpha=0.55, zorder=1)


def draw_axes(ax, x0):
    ax.plot([x0, x0 + 0.36], [0.30, 0.30], color="#6f7378", lw=1.4)
    ax.plot([x0, x0], [0.30, 0.70], color="#6f7378", lw=1.4)
    ax.text(x0 + 0.18, 0.258, "parameter value theta", ha="center", va="center", fontsize=8.5, color=MUTED)
    ax.text(x0 - 0.035, 0.50, "loss", ha="center", va="center", rotation=90, fontsize=8.5, color=MUTED)


def draw_lower_loss(ax, cx, cy):
    circ = Circle((cx, cy), 0.035, facecolor=GOLD_FILL, edgecolor="#b9a46b", lw=1.2, zorder=3)
    ax.add_patch(circ)
    ax.text(cx, cy, "lower\nloss", ha="center", va="center", fontsize=7.5, color="#6e5b1f", zorder=4)


def draw_left_panel(ax):
    panel = Rectangle((0.055, 0.215), 0.405, 0.57, facecolor="white", edgecolor=PANEL_EDGE, lw=0.9)
    ax.add_patch(panel)
    ax.text(0.055, 0.905, "SGD reacts to the latest hint", fontsize=15, fontweight="bold", color=INK)
    ax.text(0.055, 0.858, "Each mini-batch gradient is useful,", fontsize=9, color=MUTED)
    ax.text(0.055, 0.827, "but it can wobble from step to step.", fontsize=9, color=MUTED)

    x0 = 0.105
    draw_axes(ax, x0)
    draw_loss_curve(ax, x0)
    draw_lower_loss(ax, 0.405, 0.335)

    points = [
        (0.137, 0.61),
        (0.185, 0.54),
        (0.242, 0.62),
        (0.295, 0.47),
        (0.36, 0.50),
        (0.397, 0.38),
    ]
    ax.plot([p[0] for p in points], [p[1] for p in points], color=BLUE, lw=1.8, zorder=5)
    ax.scatter([points[0][0]], [points[0][1]], s=22, color=BLUE, zorder=6)
    for start, end in zip(points[:-1], points[1:]):
        add_arrow(ax, start, end, BLUE)

    ax.text(0.147, 0.69, "step follows latest", fontsize=9, color=BLUE, fontweight="bold")
    ax.text(0.147, 0.666, "noisy gradient", fontsize=9, color=BLUE, fontweight="bold")
    ax.text(0.147, 0.635, "so hints can zigzag", fontsize=8.5, color=MUTED)


def draw_right_panel(ax):
    panel = Rectangle((0.54, 0.215), 0.405, 0.57, facecolor="white", edgecolor=PANEL_EDGE, lw=0.9)
    ax.add_patch(panel)
    ax.text(0.54, 0.905, "Adam keeps running estimates", fontsize=15, fontweight="bold", color=INK)
    ax.text(0.54, 0.858, "It does not know the best path.", fontsize=9, color=MUTED)
    ax.text(0.54, 0.827, "It shapes each step from recent history.", fontsize=9, color=MUTED)

    x0 = 0.59
    draw_axes(ax, x0)
    draw_loss_curve(ax, x0)
    draw_lower_loss(ax, 0.89, 0.335)

    path_x = np.array([0.635, 0.70, 0.765, 0.835, 0.877])
    path_y = np.array([0.61, 0.55, 0.47, 0.39, 0.355])
    ax.plot(path_x, path_y, color=GREEN, lw=2.1, zorder=5)
    ax.scatter([path_x[0], path_x[2]], [path_y[0], path_y[2]], s=[22, 16], color=GREEN, zorder=6)
    add_arrow(ax, (path_x[-2], path_y[-2]), (path_x[-1], path_y[-1]), GREEN, lw=2.1, mutation_scale=9)

    ax.text(0.66, 0.662, "current step shaped", fontsize=9, color=GREEN, fontweight="bold")
    ax.text(0.66, 0.636, "by m_t and v_t", fontsize=9, color=GREEN, fontweight="bold")

    callout = Rectangle((0.585, 0.075), 0.36, 0.12, facecolor="white", edgecolor="#cfcfcf", lw=0.9)
    ax.add_patch(callout)
    ax.text(0.602, 0.167, "Recent noisy gradients:", fontsize=7.4, color=INK, fontweight="bold")
    ax.text(0.602, 0.139, "g_{t-2}, g_{t-1}, g_t", fontsize=7.4, color=MUTED)
    ax.text(0.748, 0.167, "Adam summarizes them as:", fontsize=7.4, color=INK, fontweight="bold")
    ax.text(0.748, 0.139, "m_t = recent direction", fontsize=7.4, color=MUTED)
    ax.text(0.748, 0.111, "v_t = recent squared-gradient scale", fontsize=7.0, color=MUTED)


def build_figure():
    fig, ax = plt.subplots(figsize=(11, 6.4), dpi=160)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    draw_left_panel(ax)
    draw_right_panel(ax)

    ax.text(0.055, 0.115, "Conceptual teaching sketch, not a measured Adam result.", fontsize=9, color=MUTED)
    ax.text(0.055, 0.085, "Left: direct reactions to recent gradients.", fontsize=9, color=MUTED)
    ax.text(0.055, 0.055, "Right: state shapes the step; it does not know the optimum.", fontsize=9, color=MUTED)
    fig.subplots_adjust(left=0.02, right=0.985, top=0.96, bottom=0.05)
    return fig


def main():
    fig = build_figure()
    fig.savefig(SVG_PATH, format="svg", metadata={"Date": None})
    fig.savefig(PNG_PATH, format="png", metadata={"Software": "Wheels"})
    plt.close(fig)


if __name__ == "__main__":
    main()
