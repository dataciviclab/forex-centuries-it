"""
currency_regimes.py - Regimi di cambio nel tempo
Dati: yearly_regime_classification.csv da forex-centuries upstream
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA = ROOT / "data" / "raw" / "forex-centuries" / "data" / "derived" / "analysis"
CHARTS = ROOT / "charts" / "macro"
CHARTS.mkdir(parents=True, exist_ok=True)


def main():
    filepath = DATA / "yearly_regime_classification.csv"
    if not filepath.exists():
        print(f"ERRORE: File non trovato: {filepath}")
        return
    
    regime = pd.read_csv(filepath)
    
    print("=== Regimi di Cambio ===\n")
    print("Regimi disponibili:")
    print(regime["regime_label"].value_counts().to_string())
    
    # Grafico: distribuzione regimi nel tempo
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Conteggio regimi per decennio
    regime["decade"] = (regime["year"] // 10) * 10
    regime_counts = regime.groupby(["decade", "regime_label"]).size().unstack(fill_value=0)
    
    # Stack plot
    regime_counts.plot(kind="bar", stacked=True, ax=ax1, 
                       colormap="Set2", edgecolor="white", linewidth=0.5)
    ax1.set_xlabel("Decennio")
    ax1.set_ylabel("Numero di paesi")
    ax1.set_title("Distribuzione Regimi di Cambio nel Tempo", fontsize=12, fontweight="bold")
    ax1.legend(title="Regime", bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)
    ax1.set_xticklabels([str(int(x)) for x in regime_counts.index], rotation=45)
    
    # Italia specifica
    italy_regime = regime[regime["country"] == "Italy"].sort_values("year")
    if len(italy_regime) > 0:
        regime_colors = {"peg": "#2166AC", "free_float": "#55A868", 
                        "managed_float": "#DD8452", "freely_falling": "#D65F5F"}
        
        for _, row in italy_regime.iterrows():
            color = regime_colors.get(row["regime_label"], "#8C8C8C")
            ax2.barh(0, 1, left=row["year"], height=0.8, color=color, edgecolor="none")
        
        ax2.set_yticks([])
        ax2.set_xlabel("Anno")
        ax2.set_title("Regime di Cambio Italia", fontsize=12, fontweight="bold")
        
        # Legend
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=c, label=l) for l, c in regime_colors.items()]
        ax2.legend(handles=legend_elements, loc="upper right", fontsize=8)
    
    plt.tight_layout()
    plt.savefig(CHARTS / "currency_regimes.png", dpi=150)
    plt.close()
    print("\nSalvato: charts/macro/currency_regimes.png")


if __name__ == "__main__":
    main()
