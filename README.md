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

## Nutzung

Die Anwendung wird über eine Streamlit-Oberfläche gesteuert.

- Über die Sidebar können die verschiedenen Bereiche (Kunden, Artikel, Bestand und Bestellungen) ausgewählt werden.
- Zunächst können Kunden und Artikel angelegt und verwaltet werden.
- Anschließend können Lagerbestände für Artikel erstellt und angepasst werden.
- Im Bereich Bestellungen können neue Bestellungen erstellt und mit Artikeln ergänzt werden.
- Beim Finalisieren einer Bestellung wird automatisch geprüft, ob ausreichend Lagerbestand vorhanden ist. Bei erfolgreicher Prüfung wird der Bestand aktualisiert und die Bestellung abgeschlossen.

## Projektstruktur

- app.py → Streamlit-Oberfläche
- erp.py → Geschäftslogik und Datenbankoperationen
- erp.db → SQLite-Datenbank
- requirements.txt → Abhängigkeiten

## Beispiel / Output

Die Anwendung ermöglicht:
- Anzeige von Kunden- und Artikellisten
- Verwaltung von Lagerbeständen
- Erstellung und Auswertung von Bestellungen inklusive Gesamtwert

## Learnings

- Umsetzung einer relationalen Datenbankstruktur mit SQLite
- Arbeiten mit SQL (Joins, Aggregationen, Transaktionen)
- Einsatz von Transaktionen zur Sicherstellung von Datenkonsistenz
- Trennung von Geschäftslogik und Benutzeroberfläche
- Umgang mit Fehlerfällen (z. B. unzureichender Lagerbestand)
- Entwicklung einer einfachen UI mit Streamlit
