"""Summary figure for the README: CHSH value S measured in the lab sessions.

Values are copied from the outputs of the notebooks:
  notebooks/4_CHSH-Bell-inequality.ipynb        (Aer simulator and IBM Quantum run 1)
  notebooks/5_lab-answers-sessions-1-3_ES.ipynb (IBM Quantum run 2)
Error bars are the standard errors returned by the Qiskit Estimator, added in quadrature.
Usage: python figures/make_chsh_figure.py  (writes the PNGs next to this script)
"""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))

rows = [  # label, S, error
    ("Aer simulator", 2.8284, 0.0220),
    ("IBM Quantum, run 1", 2.7881, 0.0268),
    ("IBM Quantum, run 2", 2.9010, 0.0278),
]
tsirelson = 2 * np.sqrt(2)

themes = {
    "light": dict(bg="#ffffff", fg="#1f2328", muted="#59636e", grid="#d1d9e0",
                  region="#f6f8fa", mark="#1c5cab"),
    "dark": dict(bg="#0d1117", fg="#e6edf3", muted="#9198a1", grid="#3d444d",
                 region="#161b22", mark="#6da7ec"),
}

for name, t in themes.items():
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 11, "mathtext.fontset": "dejavusans",
        "text.color": t["fg"], "axes.labelcolor": t["fg"], "xtick.color": t["muted"], "ytick.color": t["fg"],
        "axes.edgecolor": t["grid"], "figure.facecolor": t["bg"], "axes.facecolor": t["bg"],
    })
    fig, ax = plt.subplots(figsize=(9, 3.8))
    x0, x1 = 1.8, 3.05
    ax.axvspan(x0, 2.0, color=t["region"], zorder=0)
    ax.axvline(2.0, color=t["muted"], lw=1.0, zorder=1)
    ax.axvline(tsirelson, color=t["muted"], lw=1.0, ls=(0, (4, 3)), zorder=1)
    ytop = len(rows) + 0.3
    ax.text(1.99, ytop, "local realism\n" + r"$|S|\leq 2$", ha="right", va="top", fontsize=10, color=t["muted"])
    ax.text(tsirelson - 0.01, ytop, "quantum maximum\n" + r"$2\sqrt{2}$", ha="right", va="top", fontsize=10,
            color=t["muted"])
    for i, (label, s, e) in enumerate(rows):
        y = len(rows) - 1 - i
        ax.errorbar(s, y, xerr=e, fmt="o", ms=8, color=t["mark"], ecolor=t["mark"], elinewidth=2,
                    capsize=4, capthick=2, markeredgecolor=t["bg"], markeredgewidth=2, zorder=3)
        ax.text(s + e + 0.02, y, f"{s:.3f} ± {e:.3f}", va="center", fontsize=10, color=t["fg"])
    ax.set_yticks(range(len(rows)), [r[0] for r in reversed(rows)])
    ax.set_ylim(-0.6, len(rows) + 0.4)
    ax.set_xlim(x0, x1)
    ax.set_xticks([1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0])
    ax.grid(axis="x", color=t["grid"], lw=0.6, zorder=0)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0, pad=8)
    ax.set_xlabel(r"CHSH value  $S=\langle A_1B_1\rangle+\langle A_1B_2\rangle+\langle A_2B_1\rangle-\langle A_2B_2\rangle$")
    ax.set_title("Bell (CHSH) test on the singlet state", fontsize=12, loc="left", color=t["fg"], pad=10)
    fig.tight_layout()
    fig.savefig(f"{out_dir}/chsh_{name}.png", dpi=150, facecolor=t["bg"])
    plt.close(fig)
print("ok")
