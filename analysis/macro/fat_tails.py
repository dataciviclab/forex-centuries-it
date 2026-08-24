"""
fat_tails.py - Code grasse e paradosso del peg
Dati: daily_volatility_stats.csv da forex-centuries upstream
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
    filepath = DATA / "daily_volatility_stats.csv"
    if not filepath.exists():
        print(f"ERRORE: File non trovato: {filepath}")
        return
    
    vol = pd.read_csv(filepath)
    
    print("=== Code Grasse e Paradosso del Peg ===\n")
    print("Top 5 curtosi:")
    top5 = vol.nlargest(5, "excess_kurtosis")[["currency", "annualized_volatility", "excess_kurtosis"]]
    top5["annualized_volatility"] = (top5["annualized_volatility"] * 100).round(1)
    top5["excess_kurtosis"] = top5["excess_kurtosis"].round(0).astype(int)
    print(top5.to_string(index=False))
    
    print("\nParadosso del peg (vol bassa, curtosi alta):")
    peg_currencies = vol[vol["currency"].isin(["HKD", "CNY", "SGD", "THB"])]
    for _, row in peg_currencies.iterrows():
        print(f"  {row['currency']}: vol={row['annualized_volatility']*100:.1f}%, curtosi={row['excess_kurtosis']:.0f}")
    
    # Grafico 1: Curtosi vs Volatilità
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Scatter plot
    ax1.scatter(vol["annualized_volatility"] * 100, vol["excess_kurtosis"], 
                s=80, alpha=0.7, color="#4C72B0")
    
    # Evidenzia peg currencies
    for _, row in peg_currencies.iterrows():
        ax1.annotate(row["currency"], 
                    (row["annualized_volatility"] * 100, row["excess_kurtosis"]),
                    textcoords="offset points", xytext=(10, 5),
                    fontsize=10, fontweight="bold", color="#D65F5F")
    
    ax1.set_xlabel("Volatilità annua (%)")
    ax1.set_ylabel("Curtosi in eccesso")
    ax1.set_title("Paradosso del Peg:\nVol bassa ≠ Rischio basso", fontsize=12, fontweight="bold")
    ax1.set_yscale("log")
    ax1.grid(True, alpha=0.3)
    
    # Bar chart top 10 curtosi
    top10 = vol.nlargest(10, "excess_kurtosis")
    colors = ["#D65F5F" if c in ["HKD", "CNY", "SGD", "THB"] else "#4C72B0" 
              for c in top10["currency"]]
    ax2.barh(top10["currency"], top10["excess_kurtosis"], color=colors)
    ax2.set_xlabel("Curtosi in eccesso")
    ax2.set_title("Top 10: Code più grasse", fontsize=12, fontweight="bold")
    ax2.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig(CHARTS / "fat_tails_peg_paradox.png", dpi=150)
    plt.close()
    print("\nSalvato: charts/macro/fat_tails_peg_paradox.png")


if __name__ == "__main__":
    main()
