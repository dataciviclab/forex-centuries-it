"""
app.py - Dashboard Streamlit: Italia, 2000 anni di dati economici
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "raw" / "forex-centuries" / "data"

st.set_page_config(page_title="Italia: 2000 anni di dati", layout="wide")


@st.cache_data
def load_fx():
    return pd.read_csv(DATA / "derived" / "normalized" / "yearly_unified_panel.csv")


@st.cache_data
def load_grain(city):
    return pd.read_csv(DATA / "sources" / "allenunger" / f"{city}_Wheat.tab", sep="\t")


@st.cache_data
def load_rates():
    df = pd.read_excel(DATA / "sources" / "schmelzing" / "schmelzing_real_interest_rates.xlsx",
                       sheet_name="IV. Country level, 1310-2018", header=None, skiprows=3)
    df = df.iloc[:, :10]
    df.columns = ["Year", "_", "Italy", "UK", "Holland", "Germany", "France", "USA", "Spain", "Japan"]
    for c in ["Italy", "UK", "Germany", "France", "USA", "Spain", "Japan"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["Year"])
    return df


@st.cache_data
def load_debt():
    imf = pd.read_csv(DATA / "sources" / "imf_hpdd" / "imf_hpdd_debt_gdp.csv")
    imf = imf[imf["country"].apply(lambda x: isinstance(x, str) and len(x) == 2)]
    map_ = {"IT": "Italy", "US": "USA", "GB": "UK", "FR": "France", "DE": "Germany", "JP": "Japan", "ES": "Spain"}
    imf["cn"] = imf["country"].map(map_)
    imf = imf.dropna(subset=["cn"])
    return imf.pivot_table(index="year", columns="cn", values="value")


@st.cache_data
def load_gold():
    return pd.read_csv(DATA / "derived" / "analysis" / "yearly_gold_inflation.csv")


# ─── Sidebar ───
st.sidebar.title("Navigazione")
pagina = st.sidebar.radio("Scegli un'analisi", [
    "Tassi di cambio",
    "Grano medievale",
    "Carestie",
    "Confronto Europa",
    "Correlazioni",
    "Tassi reali secolari",
    "Debito sovrano",
    "Oro come hedge",
    "Code grasse",
    "Regimi di cambio"
])


# ─── Pagine ───
if pagina == "Tassi di cambio":
    st.title("Tassi di cambio Italia vs USD")
    st.write("155 anni di tassi di cambio: dalla Lira all'Euro.")
    
    fx = load_fx()
    italy = fx[fx["country"] == "Italy"].sort_values("year")
    
    # Filtro anni
    year_min, year_max = st.slider("Range anni", 
                                    int(italy["year"].min()), 
                                    int(italy["year"].max()),
                                    (1861, 2025))
    mask = (italy["year"] >= year_min) & (italy["year"] <= year_max)
    filtered = italy[mask]
    
    fig = px.line(filtered, x="year", y="rate_per_usd",
                  title="Tasso di cambio: Lire/EUR per 1 USD",
                  labels={"year": "Anno", "rate_per_usd": "Lire/EUR per 1 USD"})
    fig.update_yaxes(type="log")
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistiche
    col1, col2, col3 = st.columns(3)
    col1.metric("Anni totali", len(filtered))
    col2.metric("Min", f"{filtered['rate_per_usd'].min():.6f}")
    col3.metric("Max", f"{filtered['rate_per_usd'].max():.4f}")


elif pagina == "Grano medievale":
    st.title("Prezzi del grano nelle città italiane")
    
    cities = ["Pisa", "Amsterdam", "Paris", "Edinburgh"]
    selected = st.multiselect("Seleziona città", cities, default=["Pisa", "Amsterdam"])
    
    fig = go.Figure()
    for city in selected:
        try:
            df = load_grain(city)
            df["Price"] = pd.to_numeric(df["Standardized Value"], errors="coerce")
            df = df.dropna(subset=["Price"]).sort_values("Year")
            df["rmean"] = df["Price"].rolling(10, center=True).mean()
            fig.add_trace(go.Scatter(x=df["Year"], y=df["rmean"], name=city, mode="lines"))
        except:
            st.warning(f"Dati non disponibili per {city}")
    
    fig.update_layout(title="Prezzo del grano (g argento/litro)",
                      xaxis_title="Anno", yaxis_title="Prezzo",
                      height=500)
    st.plotly_chart(fig, use_container_width=True)


elif pagina == "Carestie":
    st.title("Carestie nei dati del grano")
    
    pisa = load_grain("Pisa")
    pisa["Price"] = pd.to_numeric(pisa["Standardized Value"], errors="coerce")
    pisa = pisa.dropna(subset=["Price"]).sort_values("Year")
    
    # Z-score
    soglia = st.slider("Soglia z-score", 1.0, 3.0, 1.5, 0.1)
    pisa["zscore"] = (pisa["Price"] - pisa["Price"].rolling(20, center=True).mean()) / \
                     pisa["Price"].rolling(20, center=True).std()
    
    critical = pisa[pisa["zscore"] > soglia]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pisa["Year"], y=pisa["Price"], name="Prezzo", mode="lines"))
    fig.add_trace(go.Scatter(x=critical["Year"], y=critical["Price"], 
                            name=f"Anni critici (z>{soglia})", mode="markers",
                            marker=dict(color="red", size=8)))
    fig.update_layout(title=f"Prezzo grano Pisa - Anni critici: {len(critical)}",
                      xaxis_title="Anno", yaxis_title="Prezzo (g arg/litro)",
                      height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.metric("Anni critici", len(critical))


elif pagina == "Confronto Europa":
    st.title("Confronto prezzi grano: Italia vs Nord Europa")
    
    cities = {"Pisa": "#DAA520", "Amsterdam": "#2166AC", "Paris": "#55A868", "Edinburgh": "#8172B3"}
    
    fig = go.Figure()
    for city, color in cities.items():
        try:
            df = load_grain(city)
            df["Price"] = pd.to_numeric(df["Standardized Value"], errors="coerce")
            df = df.dropna(subset=["Price"]).sort_values("Year")
            df["rmean"] = df["Price"].rolling(10, center=True).mean()
            fig.add_trace(go.Scatter(x=df["Year"], y=df["rmean"], name=city, 
                                    mode="lines", line=dict(color=color)))
        except:
            pass
    
    fig.update_layout(title="Prezzo del grano: Italia vs Nord Europa",
                      xaxis_title="Anno", yaxis_title="Prezzo (g arg/litro)",
                      height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("Il grano italiano costava 30-40% meno di quello del Nord Europa.")


elif pagina == "Tassi reali secolari":
    st.title("Tassi reali secolari (Schmelzing)")
    st.write("700 anni di tassi reali: il suprasecular decline.")
    
    rates = load_rates()
    paesi = st.multiselect("Seleziona paesi", 
                           ["Italy", "UK", "Germany", "France", "USA"],
                           default=["Italy", "UK", "Germany"])
    
    fig = go.Figure()
    colors = {"Italy": "#DAA520", "UK": "#2166AC", "Germany": "#55A868", 
              "France": "#D65F5F", "USA": "#8172B3"}
    
    for p in paesi:
        data = rates[["Year", p]].dropna()
        data["rmean"] = data[p].rolling(50, center=True).mean()
        fig.add_trace(go.Scatter(x=data["Year"], y=data["rmean"], name=p,
                                mode="lines", line=dict(color=colors.get(p, "#4C72B0"))))
    
    fig.update_layout(title="Tassi reali: trend secolare",
                      xaxis_title="Anno", yaxis_title="Tasso reale (%)",
                      height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("Trend: -1.59% per secolo in 700 anni.")


elif pagina == "Debito sovrano":
    st.title("Debito sovrano: Italia vs paesi")
    
    debt = load_debt()
    paesi = st.multiselect("Seleziona paesi", 
                           debt.columns.tolist(),
                           default=["Italy", "USA", "UK", "Germany"])
    
    fig = go.Figure()
    for p in paesi:
        data = debt[p].dropna()
        fig.add_trace(go.Scatter(x=data.index, y=data, name=p, mode="lines"))
    
    fig.add_hline(y=60, line_dash="dash", line_color="gray", 
                  annotation_text="Maastricht (60%)")
    fig.update_layout(title="Debito sovrano vs PIL",
                      xaxis_title="Anno", yaxis_title="Debito/PIL (%)",
                      height=500)
    st.plotly_chart(fig, use_container_width=True)


elif pagina == "Oro come hedge":
    st.title("Oro come hedge: potere d'acquisto")
    
    gold = load_gold()
    paesi = st.multiselect("Seleziona paesi",
                          ["United States", "United Kingdom", "France", "Germany", "Italy"],
                          default=["United States", "United Kingdom", "Italy"])
    
    fig = go.Figure()
    colors = {"United States": "#DAA520", "United Kingdom": "#2166AC", "France": "#D65F5F",
              "Germany": "#55A868", "Italy": "#DD8452"}
    
    for p in paesi:
        d = gold[gold["country"] == p].sort_values("year")
        if len(d) > 0:
            fig.add_trace(go.Scatter(x=d["year"], y=d["cumulative_retained_pct"],
                                    name=p, mode="lines",
                                    line=dict(color=colors.get(p, "#4C72B0"))))
    
    fig.update_yaxes(type="log")
    fig.add_hline(y=100, line_dash="dash", line_color="gray")
    fig.update_layout(title="Potere d'acquisto dell'oro vs valute",
                      xaxis_title="Anno", yaxis_title="% retained (log)",
                      height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("L'oro ha preservato il valore in GBP per 768 anni. Il dollaro ha perso il 99.4%.")


elif pagina == "Code grasse":
    st.title("Code grasse e paradosso del peg")
    st.write("Ogni valuta mostra eventi estremi più frequenti della distribuzione normale.")
    
    vol = pd.read_csv(DATA / "derived" / "analysis" / "daily_volatility_stats.csv")
    
    # Scatter plot
    fig = px.scatter(vol, x="annualized_volatility", y="excess_kurtosis",
                     hover_data=["currency"],
                     title="Paradosso del Peg: Vol bassa ≠ Rischio basso",
                     labels={"annualized_volatility": "Volatilità annua",
                             "excess_kurtosis": "Curtosi in eccesso"})
    fig.update_yaxes(type="log")
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("HKD ha volatilità 3.2% ma curtosi 4109 — il peg comprime ma quando cede, esplode.")


elif pagina == "Regimi di cambio":
    st.title("Regimi di cambio nel tempo")
    st.write("Come i regimi (peg, float) cambiano nel tempo.")
    
    regime = pd.read_csv(DATA / "derived" / "analysis" / "yearly_regime_classification.csv")
    
    # Conteggio per decennio
    regime["decade"] = (regime["year"] // 10) * 10
    counts = regime.groupby(["decade", "regime_label"]).size().unstack(fill_value=0)
    
    fig = px.bar(counts, barmode="stack",
                 title="Distribuzione Regimi di Cambio nel Tempo",
                 labels={"value": "Numero di paesi", "decade": "Decennio"})
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("I peg dominano il 900°, poi cedono il passo ai float dopo Bretton Woods.")
