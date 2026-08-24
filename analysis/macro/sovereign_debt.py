"""
sovereign_debt.py - Debito sovrano italiano
Dati: imf_hpdd_debt_gdp.csv da forex-centuries upstream
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA = ROOT / "data" / "raw" / "forex-centuries" / "data" / "sources" / "imf_hpdd"
CHARTS = ROOT / "charts" / "macro"
CHARTS.mkdir(parents=True, exist_ok=True)


def main():
    filepath = DATA / "imf_hpdd_debt_gdp.csv"
    if not filepath.exists():
        print(f"ERRORE: File non trovato: {filepath}")
        print("Esegui: git clone https://github.com/unbalancedparentheses/forex-centuries.git data/raw/forex-centuries")
        return
    
    # Carica dati
    imf = pd.read_csv(filepath)
    imf = imf[imf["country"].apply(lambda x: isinstance(x, str) and len(x) == 2)]
    
    country_map = {"IT": "Italy", "US": "USA", "GB": "UK", "FR": "France", 
                   "DE": "Germany", "JP": "Japan", "ES": "Spain"}
    imf["cn"] = imf["country"].map(country_map)
    imf = imf.dropna(subset=["cn"])
    
    debt = imf.pivot_table(index="year", columns="cn", values="value")
    
    # Statistiche
    italy_debt = debt["Italy"].dropna()
    print(f"Italia: {len(italy_debt)} anni, media={italy_debt.mean():.1f}%, max={italy_debt.max():.1f}%")
    print(f"Sopra 60%: {(italy_debt>60).sum()} anni ({(italy_debt>60).sum()/len(italy_debt)*100:.0f}%)")
    print(f"Sopra 100%: {(italy_debt>100).sum()} anni ({(italy_debt>100).sum()/len(italy_debt)*100:.0f}%)")
    
    # Grafico
    fig, ax = plt.subplots(figsize=(14, 7))
    colors = {"Italy": "#D65F5F", "USA": "#2166AC", "UK": "#55A868", "France": "#8172B3",
              "Germany": "#DD8452", "Japan": "#C44E52", "Spain": "#8C8C8C"}
    
    for c in debt.columns:
        data = debt[c].dropna()
        if len(data) > 0:
            ax.plot(data.index, data, label=c, color=colors.get(c, "#4C72B0"), linewidth=2)
    
    ax.axhline(60, color="gray", linestyle="--", alpha=0.5, label="Maastricht (60%)")
    ax.set_xlabel("Anno")
    ax.set_ylabel("Debito/PIL (%)")
    ax.set_title("Debito Pubblico: Italia vs Altri Paesi (1800-2015)", 
                 fontsize=14, fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(CHARTS / "sovereign_debt_countries.png", dpi=150)
    plt.close()
    print("\nSalvato: charts/macro/sovereign_debt_countries.png")


if __name__ == "__main__":
    main()
