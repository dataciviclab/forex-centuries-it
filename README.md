# forex-centuries-it

Analisi dei dati storici economici e finanziari dell'Italia, basata sul dataset [forex-centuries](https://github.com/unbalancedparentheses/forex-centuries).

## Descrizione

Questo repo contiene analisi dei dati storici che coprono:

- **Tassi di cambio** Italia vs USD (1861-2025)
- **Prezzi del grano** nelle città italiane medievali (1286-1860)
- **Carestie** identificate dai prezzi del grano
- **Tassi d'interesse reali** secolari (1314-2018)
- **Debito sovrano** italiano vs altri paesi (1800-2015)
- **Oro** come hedge contro l'inflazione (1257-2025)

## Struttura

```
forex-centuries-it/
├── README.md
├── LESSONS_FROM_HISTORY.md      # 7 lezioni dalla storia
├── data/raw/                   # Dati upstream (gitignored)
├── analysis/
│   ├── italy/
│   │   ├── fx_history.py
│   │   ├── grain_prices.py
│   │   └── famines.py
│   ├── europe/
│   │   └── wheat_comparison.py
│   └── macro/
│       ├── interest_rates.py
│       ├── sovereign_debt.py
│       └── gold_hedge.py
│   └── run_all.py
├── notebooks/
│   └── summary.ipynb
└── charts/
    ├── italy/
    ├── europe/
    ├── gold/
    └── macro/
```

## Setup

```bash
# 1. Clona questo repo
git clone https://github.com/dataciviclab/forex-centuries-it.git
cd forex-centuries-it

# 2. Clona i dati upstream
git clone https://github.com/unbalancedparentheses/forex-centuries.git data/raw/forex-centuries

# 3. Installa dipendenze
pip install pandas numpy matplotlib openpyxl jupyter
```

## Uso

```bash
# Esegui tutte le analisi
python analysis/run_all.py

# O singole analisi
python analysis/italy/fx_history.py
python analysis/macro/interest_rates.py

# Apri il notebook
jupyter notebook notebooks/summary.ipynb
```

## Output

| Analisi | Output |
|---------|--------|
| fx_history | charts/italy/italy_fx_vs_usd.png |
| grain_prices | charts/italy/grain_prices_cities.png |
| famines | charts/italy/famines_pisa.png |
| wheat_comparison | charts/europe/wheat_italy_vs_north.png |
| interest_rates | charts/macro/interest_rates_countries.png |
| sovereign_debt | charts/macro/sovereign_debt_countries.png |
| gold_hedge | charts/gold/gold_hedge_comparison.png |

## Fonti

- [forex-centuries](https://github.com/unbalancedparentheses/forex-centuries) - Dataset originale
- [Allen-Unger Global Commodity Prices](https://datasets.iisg.amsterdam/) - Prezzi storici
- [Schmelzing (BoE)](https://www.bankofengland.co.uk/) - Tassi reali secolari
- [IMF HPDD](https://data.imf.org/) - Debito sovrano

## Licenza

Questo repo è distribuito sotto licenza MIT. I dati upstream hanno le loro licenze originali.

## Contatti

DataCivicLab - [github.com/dataciviclab](https://github.com/dataciviclab)
