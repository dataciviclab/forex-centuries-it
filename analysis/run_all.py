"""
run_all.py - Esegue tutte le analisi
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SCRIPTS = [
    "italy/fx_history.py",
    "italy/grain_prices.py",
    "italy/famines.py",
    "europe/wheat_comparison.py",
    "macro/interest_rates.py",
    "macro/sovereign_debt.py",
    "macro/gold_hedge.py",
]


def main():
    print("=== Esecuzione analisi forex-centuries-it ===\n")
    
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
            if result.stderr:
                print(f"STDERR: {result.stderr[:200]}")
        except Exception as e:
            print(f"Errore: {e}")
        print()
    
    print("=== Tutte le analisi completate ===")


if __name__ == "__main__":
    main()
