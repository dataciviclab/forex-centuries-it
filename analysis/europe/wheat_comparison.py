"""
wheat_comparison.py - Confronto prezzi grano Italia vs Nord Europa
Dati: Allen-Unger dataset da forex-centuries upstream
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA = ROOT / "data" / "raw" / "forex-centuries" / "data" / "sources" / "allenunger"
CHARTS = ROOT / "charts" / "europe"
CHARTS.mkdir(parents=True, exist_ok=True)


def main():
    # Carica dati grano
    cities = {
        "Pisa": "Pisa_Wheat.tab",
        "Amsterdam": "Amsterdam_Wheat.tab",
        "Paris": "Paris_Wheat.tab",
        "Edinburgh": "Edinburgh_Wheat.tab",
    }
    
    grains = {}
    for city, fname in cities.items():
        filepath = DATA / fname
        if filepath.exists():
            df = pd.read_csv(filepath, sep="\t")
            df["Price"] = pd.to_numeric(df["Standardized Value"], errors="coerce")
            grains[city] = df.dropna(subset=["Price"])
    
    print("Prezzo medio grano (g argento/litro):")
    for city, df in sorted(grains.items(), key=lambda x: x[1]["Price"].mean()):
        print(f"  {city:<12} {df['Price'].mean():.3f}")
    
    # Grafico
    fig, ax = plt.subplots(figsize=(14, 7))
    colors = {"Pisa": "#DAA520", "Amsterdam": "#2166AC", "Paris": "#55A868", "Edinburgh": "#8172B3"}
    
    for city, df in grains.items():
        df_sorted = df.sort_values("Year")
        df_sorted["rmean"] = df_sorted["Price"].rolling(10, center=True).mean()
        ax.plot(df_sorted["Year"], df_sorted["rmean"], label=city, 
                color=colors.get(city, "#4C72B0"), linewidth=2)
    
    ax.set_xlabel("Anno")
    ax.set_ylabel("Prezzo grano (g argento/litro)")
    ax.set_title("Prezzo del Grano: Italia vs Nord Europa (media mobile 10 anni)", 
                 fontsize=14, fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(CHARTS / "wheat_italy_vs_north.png", dpi=150)
    plt.close()
    print("\nSalvato: charts/europe/wheat_italy_vs_north.png")


if __name__ == "__main__":
    main()
