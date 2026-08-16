"""
Generates convergence plots for the DFG cylinder benchmark
(Re=20 Fluent sweep, Re=100 OpenFOAM sweep) from the CSVs in results/tables.
Outputs PNGs into results/figures.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TABLES = ROOT / "results" / "tables"
FIGURES = ROOT / "results" / "figures"

# ---------- Re=20 convergence (Fluent, 4 levels) ----------
df20 = pd.read_csv(TABLES / "re20_convergence.csv")
fluent20 = df20[df20["solver"] == "fluent"].sort_values("level")
ref20 = df20[df20["solver"] == "reference"].iloc[0]

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].plot(fluent20["cells"], fluent20["Cd"], "o-", label="Fluent")
axes[0].axhline(ref20["Cd"], color="k", linestyle="--", label="Featflow reference")
axes[0].set_xlabel("Cells")
axes[0].set_ylabel("Cd")
axes[0].set_title("Drag coefficient vs mesh")
axes[0].legend()

axes[1].plot(fluent20["cells"], fluent20["Cl"], "o-", label="Fluent")
axes[1].axhline(ref20["Cl"], color="k", linestyle="--", label="Featflow reference")
axes[1].axhline(0, color="gray", linewidth=0.5)
axes[1].set_xlabel("Cells")
axes[1].set_ylabel("Cl")
axes[1].set_title("Lift coefficient vs mesh (sign instability)")
axes[1].legend()

axes[2].plot(fluent20["cells"], fluent20["p_diff"], "o-", label="Fluent")
axes[2].axhline(ref20["p_diff"], color="k", linestyle="--", label="Featflow reference")
axes[2].set_xlabel("Cells")
axes[2].set_ylabel("p_diff [Pa]")
axes[2].set_title("Pressure difference vs mesh")
axes[2].legend()

plt.tight_layout()
plt.savefig(FIGURES / "re20_fluent_convergence.png", dpi=150)
plt.close()

# ---------- Re=100 convergence (OpenFOAM, 4 levels) ----------
df100 = pd.read_csv(TABLES / "re100_convergence.csv")
of100 = df100[df100["solver"] == "openfoam"].sort_values("level")
ref100 = df100[df100["solver"] == "reference"].iloc[0]

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].plot(of100["level"], of100["meanCd"], "o-", label="OpenFOAM")
axes[0].axhline(ref100["meanCd"], color="k", linestyle="--", label="Featflow reference")
axes[0].set_xlabel("Mesh level")
axes[0].set_ylabel("mean(Cd)")
axes[0].set_title("Mean drag coefficient vs mesh level")
axes[0].legend()

axes[1].plot(of100["level"], of100["ampCl"], "o-", label="OpenFOAM")
axes[1].axhline(ref100["ampCl"], color="k", linestyle="--", label="Featflow reference")
axes[1].set_xlabel("Mesh level")
axes[1].set_ylabel("amp(Cl)")
axes[1].set_title("Lift amplitude vs mesh level (shedding onset)")
axes[1].legend()

axes[2].plot(of100["level"], of100["St"], "o-", label="OpenFOAM")
axes[2].axhline(ref100["St"], color="k", linestyle="--", label="Featflow reference")
axes[2].set_xlabel("Mesh level")
axes[2].set_ylabel("Strouhal number")
axes[2].set_title("Strouhal number vs mesh level")
axes[2].legend()

plt.tight_layout()
plt.savefig(FIGURES / "re100_openfoam_convergence.png", dpi=150)
plt.close()

print("Saved: re20_fluent_convergence.png, re100_openfoam_convergence.png")