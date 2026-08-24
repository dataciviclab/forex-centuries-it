"""
fx_history.py - Storia del tasso di cambio Italia vs USD
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
CHARTS = ROOT / "charts" / "italy"
CHARTS.mkdir(parents=True, exist_ok=True)


def main():
    # Carica dati
    filepath = DATA / "yearly_unified_panel.csv"
    if not filepath.exists():
        print(f"ERRORE: File non trovato: {filepath}")
        print("Esegui: git clone https://github.com/unbalancedparentheses/forex-centuries.git data/raw/forex-centuries")
        return
    
    panel = pd.read_csv(filepath)
    panel["year"] = panel["year"].astype(int)
    italy = panel[panel["country"] == "Italy"].sort_values("year")
    
    print(f"Italia: {len(italy)} anni, {italy['year'].min()}-{italy['year'].max()}")
    
    # Grafico principale
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={"height_ratios": [3, 1]})
    
    ax1.plot(italy["year"], italy["rate_per_usd"], color="#2166AC", linewidth=1.5)
    ax1.set_yscale("log")
    ax1.set_ylabel("Lira/EUR per 1 USD (log scale)")
    ax1.set_title("Italia: Tasso di cambio vs USD (1861-2025)", fontsize=14, fontweight="bold")
    ax1.grid(True, alpha=0.3)
    
    # Eventi storici
    events = {
        1861: "Unita d'Italia", 1914: "WWI", 1922: "Fascismo",
        1940: "WWII", 1946: "Repubblica", 1992: "Crisi ERM", 2002: "Euro"
    }
    for year, label in events.items():
        if italy["year"].min() <= year <= italy["year"].max():
            ax1.axvline(year, color="gray", linestyle=":", alpha=0.5)
            ax1.text(year, ax1.get_ylim()[1] * 0.6, f" {label}", fontsize=7, rotation=90, va="top", color="gray")
    
    # Variazione %
    italy["pct_change"] = italy["rate_per_usd"].pct_change() * 100
    colors = ["#D65F5F" if x < 0 else "#55A868" for x in italy["pct_change"].fillna(0)]
    ax2.bar(italy["year"], italy["pct_change"], color=colors, width=1, alpha=0.7)
    ax2.set_ylabel("Variazione % annua")
    ax2.set_xlabel("Anno")
    ax2.axhline(0, color="black", linewidth=0.5)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(CHARTS / "italy_fx_vs_usd.png", dpi=150)
    plt.close()
    print("Salvato: charts/italy/italy_fx_vs_usd.png")
    
    # Riepilogo
    start = italy.iloc[0]["rate_per_usd"]
    end = italy.iloc[-1]["rate_per_usd"]
    print(f"\n1861: 1 USD = {start:.6f} Lire")
    print(f"2025: 1 USD = {end:.4f} EUR")
    print(f"Deprecazione: {((end-start)/start*100):+.0f}%")


if __name__ == "__main__":
    main()
