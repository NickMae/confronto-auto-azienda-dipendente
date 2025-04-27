# app_definitivo.py

import streamlit as st
import pandas as pd
import requests
from st_aggrid import AgGrid, GridOptionsBuilder
from utils.calculator import calculate_scenarios
from utils.data_loader import load_aci_data

st.set_page_config(page_title="Confronto Auto Azienda vs Dipendente 2025", layout="wide")
st.title("🚗 Confronto Auto Azienda vs Dipendente (Italia 2025)")

aci_data = load_aci_data()

# --- Sidebar Input ---
with st.sidebar:
    st.header("🛠️ Parametri di Input")

    marca = st.selectbox("Marca", sorted(aci_data['MARCA'].unique()))
    modello = st.selectbox("Modello", sorted(aci_data[aci_data['MARCA'] == marca]['MODELLO'].unique()))
    alimentazione = st.selectbox("Alimentazione", sorted(aci_data[aci_data['MARCA'] == marca]['TIPO_ALIMENTAZIONE'].unique()))

    km_annui = st.number_input("Km percorsi annui", min_value=0, step=1000)

    # Tentativo di recupero prezzo auto online
    prezzo_auto = 0
    try:
        query = f"prezzo {marca} {modello} auto nuova"
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        if response.ok and "€" in response.text:
            prezzo_str = response.text.split("€")[1].split()[0].replace('.', '').replace(',', '')
            prezzo_auto = int(prezzo_str)
    except:
        pass

    prezzo_auto = st.number_input("Prezzo auto (€)", min_value=0, value=prezzo_auto, step=500)

    if prezzo_auto == 0:
        st.warning("❗ Prezzo non trovato automaticamente. Inserisci manualmente.")

    costo_gestione_annuo = st.number_input("Costi gestione annui (€)", min_value=0, step=500)
    valore_finale = st.number_input("Valore finale auto (€)", min_value=0, step=500)
    rimborso_fisso_km = st.number_input("Rimborso €/km riconosciuto", min_value=0.0, step=0.01)
    costo_noleggio_mensile = st.number_input("Costo noleggio mensile (€)", min_value=0, step=50)
    manutenzione_inclusa = st.radio("Manutenzione inclusa nel noleggio?", ("Si", "No"))
    tipo_trasferta = st.radio("Tipo Trasferta?", ("Fuori Comune", "Dentro Comune"))
    addebito_fringe_fattura = st.radio("Addebito fringe benefit con fattura al dipendente?", ("No", "Si"))
    durata_anni = st.slider("Durata confronto (anni)", 1, 10, 5)

    with st.expander("⚙️ Altre Impostazioni Avanzate"):
        perc_detraibilita_iva = st.slider("Detraibilità IVA (%)", 0, 100, 40, step=1) / 100
        limite_deducibilita = st.number_input("Limite deducibilità (€)", value=18075.99)
        aliquota_ires = st.slider("Aliquota IRES (%)", 0, 50, 24, step=1) / 100
        aliquota_irap = st.slider("Aliquota IRAP (%)", 0.0, 10.0, 3.9, step=0.1) / 100
        perc_inps_dipendente = st.slider("% Contributi INPS Dipendente", 0.0, 50.0, 9.19, step=0.01) / 100
        aliquota_irpef = st.slider("Aliquota IRPEF Dipendente (%)", 0, 50, 30, step=1) / 100
        aliquota_iva = st.slider("Aliquota IVA (%)", 0, 30, 22, step=1) / 100
        perc_ammortamento = st.slider("% Ammortamento annuo", 0, 30, 20, step=1) / 100
        perc_fringe = st.slider("% Rilevanza Fringe Benefit", 0, 100, 50, step=1) / 100
		
try:
    costo_km_aci = aci_data[
        (aci_data['MARCA'] == marca) &
        (aci_data['MODELLO'] == modello) &
        (aci_data['TIPO_ALIMENTAZIONE'] == alimentazione)
    ].iloc[0]['COSTO_KM_15000KM']
except IndexError:
    st.error("❌ Errore: Costo/km ACI non trovato!")
    costo_km_aci = 0

st.sidebar.success(f"Costo/km ACI: {costo_km_aci:.3f} €/km")

