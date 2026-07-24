import sqlite3

#------------------------------------
#Kunden anlegen
#------------------------------------

def kunde_anlegen(verbindung, kundenname):
    if not kundenname or kundenname.strip() == "":
        return False, 'Kundenname darf nicht leer sein'
    kundenname = kundenname.strip()
    try:
        verbindung.execute(
            '''INSERT INTO kunden 
            (kundenname) 
            VALUES (?)''', (kundenname, ))
        verbindung.commit()
        return True, f'Kunde {kundenname} erfolgreich angelegt'
    except sqlite3.IntegrityError:
        verbindung.rollback()
        return False, f'Kunde {kundenname} existiert bereits'
    except Exception as e:
        verbindung.rollback()
        return False, f'Fehler beim Anlegen des Kunden: {e}'

#------------------------------------
#Kunden löschen
#------------------------------------

def kunde_löschen(verbindung, kunden_id):
    if kunden_id is None:
        return False, 'Kunden-ID darf nicht leer sein'
    try:
        zeiger = verbindung.execute('''DELETE FROM kunden
                                    WHERE id = ? ''', (kunden_id, ))
        if zeiger.rowcount == 0:
            verbindung.rollback()
            return False, f'Kunde mit ID {kunden_id} existiert nicht'
        verbindung.commit()
        return True, f'Kunde {kunden_id} gelöscht'
    except Exception as e:
        verbindung.rollback()
        return False, f'Fehler bei Löschung: {e}'

#------------------------------------
#Artikel anlegen
#------------------------------------

def artikel_anlegen(verbindung, artikelname, artikelpreis):
    if not artikelname or artikelname.strip() == "":
        return False, 'Artikelname darf nicht leer sein'
    try:
        artikelpreis = str(artikelpreis).replace(',', '.')
        artikelpreis_cent = int(round(float(artikelpreis)* 100))
    except ValueError:
        return False, 'Artikelpreis ist ungültig. Bitte z.B. 2,99 eingeben'
    if artikelpreis_cent < 0:
        return False, 'Artikelpreis darf nicht negativ sein'
    artikelname = artikelname.strip()
    try:
        verbindung.execute('''INSERT INTO artikel 
                           (artikelname, artikelpreis_cent)
                           VALUES (?, ?)
                           ''', (artikelname, artikelpreis_cent))
        verbindung.commit()
        return True, f'Artikel {artikelname} erfolgreich angelegt'
    except sqlite3.IntegrityError:
        verbindung.rollback()
        return False, f'Artikel mit ID oder Name existiert bereits'
    except Exception as e:
        verbindung.rollback()
        return False, f'Fehler beim Anlegen des Artikels: {e}'

#------------------------------------
#Artikel löschen
#------------------------------------

def artikel_löschen(verbindung, artikel_id):
    if artikel_id is None:
        return False, 'Artikel-ID darf nicht leer sein'
    zeiger = verbindung.cursor()
    try:
        verbindung.execute('BEGIN IMMEDIATE')
        zeiger.execute('''SELECT 1
                       FROM artikel
                       WHERE id = ? ''', (artikel_id, ))
        if zeiger.fetchone() is None:
            verbindung.rollback()
            return False, f'Artikel mit ID {artikel_id} existiert nicht'
        zeiger.execute('''SELECT 1
                    FROM bestellpositionen 
                    WHERE artikel_id = ? ''', (artikel_id, ))
        if zeiger.fetchone() is not None:
            verbindung.rollback()
            return False, f'Für Artikel {artikel_id} existieren Bestellungen'
        zeiger.execute('''DELETE FROM artikel
                    WHERE id = ? ''', (artikel_id, ))
        verbindung.commit()
        return True, f'Artikel {artikel_id} erfolgreich gelöscht'
    except Exception as e:
        verbindung.rollback()
        return False, f'Fehler bei der Löschung des Artikels: {e}'

#------------------------------------
#Bestand anlegen 
#------------------------------------

def bestand_anlegen(verbindung, artikel_id, bestand_anzahl):
    if artikel_id is None:
        return False, 'Artikel-ID darf nicht leer sein'
    if bestand_anzahl is None or bestand_anzahl < 0:
        return False, 'Bestand ist ungültig'
    try:
        verbindung.execute('''INSERT INTO bestaende
                           (artikel_id, artikelbestand)
                           VALUES (?, ?) ''', (artikel_id, bestand_anzahl))
        verbindung.commit()
        return True, f'Bestand von {bestand_anzahl} für Artikel {artikel_id} erfolgreich angelegt'
    except sqlite3.IntegrityError:
        verbindung.rollback()
        return False, 'Artikel existiert nicht oder Bestand bereits vorhanden'
    except Exception as e:
        verbindung.rollback()
        return False, f'Fehler beim Anlegen des Bestands: {e}'

#------------------------------------
#Bestand ändern
#------------------------------------

