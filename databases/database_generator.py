import sqlite3
import sys
import os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mock_data import (
    create_orgs,
    create_new_research,
    create_approved_research, 
    create_rejected_research, 
    create_closed_research, 
    create_users, 
    create_research_registrations, 
    create_user_disabilities
)

class WP2DatabaseGenerator:
    def __init__(self, database_file, overwrite=False, initial_data=False):
        self.database_file = Path(database_file)
        self.create_initial_data = initial_data
        self.database_overwrite = overwrite
        self.test_file_location()
        self.conn = sqlite3.connect(self.database_file)

    def generate_database(self):
        self.create_table_beperkingen()
        self.create_table_organisaties()
        self.create_table_onderzoeken()
        self.create_table_gebruikers()
        self.create_table_gebruiker_onderzoek()
        self.create_table_gebruiker_beperking()
        self.create_table_admin_logs()
        if self.create_initial_data:
            self.insert_beperkingen()
            self.insert_organisaties()
            self.insert_onderzoeken()
            self.insert_gebruikers()
            self.insert_gebruiker_onderzoek()
            self.insert_gebruiker_beperking()
     
    def create_table_beperkingen(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS beperkingen (
            beperking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            beperking_naam TEXT NOT NULL,
            beperking_categorie TEXT NOT NULL            
            );
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Beperkingentabel aangemaakt")
           
    def create_table_organisaties(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS organisaties (
            organisatie_id INTEGER PRIMARY KEY AUTOINCREMENT,
            organisatie_naam TEXT UNIQUE NOT NULL,
            organisatie_type TEXT  NOT NULL,
            website TEXT UNIQUE,
            beschrijving TEXT,
            contactpersoon TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            wachtwoord TEXT NOT NULL,
            telefoonnummer TEXT,
            overige_details TEXT,
            status TEXT NOT NULL         
            );
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Organisatiestabel aangemaakt")
        
    def create_table_onderzoeken(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS onderzoeken (
            onderzoek_id INTEGER PRIMARY KEY AUTOINCREMENT,
            titel TEXT UNIQUE NOT NULL,
            status TEXT NOT NULL,
            beschikbaar INTEGER DEFAULT 0,
            beschrijving TEXT NOT NULL,
            begindatum TEXT NOT NULL,
            einddatum TEXT NOT NULL,
            onderzoek_type TEXT NOT NULL,
            locatie TEXT NOT NULL,
            met_beloning INTEGER,
            beloning TEXT,
            leeftijd_doelgroep_van INTEGER NOT NULL,
            leeftijd_doelgroep_tot INTEGER NOT NULL,
            beperking_categorie TEXT NOT NULL,
            organisatie_id INTEGER NOT NULL,
            FOREIGN KEY (organisatie_id) REFERENCES organisaties(organisatie_id) ON DELETE CASCADE
            );
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Onderzoekentabel aangemaakt")
        
    def create_table_gebruikers(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS gebruikers (
            gebruiker_id INTEGER PRIMARY KEY AUTOINCREMENT,
            voornaam TEXT NOT NULL,
            tussenvoegsel TEXT,
            achternaam TEXT NOT NULL,
            geboortedatum TEXT NOT NULL,
            geslacht TEXT,
            postcode TEXT,
            telefoonnummer TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            wachtwoord TEXT NOT NULL,
            hulpmiddelen TEXT,
            contact_voorkeur TEXT,
            introductie TEXT,
            onderzoektype_voorkeur TEXT,
            bijzonderheden_beperkingen TEXT,
            bijzonderheden_beschikbaarheid TEXT,
            status TEXT NOT NULL,
            beheerder INTEGER DEFAULT 0,
            voorwaarden_akkoord INTEGER DEFAULT 0,
            heeft_voogd INTEGER DEFAULT 0,
            naam_voogd TEXT,
            email_voogd TEXT,
            telefoonnummer_voogd TEXT
            );
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Gebruikerstabel aangemaakt")
    
    def create_table_gebruiker_onderzoek(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS gebruiker_onderzoek (
            onderzoek_id INTEGER,
            gebruiker_id INTEGER,
            status TEXT,
            PRIMARY KEY (onderzoek_id, gebruiker_id),
            FOREIGN KEY (onderzoek_id) REFERENCES onderzoeken(onderzoek_id) ON DELETE CASCADE,         
            FOREIGN KEY (gebruiker_id) REFERENCES gebruikers(gebruiker_id) ON DELETE CASCADE
            );
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Gebruiker/Onderzoektabel aangemaakt")
        
    def create_table_gebruiker_beperking(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS gebruiker_beperking (
            gebruiker_id INTEGER,
            beperking_id INTEGER,
            PRIMARY KEY (gebruiker_id, beperking_id),
            FOREIGN KEY (gebruiker_id) REFERENCES gebruikers(gebruiker_id) ON DELETE CASCADE,
            FOREIGN KEY (beperking_id) REFERENCES beperkingen(beperking_id) ON DELETE CASCADE  
            );
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Gebruiker/Beperkingtabel aangemaakt") 
         
    def create_table_admin_logs(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS admin_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER NOT NULL,
            actie TEXT NOT NULL,
            timestamp TEXT DEFAULT (DATETIME('now', 'localtime')),
            FOREIGN KEY (admin_id) REFERENCES gebruikers(gebruiker_id)           
            );
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Admin_logstabel aangemaakt")
        
    def insert_beperkingen(self):
        beperkingen = [
            ("Doof", "Auditieve beperkingen"),
            ("Slechthorend", "Auditieve beperkingen"),
            ("Doofblind", "Auditieve beperkingen"),
            ("Blind", "Visuele beperkingen"),
            ("Slechtziend", "Visuele beperkingen"),
            ("Kleurenblind", "Visuele beperkingen"),
            ("Doofblind", "Visuele beperkingen"),
            ("Amputatie en mismaaktheid", "Motorische / lichamelijke beperkingen"),
            ("Artritus", "Motorische / lichamelijke beperkingen"),
            ("Fibromyalgie", "Motorische / lichamelijke beperkingen"),
            ("Reuma", "Motorische / lichamelijke beperkingen"),
            ("Verminderde handvaardigheid", "Motorische / lichamelijke beperkingen"),
            ("Spierdystrofie", "Motorische / lichamelijke beperkingen"),
            ("RSI", "Motorische / lichamelijke beperkingen"),
            ("Tremor en Spasmen", "Motorische / lichamelijke beperkingen"),
            ("Quadriplegie of tetraplegie", "Motorische / lichamelijke beperkingen"),
            ("ADHD", "Cognitieve / neurologische beperkingen"),
            ("Autisme", "Cognitieve / neurologische beperkingen"),
            ("Dyslexie", "Cognitieve / neurologische beperkingen"),
            ("Dyscalculie", "Cognitieve / neurologische beperkingen"),
            ("Leerstoornis", "Cognitieve / neurologische beperkingen"),
            ("Geheugen beperking", "Cognitieve / neurologische beperkingen"),
            ("Multiple Sclerose", "Cognitieve / neurologische beperkingen"),
            ("Epilepsie", "Cognitieve / neurologische beperkingen"),
            ("Migraine", "Cognitieve / neurologische beperkingen")
        ]
        insert_statement = "INSERT INTO beperkingen (beperking_naam, beperking_categorie) VALUES (?, ?);"
        self.__execute_many_transaction_statement(insert_statement, beperkingen)
        print("✅ Beperkingen aangemaakt")
        
    def insert_organisaties(self):
        organisaties = create_orgs()
            
        insert_statement = """
        INSERT INTO organisaties (
            organisatie_naam, organisatie_type, website, beschrijving, contactpersoon, email, wachtwoord, telefoonnummer, overige_details, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        self.__execute_many_transaction_statement(insert_statement, organisaties)
        print("✅ Dummyorganisaties aangemaakt")
        
    def insert_onderzoeken(self):
        onderzoeken = create_new_research() + create_approved_research() + create_rejected_research() + create_closed_research()
        
        insert_statement = """
        INSERT INTO onderzoeken (
            titel, status, beschikbaar, beschrijving, begindatum, einddatum, onderzoek_type, locatie, met_beloning, beloning, leeftijd_doelgroep_van, leeftijd_doelgroep_tot, beperking_categorie, organisatie_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        self.__execute_many_transaction_statement(insert_statement, onderzoeken)
        print("✅ Dummyonderzoeken aangemaakt")
      
    def insert_gebruikers(self):
        gebruikers = create_users()
            
        insert_statement = """
        INSERT INTO gebruikers (
            voornaam, tussenvoegsel, achternaam, geboortedatum, geslacht, postcode, telefoonnummer, email, wachtwoord, hulpmiddelen, contact_voorkeur, introductie, onderzoektype_voorkeur, bijzonderheden_beperkingen, bijzonderheden_beschikbaarheid, status, beheerder, voorwaarden_akkoord, heeft_voogd, naam_voogd, email_voogd, telefoonnummer_voogd
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        self.__execute_many_transaction_statement(insert_statement, gebruikers)
        print("✅ Dummygebruikers aangemaakt")
        
    def insert_gebruiker_onderzoek(self):
        gebruiker_onderzoek = create_research_registrations()
        
        insert_statement = "INSERT INTO gebruiker_onderzoek (onderzoek_id, gebruiker_id, status) VALUES (?, ?, ?);"
        self.__execute_many_transaction_statement(insert_statement, gebruiker_onderzoek)
        print("✅ Gebruiker_onderzoek aangemaakt")
        
    def insert_gebruiker_beperking(self):
        gebruiker_beperking = create_user_disabilities()
        
        insert_statement = "INSERT INTO gebruiker_beperking (gebruiker_id, beperking_id) VALUES (?, ?);"
        self.__execute_many_transaction_statement(insert_statement, gebruiker_beperking)
        print("✅ Gebruiker_beperking aangemaakt")
        
    def __execute_many_transaction_statement(self, create_statement, list_of_parameters=()):
        c = self.conn.cursor()
        c.executemany(create_statement, list_of_parameters)
        self.conn.commit()

    def __execute_transaction_statement(self, create_statement, parameters=()):
        c = self.conn.cursor()
        c.execute(create_statement, parameters)
        self.conn.commit()

    def test_file_location(self):
        if self.database_file.exists():
            if not self.database_overwrite:
                raise ValueError(
                    f"Database file {self.database_file} already exists, set overwrite=True to overwrite"
                )
            else:
                self.database_file.unlink()
                print("✅ Database already exists, deleted")

        if not self.database_file.exists():
            try:
                self.database_file.touch()
                print("✅ New database setup")
            except Exception as e:
                raise ValueError(
                    f"Could not create database file {self.database_file} due to error {e}"
                )

if __name__ == "__main__":
    script_directory = Path(__file__).parent.resolve()
    database_path = script_directory / "database.db"

    database_generator = WP2DatabaseGenerator(
        database_path, overwrite=True, initial_data=True
    )
    database_generator.generate_database()