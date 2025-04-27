# utils/calculator.py

def calculate_scenarios(marca, modello, alimentazione,
                         km_annui, prezzo_auto, costo_gestione_annuo, valore_finale,
                         costo_km_aci, rimborso_fisso_km,
                         perc_detraibilita_iva, limite_deducibilita,
                         aliquota_ires, aliquota_irap, aliquota_irpef, perc_inps_dipendente,
                         aliquota_iva, perc_ammortamento, perc_fringe,
                         durata_anni,
                         costo_noleggio_mensile, manutenzione_inclusa,
                         tipo_trasferta,
                         addebito_fringe_fattura):

    risultati = {}
    spiegazioni = {}

    # --- Inizializza sezioni ---
    for scenario in [
        "Auto Aziendale - Azienda", "Auto Aziendale - Dipendente",
        "Rimborso km - Azienda", "Rimborso km - Dipendente",
        "Noleggio - Azienda", "Noleggio - Dipendente"
    ]:
        risultati[scenario] = {}
        spiegazioni[scenario] = {}

    # --- Auto Aziendale - Azienda ---
    iva_auto = prezzo_auto * aliquota_iva
    iva_detraibile = iva_auto * perc_detraibilita_iva
    costo_netto_auto = prezzo_auto - iva_detraibile
    base_ammortizzabile = min(costo_netto_auto, limite_deducibilita)
    ammortamento_annuo = base_ammortizzabile * perc_ammortamento
    quota_ammortamento_deducibile = ammortamento_annuo * 0.7
    quota_gestione_deducibile = costo_gestione_annuo * 0.7
    risparmio_ires_annuo = (quota_ammortamento_deducibile + quota_gestione_deducibile) * aliquota_ires
    risparmio_irap_annuo = (quota_ammortamento_deducibile + quota_gestione_deducibile) * aliquota_irap

    fringe_annuo = costo_km_aci * 15000 * perc_fringe
    fattura_dipendente_annua = fringe_annuo * 1.22 if addebito_fringe_fattura == "Si" else 0
    fringe_tassabile = max(fringe_annuo - fattura_dipendente_annua, 0)
    fringe_irpef_annuo = fringe_tassabile * aliquota_irpef
    fringe_inps_annuo = fringe_tassabile * perc_inps_dipendente

    costo_annuo = ammortamento_annuo + costo_gestione_annuo + fringe_annuo - risparmio_ires_annuo - risparmio_irap_annuo - (iva_detraibile / durata_anni)
    costo_totale = costo_annuo * durata_anni - valore_finale

    imposte_annue_dipendente = fringe_irpef_annuo + fringe_inps_annuo + fattura_dipendente_annua
    imposte_totali_dipendente = imposte_annue_dipendente * durata_anni

    # --- Riempimento risultati + spiegazioni Auto Azienda ---
    risultati["Auto Aziendale - Azienda"]["Ammortamento annuo (€)"] = round(ammortamento_annuo, 2)
    spiegazioni["Auto Aziendale - Azienda"]["Ammortamento annuo (€)"] = "Base ammortizzabile × % ammortamento"

    risultati["Auto Aziendale - Azienda"]["Costi gestione annui (€)"] = round(costo_gestione_annuo, 2)
    spiegazioni["Auto Aziendale - Azienda"]["Costi gestione annui (€)"] = "Costi fissi annuali di gestione del veicolo"

    risultati["Auto Aziendale - Azienda"]["Fringe benefit annuo (€)"] = round(fringe_annuo, 2)
    spiegazioni["Auto Aziendale - Azienda"]["Fringe benefit annuo (€)"] = "Costo/km ACI × 15.000 km × % fringe benefit"

    risultati["Auto Aziendale - Azienda"]["Risparmio IRES annuo (€)"] = round(-risparmio_ires_annuo, 2)
    spiegazioni["Auto Aziendale - Azienda"]["Risparmio IRES annuo (€)"] = "Quote deducibili × aliquota IRES"

    risultati["Auto Aziendale - Azienda"]["Risparmio IRAP annuo (€)"] = round(-risparmio_irap_annuo, 2)
    spiegazioni["Auto Aziendale - Azienda"]["Risparmio IRAP annuo (€)"] = "Quote deducibili × aliquota IRAP"

    risultati["Auto Aziendale - Azienda"]["Detrazione IVA annua (€)"] = round(-(iva_detraibile / durata_anni), 2)
    spiegazioni["Auto Aziendale - Azienda"]["Detrazione IVA annua (€)"] = "IVA detraibile ripartita sugli anni di ammortamento"

    risultati["Auto Aziendale - Azienda"]["Costo aziendale annuo (€)"] = round(costo_annuo, 2)
    spiegazioni["Auto Aziendale - Azienda"]["Costo aziendale annuo (€)"] = "Somma ammortamento + gestione + fringe - risparmi fiscali - IVA detraibile"

    risultati["Auto Aziendale - Azienda"]["Costo aziendale totale (€)"] = round(costo_totale, 2)
    spiegazioni["Auto Aziendale - Azienda"]["Costo aziendale totale (€)"] = "Costo annuo × durata anni - valore finale auto"
    
    # ...
    risultati["Auto Aziendale - Azienda"]["Costo aziendale totale (€)"] = round(costo_totale, 2)
    spiegazioni["Auto Aziendale - Azienda"]["Costo aziendale totale (€)"] = "Costo annuo × durata anni - valore finale auto"

    # --- INSERISCI QUI il codice dello scenario DIPENDENTE auto aziendale ---
    risultati["Auto Aziendale - Dipendente"]["Fringe benefit tassabile annuo (€)"] = round(fringe_tassabile, 2)
    spiegazioni["Auto Aziendale - Dipendente"]["Fringe benefit tassabile annuo (€)"] = "Fringe lordo - eventuale fattura dipendente"

    risultati["Auto Aziendale - Dipendente"]["IRPEF annua (€)"] = round(fringe_irpef_annuo, 2)
    spiegazioni["Auto Aziendale - Dipendente"]["IRPEF annua (€)"] = "Fringe tassabile × aliquota IRPEF"

    risultati["Auto Aziendale - Dipendente"]["INPS annua (€)"] = round(fringe_inps_annuo, 2)
    spiegazioni["Auto Aziendale - Dipendente"]["INPS annua (€)"] = "Fringe tassabile × aliquota INPS dipendente"

    risultati["Auto Aziendale - Dipendente"]["Fattura annua (€)"] = round(fattura_dipendente_annua, 2)
    spiegazioni["Auto Aziendale - Dipendente"]["Fattura annua (€)"] = "Fringe annuo × 1,22 se fatturato al dipendente"

    risultati["Auto Aziendale - Dipendente"]["Imposte totali annue (€)"] = round(imposte_annue_dipendente, 2)
    spiegazioni["Auto Aziendale - Dipendente"]["Imposte totali annue (€)"] = "Somma IRPEF + INPS + fattura dipendente"

    risultati["Auto Aziendale - Dipendente"]["Imposte totali periodo (€)"] = round(imposte_totali_dipendente, 2)
    spiegazioni["Auto Aziendale - Dipendente"]["Imposte totali periodo (€)"] = "Imposte totali annue × durata confronto"

    # --- fine scenario Auto Aziendale Dipendente ---

    # --- Rimborso km Dipendente ---
    rimborso_km_annuo = rimborso_fisso_km * km_annui
    risparmio_ires_rimborso = rimborso_km_annuo * aliquota_ires
    risparmio_irap_rimborso = rimborso_km_annuo * aliquota_irap

    if tipo_trasferta == "Fuori Comune":
        fringe_irpef_rimborso = 0
        fringe_inps_rimborso = 0
    else:
        fringe_irpef_rimborso = rimborso_km_annuo * aliquota_irpef
        fringe_inps_rimborso = rimborso_km_annuo * perc_inps_dipendente

    costo_azienda_rimborso_annuo = rimborso_km_annuo - risparmio_ires_rimborso - risparmio_irap_rimborso
    costo_azienda_rimborso_totale = costo_azienda_rimborso_annuo * durata_anni

    rimborso_netto_annuo = rimborso_km_annuo - (fringe_irpef_rimborso + fringe_inps_rimborso)
    rimborso_netto_totale = rimborso_netto_annuo * durata_anni
    
    # --- Costi auto privata dipendente ---
    ammortamento_annuo_dip = (prezzo_auto - valore_finale) / durata_anni
    costi_totali_annui_dip = ammortamento_annuo_dip + costo_gestione_annuo
    costo_totale_periodo_dip = costi_totali_annui_dip * durata_anni

    # Aggiungi risultati scenario dipendente auto privata
    risultati["Rimborso km - Dipendente"]["Ammortamento annuo auto (€)"] = round(ammortamento_annuo_dip, 2)
    spiegazioni["Rimborso km - Dipendente"]["Ammortamento annuo auto (€)"] = "Costo acquisto meno valore finale / anni"

    risultati["Rimborso km - Dipendente"]["Costi gestione annui (€)"] = round(costo_gestione_annuo, 2)
    spiegazioni["Rimborso km - Dipendente"]["Costi gestione annui (€)"] = "Costi annuali di manutenzione auto privata"

    risultati["Rimborso km - Dipendente"]["Costo totale annuo auto (€)"] = round(costi_totali_annui_dip, 2)
    spiegazioni["Rimborso km - Dipendente"]["Costo totale annuo auto (€)"] = "Ammortamento annuo + manutenzione annua"

    risultati["Rimborso km - Dipendente"]["Costo totale auto periodo (€)"] = round(costo_totale_periodo_dip, 2)
    spiegazioni["Rimborso km - Dipendente"]["Costo totale auto periodo (€)"] = "Costo totale annuo × durata anni"

    # Calcolo rimborso netto effettivo (meno costi auto)
    rimborso_netto_effettivo_totale = rimborso_netto_totale - costo_totale_periodo_dip

    risultati["Rimborso km - Dipendente"]["Rimborso netto effettivo totale (€)"] = round(rimborso_netto_effettivo_totale, 2)
    spiegazioni["Rimborso km - Dipendente"]["Rimborso netto effettivo totale (€)"] = "Rimborso netto totale meno costi totali auto privata"


    # --- Riempimento risultati + spiegazioni Rimborso km Azienda ---
    risultati["Rimborso km - Azienda"]["Rimborso km annuo (€)"] = round(rimborso_km_annuo, 2)
    spiegazioni["Rimborso km - Azienda"]["Rimborso km annuo (€)"] = "Rimborso €/km × km percorsi"

    risultati["Rimborso km - Azienda"]["Risparmio IRES annuo (€)"] = round(-risparmio_ires_rimborso, 2)
    spiegazioni["Rimborso km - Azienda"]["Risparmio IRES annuo (€)"] = "Rimborso deducibile × aliquota IRES"

    risultati["Rimborso km - Azienda"]["Risparmio IRAP annuo (€)"] = round(-risparmio_irap_rimborso, 2)
    spiegazioni["Rimborso km - Azienda"]["Risparmio IRAP annuo (€)"] = "Rimborso deducibile × aliquota IRAP"

    risultati["Rimborso km - Azienda"]["Costo aziendale annuo (€)"] = round(costo_azienda_rimborso_annuo, 2)
    spiegazioni["Rimborso km - Azienda"]["Costo aziendale annuo (€)"] = "Somma rimborso - risparmi fiscali"

    risultati["Rimborso km - Azienda"]["Costo aziendale totale (€)"] = round(costo_azienda_rimborso_totale, 2)
    spiegazioni["Rimborso km - Azienda"]["Costo aziendale totale (€)"] = "Costo annuo × durata anni"

    # --- Riempimento risultati + spiegazioni Rimborso km Dipendente ---
    risultati["Rimborso km - Dipendente"]["IRPEF annua (€)"] = round(fringe_irpef_rimborso, 2)
    spiegazioni["Rimborso km - Dipendente"]["IRPEF annua (€)"] = "Rimborso imponibile × aliquota IRPEF"

    risultati["Rimborso km - Dipendente"]["INPS annua (€)"] = round(fringe_inps_rimborso, 2)
    spiegazioni["Rimborso km - Dipendente"]["INPS annua (€)"] = "Rimborso imponibile × aliquota INPS"

    risultati["Rimborso km - Dipendente"]["Imposte totali annue (€)"] = round(fringe_irpef_rimborso + fringe_inps_rimborso, 2)
    spiegazioni["Rimborso km - Dipendente"]["Imposte totali annue (€)"] = "Somma IRPEF + INPS annue"

    risultati["Rimborso km - Dipendente"]["Imposte totali periodo (€)"] = round((fringe_irpef_rimborso + fringe_inps_rimborso) * durata_anni, 2)
    spiegazioni["Rimborso km - Dipendente"]["Imposte totali periodo (€)"] = "Totale imposte annue × durata anni"

    risultati["Rimborso km - Dipendente"]["Rimborso netto annuo (€)"] = round(rimborso_netto_annuo, 2)
    spiegazioni["Rimborso km - Dipendente"]["Rimborso netto annuo (€)"] = "Rimborso lordo - (IRPEF + INPS)"

    risultati["Rimborso km - Dipendente"]["Rimborso netto totale (€)"] = round(rimborso_netto_totale, 2)
    spiegazioni["Rimborso km - Dipendente"]["Rimborso netto totale (€)"] = "Rimborso netto annuo × durata anni"

    # --- Noleggio Auto Aziendale ---
    canone_noleggio_annuo = costo_noleggio_mensile * 12
    if manutenzione_inclusa == "No":
        canone_noleggio_annuo += costo_gestione_annuo

    fringe_noleggio_annuo = costo_km_aci * 15000 * perc_fringe

    if addebito_fringe_fattura == "Si":
        fattura_noleggio_annua = fringe_noleggio_annuo * 1.22
    else:
        fattura_noleggio_annua = 0

    fringe_noleggio_tassabile = max(fringe_noleggio_annuo - fattura_noleggio_annua, 0)
    fringe_noleggio_irpef_annuo = fringe_noleggio_tassabile * aliquota_irpef
    fringe_noleggio_inps_annuo = fringe_noleggio_tassabile * perc_inps_dipendente

    quota_deducibile_noleggio = min(canone_noleggio_annuo, 3615.20) * 0.7
    risparmio_ires_noleggio = quota_deducibile_noleggio * aliquota_ires
    risparmio_irap_noleggio = quota_deducibile_noleggio * aliquota_irap

    costo_annuo_noleggio = (
        canone_noleggio_annuo +
        fringe_noleggio_annuo -
        risparmio_ires_noleggio -
        risparmio_irap_noleggio
    )
    costo_totale_noleggio = costo_annuo_noleggio * durata_anni

    imposte_annue_noleggio = fringe_noleggio_irpef_annuo + fringe_noleggio_inps_annuo + fattura_noleggio_annua
    imposte_totali_noleggio = imposte_annue_noleggio * durata_anni

    # --- Riempimento risultati + spiegazioni Noleggio Azienda ---
    risultati["Noleggio - Azienda"]["Canone noleggio annuo (€)"] = round(canone_noleggio_annuo, 2)
    spiegazioni["Noleggio - Azienda"]["Canone noleggio annuo (€)"] = "Canone mensile × 12 (+ costi gestione se non inclusi)"

    risultati["Noleggio - Azienda"]["Fringe benefit annuo (€)"] = round(fringe_noleggio_annuo, 2)
    spiegazioni["Noleggio - Azienda"]["Fringe benefit annuo (€)"] = "Costo/km × 15.000 km × % fringe"

    risultati["Noleggio - Azienda"]["Risparmio IRES annuo (€)"] = round(-risparmio_ires_noleggio, 2)
    spiegazioni["Noleggio - Azienda"]["Risparmio IRES annuo (€)"] = "Quota deducibile × aliquota IRES"

    risultati["Noleggio - Azienda"]["Risparmio IRAP annuo (€)"] = round(-risparmio_irap_noleggio, 2)
    spiegazioni["Noleggio - Azienda"]["Risparmio IRAP annuo (€)"] = "Quota deducibile × aliquota IRAP"

    risultati["Noleggio - Azienda"]["Costo aziendale annuo (€)"] = round(costo_annuo_noleggio, 2)
    spiegazioni["Noleggio - Azienda"]["Costo aziendale annuo (€)"] = "Canone noleggio + fringe - risparmi fiscali"

    risultati["Noleggio - Azienda"]["Costo aziendale totale (€)"] = round(costo_totale_noleggio, 2)
    spiegazioni["Noleggio - Azienda"]["Costo aziendale totale (€)"] = "Costo aziendale annuo × durata anni"

    # --- Riempimento risultati + spiegazioni Noleggio Dipendente ---
    risultati["Noleggio - Dipendente"]["Fringe benefit tassabile (€)"] = round(fringe_noleggio_tassabile, 2)
    spiegazioni["Noleggio - Dipendente"]["Fringe benefit tassabile (€)"] = "Fringe lordo - eventuale fattura dipendente"

    risultati["Noleggio - Dipendente"]["IRPEF annua (€)"] = round(fringe_noleggio_irpef_annuo, 2)
    spiegazioni["Noleggio - Dipendente"]["IRPEF annua (€)"] = "Fringe tassabile × aliquota IRPEF"

    risultati["Noleggio - Dipendente"]["INPS annua (€)"] = round(fringe_noleggio_inps_annuo, 2)
    spiegazioni["Noleggio - Dipendente"]["INPS annua (€)"] = "Fringe tassabile × aliquota INPS"

    risultati["Noleggio - Dipendente"]["Fattura annua (€)"] = round(fattura_noleggio_annua, 2)
    spiegazioni["Noleggio - Dipendente"]["Fattura annua (€)"] = "Fringe annuo × 1,22 se fatturato"

    risultati["Noleggio - Dipendente"]["Imposte totali annue (€)"] = round(imposte_annue_noleggio, 2)
    spiegazioni["Noleggio - Dipendente"]["Imposte totali annue (€)"] = "Somma IRPEF + INPS + Fattura annua"

    risultati["Noleggio - Dipendente"]["Imposte totali periodo (€)"] = round(imposte_totali_noleggio, 2)
    spiegazioni["Noleggio - Dipendente"]["Imposte totali periodo (€)"] = "Totale imposte annue × durata anni"

    return {
        "risultati": risultati,
        "spiegazioni": spiegazioni
    }
