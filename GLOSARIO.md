# Glossario: Dati, Eventi e Nomi

Guida per capire i dati, gli eventi storici e i nomi usati nel progetto forex-centuries-it.

---

## Tassi di Cambio

### Lire per USD
Il numero di Lire necessarie per comprare 1 Dollaro USA. Se sale, la Lira si svaluta.

| Anno | Tasso | Contesto storico |
|------|-------|------------------|
| 1861 | 0.0027 | Unità d'Italia, Lira ancora forte |
| 1914 | ~5 | Prima guerra mondiale, primo grande debito |
| 1946 | ~100 | Post-WWII, svalutazione massiccia |
| 1992 | ~1.200 | Crisi ERM, Lira crolla del 30% |
| 2002 | 0.95 | Euro (1 EUR = 1.936 Lire) |

### EUR/USD
Dopo il 2002, il tasso è Euro per 1 Dollaro. Se sale, l'EUR si svaluta rispetto al USD.

### Rate per USD
Colonna del dataset `yearly_unified_panel.csv`. Rappresenta quante unità locali servono per 1 USD.

---

## Grano e Carestie

### Prezzo in grammi d'argento per litro
Unità di misura standardizzata del dataset Allen-Unger. Permette di confrontare prezzi tra città e secoli diversi, normalizzando per il valore dell'argento.

### Z-score
Misura quante deviazioni standard un valore è distante dalla media.
- **z > 1.5**: prezzo anomalo (anno critico)
- **z > 2.0**: carestia grave
- **z < -1.5**: anno particolarmente favorevole

Calcolo: `z = (prezzo - media_mobile_20) / std_mobile_20`

### Città italiane nel dataset

| Città | Record | Periodo | Caratteristiche |
|-------|--------|---------|-----------------|
| **Pisa** | 658 | 1548-1818 | Porto toscano, accesso grano marittimo |
| **Milano** | 3.176 | 1601-1860 | Città più grande, mercato interno |
| **Firenze** | 1.197 | 1286-1620 | Centro finanziario, banche medicee |
| **Napoli** | 224 | 1550-1803 | Regno meridionale |
| **Siena** | 220 | 1546-1765 | Città toscana, mercato locale |
| **Ancona** | 117 | 1700-1825 | Porto adriatico |
| **Brescia** | 112 | 1685-1799 | Lombardia |

### Perché il grano italiano costava meno
L'Italia aveva accesso al grano siciliano e pugliese via mare, riducendo i costi di trasporto. Il Nord Europa dipendeva dalla coltivazione locale, esposto a carestie più frequenti.

---

## Tassi d'Interesse Reali

### Tasso reale
Il tasso nominale meno l'inflazione. Se il tasso nominale è 5% e l'inflazione è 3%, il tasso reale è 2%.

Formula: `tasso_reale ≈ tasso_nominale - inflazione`

### Suprasecular decline
Il tasso reale globale è sceso da ~10% (1300) a ~1-2% (oggi) in 700 anni. Trend costante attraverso guerre, pandemie, rivoluzioni.

Tasso di declino: **-1.59% per secolo**.

### Paul Schmelzing
Ricercatore di Harvard, ha ricostruito i tassi reali globali dall'Archivio di Stato di Firenze (1311) fino ai giorni nostri. Il paper è Bank of England Staff Working Paper 845 (2020).

### Perché i tassi calano
- Accumulazione di capitale nel tempo
- Riduzione del rischio istituzionale
- Invecchiamento della popolazione
- Maggiore integrazione dei mercati finanziari

---

## Debito Sovrano

### Debito/PIL
Rapporto tra il debito pubblico e il prodotto interno lordo. Se il PIL è 100 e il debito è 60, il ratio è 60%.

### Trattato di Maastricht (1992)
Soglia del 60% per il debito/PIL nell'Eurozona. L'Italia non l'ha mai rispettata dal 1980.

### Eventi chiave del debito italiano

| Anno | Debito/PIL | Evento |
|------|-----------|--------|
| 1861 | 39% | Unità d'Italia |
| 1919 | 160% | Post-WWI |
| 1943 | 184% | WWII |
| 1947 | 24% | Post-WWII (svalutazione erode il debito) |
| 1981 | 60% | Corso forza |
| 1992 | 105% | Crisi ERM |
| 2011 | 116% | Crisi euro |

### Meccanismo di riduzione storico
L'unico modo storico per ridurre il debito significativamente è stato attraverso **inflazione e svalutazione monetaria**, non austerità.

---

## Oro come Hedge