def bestand_ändern(verbindung, artikel_id, bestand_anzahl):
    if artikel_id is None:
        return False, 'Artikel-ID darf nicht leer sein'
    if bestand_anzahl is None:
        return False, 'Bestand darf nicht leer sein'
    if bestand_anzahl < 0:
        return False, 'Bestand darf nicht negativ sein'
    try:
        zeiger = verbindung.cursor()
        zeiger.execute('''UPDATE bestaende
                    SET artikelbestand = ?
                    WHERE artikel_id = ? ''', (bestand_anzahl, artikel_id))
        if zeiger.rowcount == 0:
            return False, 'Artikel oder Bestand nicht vorhanden'
        verbindung.commit()
        return True, f'Bestand für Artikel {artikel_id} aktualisiert'
    except Exception as e:
        verbindung.rollback()
        return False, f'Fehler beim Ändern des Bestands: {e}'
 
#------------------------------------
#Bestellung anlegen
#------------------------------------

def bestellung_anlegen(verbindung, kunden_id):
    if kunden_id is None:
        return False, 'Kunden-ID darf nicht leer sein'
    try:
        zeiger = verbindung.cursor()
        zeiger.execute('''INSERT INTO bestellungen
                    (kunden_id, bestellstatus)
                    VALUES (?, "offen")''', (kunden_id, ))
        bestellung_id = zeiger.lastrowid
        return True, f'Bestellung erfolgreich angelegt', bestellung_id
    except Exception as e:
        return False, f'Datenbankfehler beim Anlegen der Bestellung: {e}', None

#------------------------------------
#Neue bestellposition hinzufügen
#------------------------------------
    
def bestellpositionen_hinzufügen(verbindung, bestellung_id, positionen):
    if not positionen:
        return False, 'Keine Positionen übergeben'
    try:
        zeiger = verbindung.cursor()
        daten = [(bestellung_id, artikel_id, bestellmenge) 
                 for artikel_id, bestellmenge in positionen]
        zeiger.executemany('''INSERT INTO bestellpositionen
                           (bestellung_id, artikel_id, bestellmenge) 
                           VALUES (?, ?, ?) ''', daten)
        return True, 'Bestellpositionen wurden angelegt'
    except Exception as e:
        return False, f'Datenbankfehler beim Anlegen der Bestellpositionen: {e}'


#------------------------------------
#bestellung finalisieren
#------------------------------------

def bestellung_finalisieren(verbindung, bestellung_id):
    zeiger = verbindung.cursor()
    try:
        zeiger.execute('''SELECT bp.artikel_id, bp.bestellmenge, b.artikelbestand
                       FROM bestellpositionen bp INNER JOIN bestaende b
                       ON bp.artikel_id = b.artikel_id
                       WHERE bp.bestellung_id = ? ''', (bestellung_id, ))
        positionen = zeiger.fetchall()
        for artikel_id, bestellmenge, bestand in positionen:
            if bestand is None:
                return False, f'Kein Bestand für Artikel {artikel_id}'
            if bestellmenge > bestand:
                return False, f'Zu wenig Bestand für Artikel {artikel_id}'
        for artikel_id, bestellmenge, bestand in positionen:
            zeiger.execute('''UPDATE bestaende
                           SET artikelbestand = ?
                           WHERE artikel_id = ? ''', (bestand - bestellmenge, artikel_id))
        zeiger.execute("""UPDATE bestellungen
                       SET bestellstatus = 'finalisiert'
                       WHERE id = ? """, (bestellung_id, ))
        return True, f'Bestellung {bestellung_id} wurde finalisiert'
    except Exception as e:
        return False, f'Datenbankfehler beim Finalisieren der Bestellung: {e}'

#------------------------------------
#Finalisieren Button Wrapper
#------------------------------------

def bestellung_gesamtprozess(verbindung, kunden_id, positionen):
    try:
        verbindung.execute('BEGIN IMMEDIATE')
        erfolg, nachricht, bestellung_id = bestellung_anlegen(verbindung, kunden_id)
        if not erfolg:
            verbindung.rollback()
            return False, nachricht, None
        erfolg, nachricht = bestellpositionen_hinzufügen(verbindung, bestellung_id, positionen)
        if not erfolg:
            verbindung.rollback()
            return False, nachricht, None
        erfolg, nachricht = bestellung_finalisieren(verbindung, bestellung_id)
        if not erfolg:
            verbindung.rollback()
            return False, nachricht, None
        verbindung.commit()
        return True, 'Bestellung erfolgreich vollständig angelegt', bestellung_id
    except Exception as e:
        verbindung.rollback()
        return False, f'Datenbankfehler: {e}', None

#------------------------------------
#Kundenliste anzeigen
#------------------------------------
    
def kundenliste_anzeigen(verbindung):
    try:
        zeiger = verbindung.cursor()
        zeiger.execute('''SELECT id,
                       kundenname
                       FROM kunden
                       ORDER BY id''')
        reihen = zeiger.fetchall()
        kunden = []
        for reihe in reihen:
            kunden.append({'ID': reihe[0], 
                           'Kundenname': reihe[1],})
        return True, kunden
    except Exception as e:
        return False, f'Fehler beim Laden der Kundenliste: {e}'
    
#------------------------------------
#Artikelliste anzeigen
#------------------------------------
    
