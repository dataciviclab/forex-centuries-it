"""
gold_hedge.py - Oro come hedge: 768 anni di potere d'acquisto
Dati: yearly_gold_inflation.csv da forex-centuries upstream
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA = ROOT / "data" / "raw" / "forex-centuries" / "data" / "derived" / "analysis"
CHARTS = ROOT / "charts" / "gold"
CHARTS.mkdir(parents=True, exist_ok=True)


def main():
    # Carica dati
    gi = pd.read_csv(DATA / "yearly_gold_inflation.csv")
    gi["year"] = gi["year"].astype(int)
    
    # USA
    us = gi[gi["country"] == "United States"].sort_values("year")
    print(f"Oro vs USD: potere d'acquisto retained = {us['cumulative_retained_pct'].iloc[-1]:.1f}%")
    print(f"Da 100% a {us['cumulative_retained_pct'].iloc[-1]:.1f}% in {len(us)} anni")
    
    # Grafico: Oro vs valute
    countries = ["United States", "United Kingdom", "France", "Germany", "Japan", "Italy"]
    colors = ["#DAA520", "#2166AC", "#D65F5F", "#55A868", "#8172B3", "#DD8452"]
    
    fig, ax = plt.subplots(figsize=(14, 8))
    for c, col in zip(countries, colors):
        d = gi[gi["country"] == c].sort_values("year")
        if len(d) > 0:
            ax.plot(d["year"], d["cumulative_retained_pct"], label=c, color=col, linewidth=1.5)
    
    ax.set_yscale("log")
    ax.set_xlabel("Anno")
    ax.set_ylabel("% potere d'acquisto retained (log)")
    ax.set_title("Oro come Hedge: Potere d'Acquisto vs Valute (1257-2025)", 
                 fontsize=14, fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3, which="both")
    ax.axhline(100, color="black", linestyle="--", alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(CHARTS / "gold_hedge_comparison.png", dpi=150)
    plt.close()
    print("\nSalvato: charts/gold/gold_hedge_comparison.png")


if __name__ == "__main__":
    main()
