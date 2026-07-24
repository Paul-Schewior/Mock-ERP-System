import streamlit as st
import pandas as pd
from Daten.db import (verbindung_herstellen,
                db_initialisieren)
from Fachlogik.erp_logic import (kundenliste_anzeigen, 
                 kunde_anlegen,
                 kunde_löschen,
                 artikelliste_anzeigen,
                 artikel_anlegen,
                 artikel_löschen,
                 bestandliste_anzeigen,
                 bestand_anlegen,
                 bestand_ändern,
                 bestellliste_anzeigen,
                 bestellung_gesamtprozess,
                 bestellung_anzeigen)

verbindung = verbindung_herstellen()
db_initialisieren(verbindung)

seite = st.sidebar.selectbox('Navigation',
['Kunden',
'Artikel',
'Bestand',
'Bestellungen'])

#------------------------------------
#Kunden
#------------------------------------

if seite == 'Kunden':
    st.title('Kunden')

    #Kundenliste anzeigen

    erfolg, kunden = kundenliste_anzeigen(verbindung)
    if erfolg:
        st.dataframe(kunden)
    else:
        st.error(kunden)
    
    #Kunde anlegen

    st.subheader('Kunde anlegen')
    kundenname = st.text_input('Kundenname')
    if st.button('Anlegen'):
        erfolg, nachricht = kunde_anlegen(verbindung, kundenname)
        if erfolg:
            st.success(nachricht)
        else:
            st.error(nachricht)
    
    #Kunde löschen

    st.subheader('Kunde löschen')
    kunde_löschen_id = st.number_input('Kunden-ID', step = 1, min_value=1, key='kunde_löschen_id')
    if st.button('Löschen', key='kunde_löschen'):
        erfolg, nachricht = kunde_löschen(verbindung, kunde_löschen_id)
        if erfolg:
            st.success(nachricht)
        else:
            st.error(nachricht)

#------------------------------------
#Artikel
#------------------------------------

elif seite == 'Artikel':
    st.title('Artikel')

    #Artikelliste anzeigen

    erfolg, artikel_liste = artikelliste_anzeigen(verbindung)
    if erfolg:
        st.dataframe(artikel_liste)
    else:
        st.error(artikel_liste)

    #Artikel anlegen

    st.subheader('Artikel anlegen')
    artikelname = st.text_input('Artikelname')
    artikelpreis_cent = artikelpreis = st.number_input('Preis (€)',
                                                       min_value=0.0,
                                                       step=0.01,
                                                       format="%.2f")
    if st.button('Artikel anlegen'):
        erfolg, nachricht = artikel_anlegen(verbindung, artikelname, artikelpreis_cent)
        if erfolg:
            st.success(nachricht)
        else:
            st.error(nachricht)

    #Artikel löschen

    st.subheader('Artikel löschen')
    artikel_id_delete = st.number_input('Artikel-ID', step=1, min_value=1, key='artikel_löschen_id')

    if st.button('Löschen', key='artikel_löschen'):
        erfolg, nachricht = artikel_löschen(verbindung, artikel_id_delete)
        if erfolg:
            st.success(nachricht)
        else:
            st.error(nachricht)

#------------------------------------
#Bestand
#------------------------------------

elif seite == 'Bestand':
    st.title('Bestand')

    #Bestandliste anzeigen

    erfolg, bestandliste = bestandliste_anzeigen(verbindung)
    if erfolg:
        st.dataframe(bestandliste)
    else:
        st.error(bestandliste)

    #Bestand anlegen

    st.subheader('Bestand anlegen')
    bestand_artikel_id = st.number_input('Artikel-ID', step=1, min_value=1, key='bestand_ändern_id')
    bestand_neue_menge = st.number_input('Menge', step = 1, min_value=0)
    if st.button('Bestand anlegen'):
        erfolg, nachricht = bestand_anlegen(verbindung, bestand_artikel_id, bestand_neue_menge)
        if erfolg:
            st.success(nachricht)
        else:
            st.error(nachricht)

    #Bestand ändern

    st.subheader('Bestand ändern')
    artikel_id_update = st.number_input('Artikel-ID', step=1, min_value=1, key='bestand_update_id')
    bestand_anzahl = st.number_input('Neue Menge', step = 1, min_value=0, key='bestand_update_menge')
    if st.button('Bestand ändern'):
        erfolg, nachricht = bestand_ändern(verbindung, artikel_id_update, bestand_anzahl)
        if erfolg:
            st.success(nachricht)
        else: 
            st.error(nachricht)

#------------------------------------
#Bestellung
#------------------------------------

elif seite == 'Bestellungen':
    st.title('Bestellungen')

    #Bestellliste anzeigen

    erfolg, bestellungen = bestellliste_anzeigen(verbindung)
    if erfolg:
        st.dataframe(bestellungen)
    else: 
        st.error(bestellungen)

    #Bestellung anlegen (Gesamtprozess)

    st.subheader('Neue Bestellung anlegen')

    bestellung_kunde_id = st.number_input('Kunden-ID', step = 1, min_value = 1, key='bestellung_anlegen_id')

    st.markdown('Bestellpositionen')

    if 'positionen' not in st.session_state:
        st.session_state.positionen = []

    bestell_position_artikel_id = st.number_input('Artikel-ID', step=1, min_value=1, key='pos_artikel')
    bestellposition_menge = st.number_input('Menge', step=1, min_value=1, key='pos_menge')

    if st.button('Position hinzufügen'):
        if bestell_position_artikel_id:
            st.session_state.positionen.append((bestell_position_artikel_id, bestellposition_menge))
            st.success('Position hinzugefügt')
        else:
            st.error('Artikel-ID fehlt')

    if st.session_state.positionen:
        st.write('Aktuelle Positionen:')
        positionen_df = pd.DataFrame(
        st.session_state.positionen,
        columns=['Artikel-ID', 'Menge'])
        st.dataframe(positionen_df, 
                     use_container_width=True,
                     hide_index=True)

    if st.button('Positionen zurücksetzen'):
        st.session_state.positionen = []
        st.info('Positionen gelöscht')

    if st.button('Bestellung final anlegen'):
        erfolg, nachricht, bestellung_id = bestellung_gesamtprozess(
            verbindung,
            bestellung_kunde_id,
            st.session_state.positionen
        )

        if erfolg:
            st.success(f'{nachricht} (Bestell-ID: {bestellung_id})')
            st.session_state.positionen = []
        else:
            st.error(nachricht)

    #Bestellung anzeigen

    st.subheader('Bestellpositionen anzeigen')
    bestellung_id_show = st.number_input('Bestell-ID', step=1, min_value=1, key ='bestellung_anzeigen_id')
    if st.button('Bestellung anzeigen'):
        erfolg, bestellung = bestellung_anzeigen(verbindung, bestellung_id_show)
        if erfolg:
            st.dataframe(bestellung)
        else:
            st.error(bestellung)