# --- Calcolo ---
if st.sidebar.button("🚀 Confronta Scenari"):
    costo_km_aci = aci_data[
        (aci_data['MARCA'] == marca) &
        (aci_data['MODELLO'] == modello) &
        (aci_data['TIPO_ALIMENTAZIONE'] == alimentazione)
    ].iloc[0]['COSTO_KM_15000KM']

    output = calculate_scenarios(
        marca, modello, alimentazione,
        km_annui, prezzo_auto, costo_gestione_annuo, valore_finale,
        costo_km_aci, rimborso_fisso_km,
        perc_detraibilita_iva, limite_deducibilita,
        aliquota_ires, aliquota_irap, aliquota_irpef, perc_inps_dipendente,
        aliquota_iva, perc_ammortamento, perc_fringe,
        durata_anni,
        costo_noleggio_mensile, manutenzione_inclusa,
        tipo_trasferta,
        addebito_fringe_fattura
    )

    risultati = output["risultati"]
    spiegazioni = output["spiegazioni"]

    st.header(f"📊 Confronto Scenari ({durata_anni} anni)")

    scenari = {
        "Auto Aziendale": ("Auto Aziendale - Azienda", "Auto Aziendale - Dipendente"),
        "Rimborso km": ("Rimborso km - Azienda", "Rimborso km - Dipendente"),
        "Noleggio": ("Noleggio - Azienda", "Noleggio - Dipendente"),
    }

    for scenario_label, (scenario_azienda, scenario_dipendente) in scenari.items():
        st.subheader(f"🔹 Scenario: {scenario_label}")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🏢 Azienda")
            df_azienda = pd.DataFrame({
                "Descrizione": list(risultati[scenario_azienda].keys()),
                "Valore (€)": [f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") for v in risultati[scenario_azienda].values()],
                "Spiegazione": [spiegazioni.get(scenario_azienda, {}).get(k, "Nessuna spiegazione disponibile") for k in risultati[scenario_azienda].keys()]
            })

            gb = GridOptionsBuilder.from_dataframe(df_azienda)
            gb.configure_column("Descrizione", headerTooltip="Campo")
            gb.configure_column("Valore (€)", type=["textColumn"])
            gb.configure_column("Spiegazione", tooltipField="Spiegazione")
            grid_options = gb.build()

            AgGrid(df_azienda, gridOptions=grid_options, enable_enterprise_modules=False, key=f"azienda_{scenario_label}")

        with col2:
            st.markdown("### 👤 Dipendente")
            df_dip = pd.DataFrame({
                "Descrizione": list(risultati[scenario_dipendente].keys()),
                "Valore (€)": [f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") for v in risultati[scenario_dipendente].values()],
                "Spiegazione": [spiegazioni.get(scenario_dipendente, {}).get(k, "Nessuna spiegazione disponibile") for k in risultati[scenario_dipendente].keys()]
            })

            gb2 = GridOptionsBuilder.from_dataframe(df_dip)
            gb2.configure_column("Descrizione", headerTooltip="Campo")
            gb2.configure_column("Valore (€)", type=["textColumn"])
            gb2.configure_column("Spiegazione", tooltipField="Spiegazione")
            grid_options2 = gb2.build()

            AgGrid(df_dip, gridOptions=grid_options2, enable_enterprise_modules=False, key=f"dipendente_{scenario_label}")

        st.divider()

    # --- Scenario migliore ---
    st.header("🏆 Scenario Consigliato")

    costo_auto_azienda = risultati["Auto Aziendale - Azienda"]["Costo aziendale totale (€)"]
    costo_rimborso_azienda = risultati["Rimborso km - Azienda"]["Costo aziendale totale (€)"]
    costo_noleggio_azienda = risultati["Noleggio - Azienda"]["Costo aziendale totale (€)"]

    costo_auto_dipendente = risultati["Auto Aziendale - Dipendente"]["Imposte totali periodo (€)"]
    costo_noleggio_dipendente = risultati["Noleggio - Dipendente"]["Imposte totali periodo (€)"]
    costo_rimborso_dipendente_netto = -risultati["Rimborso km - Dipendente"]["Rimborso netto effettivo totale (€)"]

    totali_combinati = {
        "Auto Aziendale": costo_auto_azienda + costo_auto_dipendente,
        "Rimborso km": costo_rimborso_azienda + costo_rimborso_dipendente_netto,
        "Noleggio": costo_noleggio_azienda + costo_noleggio_dipendente
    }

    scenario_migliore_combinato = min(totali_combinati, key=totali_combinati.get)
    costo_migliore_combinato = totali_combinati[scenario_migliore_combinato]

    st.success(
        f"✅ Scenario più conveniente (azienda + dipendente): "
        f"**{scenario_migliore_combinato}** con costo totale combinato di "
        f"**{costo_migliore_combinato:,.2f} €**"
    )

    st.markdown("#### 🔍 Dettaglio scenario consigliato")
    if scenario_migliore_combinato == "Rimborso km":
        dettaglio_dipendente = risultati["Rimborso km - Dipendente"]["Rimborso netto effettivo totale (€)"]
    else:
        dettaglio_dipendente = -risultati[scenario_migliore_combinato + " - Dipendente"]["Imposte totali periodo (€)"]

    st.write(pd.DataFrame({
        "Soggetto": ["Azienda", "Dipendente", "**Totale combinato**"],
        "Costo Totale (€)": [
            f"{risultati[scenario_migliore_combinato + ' - Azienda']['Costo aziendale totale (€)']:,.2f}",
            f"{dettaglio_dipendente:,.2f}",
            f"**{costo_migliore_combinato:,.2f}**"
        ]
    }))


    st.caption("🛡️ Basato su normativa fiscale italiana 2025 - Tabelle ACI aggiornate")