### Potere d'acquisto retained
Percentuale del potere d'acquisto originale che viene preservata nel tempo.
- **GBP**: ~100% retained per 768 anni
- **USD**: ~0.6% retained per 236 anni

### Hedge
Copertura contro l'inflazione. L'oro è un hedge **secolare** (funziona su 50+ anni) ma non **decennale** (volatilità alta a breve).

### Perché l'oro preserva il valore
L'offerta è limitata (mining), mentre le valute sono illimitate (stampa monetaria). Questo crea un vantaggio strutturale a lungo termine.

---

## Code Grasse (Fat Tails)

### Curtosi in eccesso (Excess Kurtosis)
Misura la "pesantezza" delle code di una distribuzione rispetto alla Gaussiana.
- **Curtosi = 0**: distribuzione normale
- **Curtosi > 0**: code più pesanti (più eventi estremi)
- **Curtosi > 100**: code enormi

### Peg Paradox
Le valute con peg (fissate a un'altra valuta) hanno:
- **Volatilità bassa** quotidianamente
- **Curtosi altissima** (quando il peg cede, il crollo è catastrofico)

Esempi:
- **HKD**: vol 3.2%, curtosi 4109
- **CNY**: vol 8.2%, curtosi 3846
- **SGD**: vol 5.3%, curtosi 11

### Implicazione pratica
I modelli finanziari standard (VaR, Black-Scholes) usano distribuzioni normali e **sottostimano sistematicamente** il rischio estremo.

---

## Regimi di Cambio

| Regime | Significato | Esempio |
|--------|-------------|---------|
| **Peg** | Valuta fissa rispetto a un'altra | HKD (fissata all'USD) |
| **Crawling peg** | Aggiustamenti periodici | Argentina 1990s |
| **Managed float** | Fluttuazione gestita dalla BC | CNY oggi |
| **Free float** | Fluttuazione libera | EUR, GBP, JPY |
| **Freely falling** | Crollo in corso | Venezuela oggi |
| **Dual market** | Mercato ufficiale + parallelo | Cuba, Iran |

### Evoluzione storica
- **1870-1914**: Gold standard (peg fisso all'oro)
- **1944-1971**: Bretton Woods (peg al USD)
- **1971-oggi**: Floating (alcuni peg rimangono)

---

## Correlazioni

### Correlazione di Pearson (r)
Misura quanto due variabili si muovono insieme.
- **r = 1**: muovono sempre insieme (perfetta positiva)
- **r = 0**: nessuna relazione
- **r = -1**: muovono in opposto (perfetta negativa)

### Correlazioni nel dataset

| Coppia | r | Interpretazione |
|--------|---|-----------------|
| Italy-Spain | 0.97 | Quasi identiche (economie simili) |
| Italy-Belgium | 0.78 | Forte connessione commerciale |
| UK-Switzerland | -0.93 | Opposte (safe haven vs rischio) |
| Netherlands-Belgium | 0.57 | Mercato integrato |
| Italy-France | — | Non correlata (dati insufficienti) |

### Integrazione commerciale
Alta correlazione tra tassi di cambio = mercati connessi. Il Nord Europa (Amsterdam-Antwerp-Paris) era più integrato dell'Italia nel Medioevo.

---

## Nomi Chiave

| Nome | Ruolo | Perché è importante |
|------|-------|---------------------|
| **Schmelzing** | Ricercatore Harvard | Ha ricostruito 700 anni di tassi reali |
| **Allen-Unger** | Storici economici | Dataset commodity 1260-1914 |
| **Maddison** | Economista | Stima PIL mondiale dal 1 d.C. |
| **Reinhart-Rogoff** | Economiste | Studio debito e crisi finanziarie |
| **Florino d'oro** | Moneta fiorentina (1252) | Prima moneta stabile europea |
| **Banco d'Inghilterra** | Banca centrale (1694) | Ha ridotto i tassi britannici |

---

## Fonti dei Dati

| Fonte | Contenuto | Periodo |
|-------|-----------|---------|
| **forex-centuries** | Dataset aggregato | 1-2026 |
| **Allen-Unger** | Commodity prices | 1260-1914 |
| **Schmelzing (BoE)** | Tassi reali | 1311-2018 |
| **IMF HPDD** | Debito sovrano | 1800-2015 |
| **MeasuringWorth** | Prezzi oro, tassi | 1257-2025 |
| **Clio Infra** | Tassi cambio, inflazione | 1500-2013 |

---

*Glossario generato il 24 agosto 2026 dal progetto forex-centuries-it.*
