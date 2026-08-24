# forex-centuries-it

Analisi dei dati storici economici e finanziari dell'Italia, basata sul dataset [forex-centuries](https://github.com/unbalancedparentheses/forex-centuries).

## Descrizione

Questo repo contiene analisi dei dati storici che coprono:

- **Tassi di cambio** Italia vs USD (1861-2025)
- **Prezzi del grano** nelle città italiane medievali (1286-1860)
- **Carestie** identificate dai prezzi del grano
- **Confronto Europa** prezzi grano Italia vs Nord
- **Correlazioni** cross-paesi (integrazione commerciale)
- **Tassi d'interesse reali** secolari (1314-2018)
- **Debito sovrano** italiano vs altri paesi (1800-2015)
- **Oro** come hedge contro l'inflazione (1257-2025)
- **Code grasse** e paradosso del peg
- **Regimi di cambio** nel tempo

## Struttura

```
forex-centuries-it/
├── README.md
├── LESSONS_FROM_HISTORY.md      # 7 lezioni dalla storia
├── GLOSARIO.md                 # Definizioni, eventi, nomi
├── requirements.txt            # Dipendenze Python
├── app.py                      # Dashboard Streamlit
├── data/raw/                   # Dati upstream (gitignored)
├── analysis/
│   ├── italy/
│   │   ├── fx_history.py       # Tassi cambio Italia
│   │   ├── grain_prices.py     # Prezzi grano città italiane
│   │   └── famines.py          # Carestie (z-score)
│   ├── europe/
│   │   ├── wheat_comparison.py # Italia vs Nord Europa
│   │   └── correlations.py     # Correlazioni cross-paesi
│   ├── macro/
│   │   ├── interest_rates.py   # Tassi reali secolari
│   │   ├── sovereign_debt.py   # Debito sovrano
│   │   ├── gold_hedge.py       # Oro come hedge
│   │   ├── fat_tails.py        # Code grasse, peg paradox
│   │   └── currency_regimes.py # Regimi di cambio
│   └── run_all.py             # Esegue tutte le analisi
├── notebooks/
│   └── summary.ipynb           # Notebook Jupyter
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
pip install -r requirements.txt
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

# Avvia la dashboard
streamlit run app.py
```

## Dashboard

La dashboard Streamlit offre 10 pagine interattive:

1. Tassi di cambio
2. Grano medievale
3. Carestie
4. Confronto Europa
5. Correlazioni
6. Tassi reali secolari
7. Debito sovrano
8. Oro come hedge
9. Code grasse
10. Regimi di cambio

## Output

| Analisi | Output |
|---------|--------|
| fx_history | charts/italy/italy_fx_vs_usd.png |
| grain_prices | charts/italy/grain_prices_cities.png |
| famines | charts/italy/famines_pisa.png |
| wheat_comparison | charts/europe/wheat_italy_vs_north.png |
| correlations | charts/europe/cross_correlations.png |
| interest_rates | charts/macro/interest_rates_countries.png |
| sovereign_debt | charts/macro/sovereign_debt_countries.png |
| gold_hedge | charts/gold/gold_hedge_comparison.png |
| fat_tails | charts/macro/fat_tails_peg_paradox.png |
| currency_regimes | charts/macro/currency_regimes.png |

## Documentazione

- **[LESSONS_FROM_HISTORY.md](LESSONS_FROM_HISTORY.md)** - 7 lezioni dalla storia economica
- **[GLOSARIO.md](GLOSARIO.md)** - Definizioni, eventi storici, nomi chiave

## Fonti

- [forex-centuries](https://github.com/unbalancedparentheses/forex-centuries) - Dataset originale
- [Allen-Unger Global Commodity Prices](https://datasets.iisg.amsterdam/) - Prezzi storici
- [Schmelzing (BoE)](https://www.bankofengland.co.uk/) - Tassi reali secolari
- [IMF HPDD](https://data.imf.org/) - Debito sovrano

## Licenza

Questo repo è distribuito sotto licenza MIT. I dati upstream hanno le loro licenze originali.

## Contatti

DataCivicLab - [github.com/dataciviclab](https://github.com/dataciviclab)
