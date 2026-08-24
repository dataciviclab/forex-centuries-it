"""
famines.py - Analisi carestie nei dati del grano italiano
Dati: Allen-Unger Pisa_Wheat.tab da forex-centuries upstream
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA = ROOT / "data" / "raw" / "forex-centuries" / "data" / "sources" / "allenunger"
CHARTS = ROOT / "charts" / "italy"
CHARTS.mkdir(parents=True, exist_ok=True)


def main():
    filepath = DATA / "Pisa_Wheat.tab"
    if not filepath.exists():
        print(f"ERRORE: File non trovato: {filepath}")
        print("Esegui: git clone https://github.com/unbalancedparentheses/forex-centuries.git data/raw/forex-centuries")
        return
    
    # Carica dati Pisa
    pisa = pd.read_csv(filepath, sep="\t")
    pisa["Year"] = pd.to_numeric(pisa["Year"], errors="coerce")
    pisa["Price"] = pd.to_numeric(pisa["Standardized Value"], errors="coerce")
    pisa = pisa.dropna(subset=["Year", "Price"]).sort_values("Year")
    
    # Z-score
    pisa["zscore"] = (pisa["Price"] - pisa["Price"].rolling(20, center=True).mean()) / \
                     pisa["Price"].rolling(20, center=True).std()
    
    n_critical = (pisa["zscore"] > 1.5).sum()
    print(f"Anni critici (z>1.5): {n_critical} su {len(pisa)}")
    
    # Top 5 anni peggiori
    top5 = pisa.nlargest(5, "zscore")
    print("\nTop 5 anni peggiori:")
    for _, r in top5.iterrows():
        print(f"  {int(r['Year'])}: {r['Price']:.3f} g arg/litro (z={r['zscore']:.1f})")
    
    # Grafico
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(pisa["Year"], pisa["Price"], color="#2166AC", linewidth=0.8, alpha=0.6, label="Annuale")
    pisa["rmean"] = pisa["Price"].rolling(20, center=True).mean()
    ax.plot(pisa["Year"], pisa["rmean"], color="#D65F5F", linewidth=2, label="Media mobile 20 anni")
    
    # Evidenzia anni critici
    critical = pisa[pisa["zscore"] > 1.5]
    ax.scatter(critical["Year"], critical["Price"], color="red", s=30, zorder=5, label="Anni critici")
    
    ax.set_xlabel("Anno")
    ax.set_ylabel("Prezzo grano (g argento/litro)")
    ax.set_title("Prezzo del Grano a Pisa: Carestie Identificate", fontsize=14, fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(CHARTS / "famines_pisa.png", dpi=150)
    plt.close()
    print("\nSalvato: charts/italy/famines_pisa.png")


if __name__ == "__main__":
    main()
