from models.model import Model
from utils import verify_plain_text, hash_plain_text


class UserModel(Model):

    def check_user_login(self, email, password):
        query = """
        SELECT *
        FROM gebruikers
        WHERE email = ?
        """
        
        result = self.fetch_one(query, email)
        if result:
            if verify_plain_text(password, result["wachtwoord"]):
                return result
        return None

    def get_all_user(self, search_term, sort_by, order):
        args = []

        query = """
        SELECT *
        FROM gebruikers
        WHERE status = 'Nieuw'
        """
        
        if search_term:
            query += """
             AND (
                LOWER(voornaam) LIKE LOWER(?)
                OR LOWER(achternaam) LIKE LOWER(?)
                OR LOWER(email) LIKE LOWER(?)
                OR LOWER(status) LIKE LOWER(?)
            )
            """
            args.extend([f"%{search_term}%"] * 4)
            
        if sort_by:
            query += f" ORDER BY {sort_by} {order}"
            
        if args:
            return self.fetch_all(query, *args)
        
        return self.fetch_all(query)
        
    def get_user(self, user_id):
        query = """
        SELECT *
        FROM gebruikers
        WHERE gebruiker_id = ?;
        """
        return self.fetch_one(query, user_id)

    def create_user(self, data):
        email = data.get("email")
        wachtwoord = data.get("wachtwoord")
        voornaam = data.get("voornaam")
        tussenvoegsel = data.get("tussenvoegsel") or None
        achternaam = data.get("achternaam")
        geboortedatum = data.get("geboortedatum")
        geslacht = data.get("geslacht")
        postcode = data.get("postcode")
        telefoonnummer = data.get("telefoonnummer")
        introductie = data.get("introductie") or None
        hulpmiddelen = data.get("hulpmiddelen") or None
        contact_voorkeur = data.get("contact_voorkeur") or None
        onderzoektype_voorkeur = data.get("onderzoektype_voorkeur")
        heeft_voogd = data.get("heeft_voogd") or None
        naam_voogd = data.get("naam_voogd") if heeft_voogd else None
        email_voogd = data.get("email_voogd")  if heeft_voogd else None
        telefoonnummer_voogd = data.get("telefoonnummer_voogd")  if heeft_voogd else None
        status = "Nieuw"
        voorwaarden_akkoord = 1

        query = """
        INSERT INTO gebruikers
        (email,
        wachtwoord,
        voornaam,
        tussenvoegsel,
        achternaam,
        geboortedatum,
        geslacht,
        postcode,
        telefoonnummer,
        introductie,
        hulpmiddelen,
        contact_voorkeur,
        onderzoektype_voorkeur,
        heeft_voogd,
        naam_voogd,
        email_voogd,
        telefoonnummer_voogd,
        status,
        voorwaarden_akkoord)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        return self.insert_one(query,
                                email, hash_plain_text(wachtwoord), voornaam, tussenvoegsel, achternaam,
                                geboortedatum, geslacht, postcode, telefoonnummer, introductie,
                                hulpmiddelen, contact_voorkeur, onderzoektype_voorkeur, heeft_voogd, naam_voogd,
                                email_voogd, telefoonnummer_voogd, status, voorwaarden_akkoord)
    
    def update_user(self, user_id, data):
        email = data.get("email")
        huidig_wachtwoord = self.get_current_password(user_id)["wachtwoord"]
        wachtwoord = data.get("wachtwoord") or huidig_wachtwoord
        voornaam = data.get("voornaam")
        tussenvoegsel = data.get("tussenvoegsel") or None
        achternaam = data.get("achternaam")
        geboortedatum = data.get("geboortedatum")
        geslacht = data.get("geslacht")
        postcode = data.get("postcode")
        telefoonnummer = data.get("telefoonnummer")
        introductie = data.get("introductie")
        hulpmiddelen = data.get("hulpmiddelen")
        contact_voorkeur = data.get("contact_voorkeur")
        onderzoektype_voorkeur = data.get("onderzoektype_voorkeur", None)
        heeft_voogd = data.get("heeft_voogd")
        naam_voogd = data.get("naam_voogd") if heeft_voogd else None
        email_voogd = data.get("email_voogd")  if heeft_voogd else None
        telefoonnummer_voogd = data.get("telefoonnummer_voogd")  if heeft_voogd else None
        status = "Goedgekeurd"
        voorwaarden_akkoord = 1

        query = """
        UPDATE gebruikers
        SET
        email = ?,
        wachtwoord = ?,
        voornaam = ?,
        tussenvoegsel = ?,
        achternaam = ?,
        geboortedatum = ?,
        geslacht = ?,
        postcode = ?,
        telefoonnummer = ?,
        introductie = ?,
        hulpmiddelen = ?,
        contact_voorkeur = ?,
        onderzoektype_voorkeur = ?,
        heeft_voogd = ?,
        naam_voogd = ?,
        email_voogd = ?,
        telefoonnummer_voogd = ?,
        status = ?,
        voorwaarden_akkoord = ?
        WHERE gebruiker_id = ?;
        """
        
        return self.update(query,
                                email, hash_plain_text(wachtwoord) if huidig_wachtwoord != wachtwoord else wachtwoord, voornaam, tussenvoegsel, achternaam,
                                geboortedatum, geslacht, postcode, telefoonnummer, introductie,
                                hulpmiddelen, contact_voorkeur, onderzoektype_voorkeur, heeft_voogd, naam_voogd,
                                email_voogd, telefoonnummer_voogd, status, voorwaarden_akkoord, user_id)
    
    def update_user_status(self, user_id, data):
        status = data.get("status", "Nieuw")
        
        query = """
        UPDATE gebruikers
        SET 
        status = ?
        WHERE gebruiker_id = ?;
        """
        return self.update(query, status, user_id)
    
    def delete_user(self, user_id):
        query = """
        DELETE FROM gebruikers
        WHERE gebruiker_id = ?
        """
        return self.delete(query, user_id)

    def add_user_disabilities(self, user_id, beperkingen: list[int]):
        query = """
        INSERT INTO gebruiker_beperking
        (gebruiker_id,
        beperking_id)
        VALUES (?, ?)
        """
        gebruiker_beperkingen = [(user_id, beperking_id) for beperking_id in beperkingen]
        return self.insert_many(query, gebruiker_beperkingen)
    
    def remove_user_disabilities(self, user_id, beperkingen: list[int]):
        query = """
        DELETE FROM gebruiker_beperking
        WHERE gebruiker_id = ?
        AND beperking_id = ?;
        """
        oude_beperkingen = [(user_id, beperking_id) for beperking_id in beperkingen]
        return self.insert_many(query, oude_beperkingen)
    
    def update_user_disabilities(self, user_id, beperkingen: list[int]|list):
        huidige_beperkingen = self.get_user_disabilities_as_id(user_id)
        beperkingen = set(beperkingen)
        success = True
        
        nieuwe_beperkingen = [beperking for beperking in beperkingen if beperking not in huidige_beperkingen]
        oude_beperkingen = [beperking for beperking in huidige_beperkingen if beperking not in beperkingen]
        
        if nieuwe_beperkingen:
            if not self.add_user_disabilities(user_id, nieuwe_beperkingen):
                success = False
        
        if oude_beperkingen:
            if not self.remove_user_disabilities(user_id, oude_beperkingen):
                success = False
            
        return 1 if success else 0

    def get_user_disabilities_as_id(self, user_id) -> list[int]|list:
        query = """
        SELECT beperking_id
        FROM gebruiker_beperking
        WHERE gebruiker_id = ?
        """
        return [row["beperking_id"] for row in self.fetch_all(query, user_id)]
    
    def get_user_disabilities_as_name(self, user_id) -> list[str]|list:
        query = """
        SELECT b.beperking_naam
        FROM beperkingen AS b
        INNER JOIN gebruiker_beperking AS gb ON gb.beperking_id = b.beperking_id
        INNER JOIN gebruikers AS g ON g.gebruiker_id = gb.gebruiker_id
        WHERE g.gebruiker_id = ?
        """
        return [row["beperking_naam"] for row in self.fetch_all(query, user_id)]
    
    def get_current_password(self, user_id):
        query = """
        SELECT wachtwoord
        FROM gebruikers
        WHERE gebruiker_id = ?
        """
        return self.fetch_one(query, user_id)