"""
run_all.py - Esegue tutte le analisi
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT.parent / "data" / "raw" / "forex-centuries" / "data"

SCRIPTS = [
    "italy/fx_history.py",
    "italy/grain_prices.py",
    "italy/famines.py",
    "europe/wheat_comparison.py",
    "europe/correlations.py",
    "macro/interest_rates.py",
    "macro/sovereign_debt.py",
    "macro/gold_hedge.py",
    "macro/fat_tails.py",
    "macro/currency_regimes.py",
]

REQUIRED_FILES = [
    "derived/normalized/yearly_unified_panel.csv",
    "sources/schmelzing/schmelzing_real_interest_rates.xlsx",
    "sources/imf_hpdd/imf_hpdd_debt_gdp.csv",
    "sources/allenunger/Pisa_Wheat.tab",
    "derived/analysis/yearly_gold_inflation.csv",
]


def preflight_check():
    """Verifica che i dati upstream esistano"""
    missing = []
    for f in REQUIRED_FILES:
        if not (DATA / f).exists():
            missing.append(f)
    
    if missing:
        print("ERRORE: File upstream mancanti:")
        for f in missing:
            print(f"  - {f}")
        print("\nPer risolvere:")
        print("  cd", ROOT.parent)
        print("  git clone https://github.com/unbalancedparentheses/forex-centuries.git data/raw/forex-centuries")
        return False
    return True


def main():
    print("=== Esecuzione analisi forex-centuries-it ===\n")
    
    if not preflight_check():
        sys.exit(1)
    
    print("Preflight check: OK\n")
    
    for script in SCRIPTS:
        path = ROOT / script
        print(f"--- {script} ---")
        try:
            result = subprocess.run(
                [sys.executable, str(path)],
                capture_output=True,
                text=True,
                timeout=60
            )
            print(result.stdout)
            if result.returncode != 0 and result.stderr:
                print(f"ERRORE: {result.stderr[:200]}")
        except subprocess.TimeoutExpired:
            print(f"ERRORE: Timeout dopo 60 secondi")
        except Exception as e:
            print(f"ERRORE: {e}")
        print()
    
    print("=== Tutte le analisi completate ===")


if __name__ == "__main__":
    main()
