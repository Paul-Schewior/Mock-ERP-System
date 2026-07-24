import os
import sqlite3

DB_NAME = os.path.join(os.path.dirname(__file__), 'erp.db')

def verbindung_herstellen():
    try:
        verbindung = sqlite3.connect(DB_NAME, check_same_thread=False)
        verbindung.execute('PRAGMA foreign_keys = ON')
        return verbindung
    except sqlite3.Error as e:
        print(f'Datenbankfehler: {e}')
        return None

def db_initialisieren(verbindung):
    zeiger = verbindung.cursor()
    zeiger.execute('''CREATE TABLE IF NOT EXISTS kunden
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kundenname TEXT NOT NULL UNIQUE)''')
    
    zeiger.execute('''CREATE TABLE IF NOT EXISTS artikel
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    artikelname TEXT NOT NULL UNIQUE,
                    artikelpreis_cent INT NOT NULL)''')
    
    zeiger.execute('''CREATE TABLE IF NOT EXISTS bestaende
                    (artikel_id INTEGER PRIMARY KEY,
                    artikelbestand INT NOT NULL,
                    FOREIGN KEY (artikel_id) REFERENCES artikel(id))''')
    
    zeiger.execute('''CREATE TABLE IF NOT EXISTS bestellungen
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kunden_id INTEGER NOT NULL,
                    bestellstatus TEXT,
                    FOREIGN KEY (kunden_id) REFERENCES kunden(id))''')
    
    zeiger.execute('''CREATE TABLE IF NOT EXISTS bestellpositionen
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bestellung_id INTEGER NOT NULL,
                    artikel_id INTEGER NOT NULL,
                    bestellmenge INT NOT NULL,
                    FOREIGN KEY (bestellung_id) REFERENCES bestellungen(id),
                    FOREIGN KEY (artikel_id) REFERENCES artikel(id))''')
    
    verbindung.commit()
    