"""
grain_prices.py - Prezzi del grano nelle città italiane medievali
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
CHARTS = ROOT / "charts" / "italy"
CHARTS.mkdir(parents=True, exist_ok=True)


def main():
    # Città italiane
    italian_cities = ["Ancona", "Brescia", "Florence", "Milan", "Naples", "Pisa", "Siena"]
    
    # Carica dati grano
    grains = {}
    for city in italian_cities:
        filepath = DATA / f"{city}_Wheat.tab"
        if filepath.exists():
            df = pd.read_csv(filepath, sep="\t")
            df["Price"] = pd.to_numeric(df["Standardized Value"], errors="coerce")
            grains[city] = df.dropna(subset=["Price"])
    
    print("Prezzo medio grano (g argento/litro):")
    for city, df in sorted(grains.items(), key=lambda x: x[1]["Price"].mean()):
        print(f"  {city:<12} {df['Price'].mean():.3f}")
    
    # Grafico confronto città
    fig, ax = plt.subplots(figsize=(14, 7))
    colors = {"Pisa": "#2166AC", "Siena": "#D65F5F", "Milan": "#55A868", 
              "Naples": "#DD8452", "Ancona": "#8172B3", "Brescia": "#C44E52"}
    
    for city, df in grains.items():
        if len(df) > 5:
            df_sorted = df.sort_values("Year")
            df_sorted["rmean"] = df_sorted["Price"].rolling(10, center=True).mean()
            ax.plot(df_sorted["Year"], df_sorted["rmean"], label=city, 
                    color=colors.get(city, "#4C72B0"), linewidth=2)
    
    ax.set_xlabel("Anno")
    ax.set_ylabel("Prezzo grano (g argento/litro)")
    ax.set_title("Prezzo del Grano nelle Città Italiane (media mobile 10 anni)", 
                 fontsize=14, fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(CHARTS / "grain_prices_cities.png", dpi=150)
    plt.close()
    print("\nSalvato: charts/italy/grain_prices_cities.png")


if __name__ == "__main__":
    main()