def artikelliste_anzeigen(verbindung):
    try:
        zeiger = verbindung.cursor()
        zeiger.execute('''SELECT id,
                      artikelname,
                      artikelpreis_cent
                      FROM artikel
                      ORDER BY id''')
        reihen = zeiger.fetchall()
        artikel = []
        for reihe in reihen:
            preis_euro = reihe[2] / 100
            preis_formatiert = f"{preis_euro:.2f} €".replace('.', ',')
            artikel.append({'ID': reihe[0], 
                            'Artikelname': reihe[1], 
                            'Artikelpreis': preis_formatiert})
        return True, artikel
    except Exception as e:
        return False, f'Fehler beim Laden der Artikelliste: {e}'

#------------------------------------
#Bestandliste anzeigen
#------------------------------------

def bestandliste_anzeigen(verbindung):
    try:
        zeiger = verbindung.cursor()
        zeiger.execute('''SELECT a.id,
                    a.artikelname,
                    b.artikelbestand
                    FROM artikel a INNER JOIN bestaende b ON a.id = b.artikel_id
                    ORDER BY id''')
        reihen = zeiger.fetchall()
        bestand = []
        for reihe in reihen:
            bestand.append({'ID': reihe[0],
                            'Artikelname': reihe[1],
                            'Bestandsmenge': reihe[2]})
        return True, bestand
    except Exception as e:
        return False, f'Fehler beim Laden des Bestands: {e}'

#------------------------------------
#Bestellung anzeigen
#------------------------------------
    
def bestellung_anzeigen(verbindung, bestellung_id):
    if bestellung_id is None:
        return False, 'Bestell-ID fehlt'

    try:
        zeiger = verbindung.cursor()

        zeiger.execute('''
            SELECT 
                b.kunden_id,
                k.kundenname,
                bp.artikel_id,
                a.artikelname,
                bp.bestellmenge,
                (bp.bestellmenge * a.artikelpreis_cent) AS positionswert_cent
            FROM bestellungen b
            INNER JOIN bestellpositionen bp
                ON b.id = bp.bestellung_id
            INNER JOIN artikel a
                ON bp.artikel_id = a.id
            INNER JOIN kunden k
                ON b.kunden_id = k.id
            WHERE b.id = ?
        ''', (bestellung_id, ))

        positionen = zeiger.fetchall()

        if not positionen:
            return False, f'Bestellung mit ID {bestellung_id} nicht gefunden'

        bestellungsliste = []

        for pos in positionen:
            bestellungsliste.append({
                'Kunden-ID': pos[0],
                'Kundenname': pos[1],
                'Artikel-ID': pos[2],
                'Artikelname': pos[3],
                'Bestellmenge': pos[4],
                'Positionswert': f"{pos[5] / 100:.2f} €".replace('.', ',')
            })

        return True, bestellungsliste

    except Exception as e:
        return False, f'Fehler beim Laden der Bestellung: {e}'
        
#------------------------------------
#Bestellliste anzeigen
#------------------------------------        

def bestellliste_anzeigen(verbindung):
    try:
        zeiger = verbindung.cursor()

        zeiger.execute('''
            SELECT 
                b.id,
                b.kunden_id,
                k.kundenname,
                b.bestellstatus,
                COALESCE(SUM(bp.bestellmenge * a.artikelpreis_cent), 0) AS gesamtwert_cent
            FROM bestellungen b
            INNER JOIN kunden k
                ON b.kunden_id = k.id
            LEFT JOIN bestellpositionen bp
                ON b.id = bp.bestellung_id
            LEFT JOIN artikel a
                ON bp.artikel_id = a.id
            GROUP BY 
                b.id,
                b.kunden_id,
                k.kundenname,
                b.bestellstatus
            ORDER BY b.id
        ''')

        reihen = zeiger.fetchall()

        bestellungen = []

        for reihe in reihen:
            bestellungen.append({
                'Bestellung-ID': reihe[0],
                'Kunden_ID': reihe[1],
                'Kundenname': reihe[2],
                'Bestellstatus': reihe[3],
                'Gesamtwert der Bestellung': f"{reihe[4] / 100:.2f} €".replace('.', ',')
            })

        return True, bestellungen

    except Exception as e:
        return False, f'Fehler beim Laden der Bestellliste: {e}'
    



    




    






#Liste an Funktionen:
    # 1. Kunden anlegen 
    # 2. Kunden löschen 
    # 3. Artikel anlegen 
    # 4. Artikel löschen 
    # 5. Bestand anlegen 
    # 6. Bestand ändern 
    # 7. Bestellung anlegen 
    # 8. Bestellpositionen hinzufügen 
    # 9. Bestellung finalisieren 
    # 10. Wrapper Funktion
    # 11. Kunde anzeigen
    # 12. Kundenliste anzeigen
    # 13. Artikel anzeigen
    # 14. Artikelliste anzeigen
    # 15. Bestand anzeigen
    # 16. Bestandliste anzeigen
    # 17 Bestellung anzeigen
    # 18. Bestellliste anzeigen

#To-Do Liste:
    #Anführungszeichen überprüfen bei allen Funktionen
    #prüfen ob alle db namen richtig verwendet werden



#Umlaute anpassen