from models.model import Model
from utils import hash_plain_text, verify_plain_text


class OrganizationModel(Model):

    def check_organization_login(self, email, password):
        query = """
        SELECT *
        FROM organisaties
        WHERE email = ?;
        """
        
        result = self.fetch_one(query, email)
        if result:
            if verify_plain_text(password, result["wachtwoord"]):
                return result
        return None

    def get_all_organization(self, search_term, sort_by, order):
        args = []
        
        query = """
        SELECT *
        FROM organisaties
        WHERE status = 'Nieuw'
        """
        
        if search_term:
            query += """
            AND (
                LOWER(organisatie_naam) LIKE LOWER(?)
                OR LOWER(contactpersoon) LIKE LOWER(?)
                OR LOWER(email) LIKE LOWER(?)
                OR LOWER(status) LIKE LOWER(?)
            )
            """
            args.extend([f"%{search_term}%"] * 4)

        if sort_by:
            query += f"ORDER BY {sort_by} {order}"
                
        if args:
            return self.fetch_all(query, *args)
            
        return self.fetch_all(query)
       
    def get_organization(self, organization_id):
        query = """
        SELECT *
        FROM organisaties
        WHERE organisatie_id = ?;
        """
        return self.fetch_one(query, organization_id)
     
    def create_organization(self, data):
        name = data.get("name")
        type = data.get("type")
        website = data.get("website")
        description = data.get("description")
        contact = data.get("contact")
        email = data.get("email")
        password = data.get("password")
        number = data.get("number")
        details = data.get("details")
        status = "Nieuw"

        query = """
        INSERT INTO organisaties 
        (organisatie_naam, 
        organisatie_type, 
        website, 
        beschrijving, 
        contactpersoon, 
        email, 
        wachtwoord, 
        telefoonnummer, 
        overige_details, 
        status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        return self.insert_one(query, 
                               name, type, website, description, contact, 
                               email, hash_plain_text(password), number, details, status)

    def update_organization(self, organization_id, data):
        name = data.get("name")
        type = data.get("type")
        website = data.get("website")
        description = data.get("description")
        contact = data.get("contact")
        email = data.get("email")
        current_password = self.get_current_password(organization_id)["wachtwoord"]
        password = data.get("password") or current_password
        number = data.get("number")
        details = data.get("details")
        status = "Goedgekeurd"

        query = """
        UPDATE organisaties
        SET 
        organisatie_naam = ?,
        organisatie_type = ?, 
        website = ?, 
        beschrijving = ?, 
        contactpersoon = ?, 
        email = ?, 
        wachtwoord = ?, 
        telefoonnummer = ?,
        overige_details = ?,
        status = ?
        WHERE organisatie_id = ?;
        """
        return self.update(query, 
                           name, type, website, description, contact, 
                           email, hash_plain_text(password) if current_password != password else password, number, details, status, organization_id)

    def update_organization_status(self, organization_id, data):
        status = data.get("status", "Nieuw")
        
        query = """
        UPDATE organisaties
        SET 
        status = ?
        WHERE organisatie_id = ?;
        """
        return self.update(query, status, organization_id)
        
        
    def delete_organization(self, organization_id):
        query = """
        DELETE FROM organisaties
        WHERE organisatie_id = ?;
        """
        return self.delete(query, organization_id)
    
    def get_current_password(self, organization_id):
        query = """
        SELECT wachtwoord
        FROM organisaties
        WHERE organisatie_id = ?
        """
        return self.fetch_one(query, organization_id)