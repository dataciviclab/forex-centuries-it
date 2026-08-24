"""
correlations.py - Correlazioni cross-paesi (integrazione commerciale)
Dati: yearly_unified_panel.csv da forex-centuries upstream
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA = ROOT / "data" / "raw" / "forex-centuries" / "data" / "derived" / "normalized"
CHARTS = ROOT / "charts" / "europe"
CHARTS.mkdir(parents=True, exist_ok=True)


def main():
    filepath = DATA / "yearly_unified_panel.csv"
    if not filepath.exists():
        print(f"ERRORE: File non trovato: {filepath}")
        return
    
    panel = pd.read_csv(filepath)
    panel["year"] = panel["year"].astype(int)
    
    # Pivot: anno x paese
    pivot = panel.pivot_table(index="year", columns="country", values="rate_per_usd")
    
    # Seleziona paesi europei principali
    europe = ["Italy", "France", "Germany", "United Kingdom", "Spain", 
              "Netherlands", "Belgium", "Switzerland"]
    available = [c for c in europe if c in pivot.columns]
    
    corr = pivot[available].corr()
    
    print("=== Correlazioni Cross-Paesi ===\n")
    print("Correlazioni significative (|r| > 0.5):")
    for i, c1 in enumerate(available):
        for c2 in available[i+1:]:
            r = corr.loc[c1, c2]
            if abs(r) > 0.5:
                print(f"  {c1} <-> {c2}: r = {r:.3f}")
    
    # Grafico: heatmap correlazioni
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1, aspect="equal")
    
    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right", fontsize=10)
    ax.set_yticks(range(len(corr.index)))
    ax.set_yticklabels(corr.index, fontsize=10)
    
    for i in range(len(corr.index)):
        for j in range(len(corr.columns)):
            val = corr.values[i, j]
            color = "white" if abs(val) > 0.5 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=10, color=color)
    
    plt.colorbar(im, ax=ax, label="Correlazione Pearson")
    ax.set_title("Correlazioni Tassi di Cambio: Integrazione Commerciale", 
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(CHARTS / "cross_correlations.png", dpi=150)
    plt.close()
    print("\nSalvato: charts/europe/cross_correlations.png")


if __name__ == "__main__":
    main()
