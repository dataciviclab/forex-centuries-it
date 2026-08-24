"""
interest_rates.py - Tassi reali secolari (Schmelzing)
Dati: schmelzing_real_interest_rates.xlsx da forex-centuries upstream
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA = ROOT / "data" / "raw" / "forex-centuries" / "data" / "sources" / "schmelzing"
CHARTS = ROOT / "charts" / "macro"
CHARTS.mkdir(parents=True, exist_ok=True)


def main():
    filepath = DATA / "schmelzing_real_interest_rates.xlsx"
    if not filepath.exists():
        print(f"ERRORE: File non trovato: {filepath}")
        print("Esegui: git clone https://github.com/unbalancedparentheses/forex-centuries.git data/raw/forex-centuries")
        return
    
    # Carica dati
    df = pd.read_excel(filepath, sheet_name="IV. Country level, 1310-2018", header=None)
    
    co = df.iloc[3:].copy()
    co.columns = range(co.shape[1])
    co = co.rename(columns={0: "Year", 2: "Italy", 3: "UK", 5: "Germany", 
                            6: "France", 7: "USA", 8: "Spain", 9: "Japan"})
    co = co[["Year", "Italy", "UK", "Germany", "France", "USA", "Spain", "Japan"]]
    
    for c in co.columns[1:]:
        co[c] = pd.to_numeric(co[c], errors="coerce")
    co["Year"] = pd.to_numeric(co["Year"], errors="coerce")
    co = co.dropna(subset=["Year"])
    co["Year"] = co["Year"].astype(int)
    
    print("Tasso reale medio per paese:")
    for c in ["Italy", "UK", "Germany", "France", "USA"]:
        v = co[c].dropna()
        if len(v) > 0:
            print(f"  {c:<10} {v.mean():.2f}% ({len(v)} anni)")
    
    # Grafico: Italia vs altri
    fig, ax = plt.subplots(figsize=(14, 7))
    colors = {"Italy": "#DAA520", "UK": "#2166AC", "Germany": "#55A868", 
              "France": "#D65F5F", "USA": "#8172B3"}
    
    for c in ["Italy", "UK", "Germany", "France", "USA"]:
        data = co[["Year", c]].dropna()
        if len(data) > 10:
            data["rmean"] = data[c].rolling(50, center=True).mean()
            ax.plot(data["Year"], data["rmean"], label=c, color=colors[c], linewidth=2)
    
    ax.set_xlabel("Anno")
    ax.set_ylabel("Tasso reale (%)")
    ax.set_title("Tassi Reali Secolari: Italia vs Altri Paesi (Schmelzing)", 
                 fontsize=14, fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.axhline(0, color="black", linewidth=0.5)
    
    plt.tight_layout()
    plt.savefig(CHARTS / "interest_rates_countries.png", dpi=150)
    plt.close()
    print("\nSalvato: charts/macro/interest_rates_countries.png")


if __name__ == "__main__":
    main()
