# Mock-ERP-System (Python + SQLite + Streamlit)

Simuliertes ERP-System zur Verwaltung von Kunden, Artikeln, Bestellungen und Lagerbeständen mit Python und Streamlit.

## Überblick

Dieses Projekt implementiert ein vereinfachtes ERP-System zur Verwaltung von Kunden, Artikeln, Lagerbeständen und Bestellungen.
Die Geschäftslogik wurde in Python entwickelt und nutzt SQLite als Datenbank. Die Interaktion mit ermöglicht die Streamlit-Oberfläche.
Der Fokus des Projektes liegt auf einer sauberen Datenbankstruktur, der Trennung der Geschäftslogik in einzelne Transaktionen und der Trennung von Backend-Logik, Datenbank-Aufbau und UI.

## Features

-Kunden anlegen, anzeigen und löschen
-Artikelverwaltung mit Preislogik
-Lagerbestände aktualisieren
-Bestellungen erstellen und Bestellpositionen hinzufügen
-Automatische Prüfung von Lagerbeständen bei Bestellabschluss
-Anzeige von Bestellübersichten inklusive Gesamtwert
-Benutzeroberfläche mit Streamlit

## Technologien

- Python
- SQLite
- Streamlit
- SQL (Joins, Aggregationen, Transaktionen)

## Installation 

```bash
git clone https://github.com/Paul-Schewior/Mock-ERP-System.git
cd mock-erp-system
pip install -r requirements.txt
```

Anwendung starten:
```bash
streamlit run app.py
```
