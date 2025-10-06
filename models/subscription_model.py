from models.model import Model

class SubscriptionModel(Model):

    def create_subscription(self, research_id, user_id):
        if self.subscription_exists(research_id, user_id):
            return "already_joined"

        query = """
        INSERT INTO gebruiker_onderzoek (onderzoek_id, gebruiker_id, status)
        VALUES (?, ?, 'Nieuw')
        """
        return self.insert_one(query, research_id, user_id)
    
    def delete_subscription(self, research_id, user_id):
        query = """
        DELETE FROM gebruiker_onderzoek
        WHERE onderzoek_id = ? AND gebruiker_id = ? 
        """
        return self.delete(query, research_id, user_id)

    def subscription_exists(self, research_id, user_id):
        query = """
        SELECT 1
        FROM gebruiker_onderzoek
        WHERE onderzoek_id = ? AND gebruiker_id = ?
        LIMIT 1
        """
        return self.fetch_one(query, research_id, user_id)
    
    def get_all_subscription(self, **kwargs):
        id = kwargs.get("id")
        role = kwargs.get("role")
        search_term = kwargs.get("search_term")
        sort_by = kwargs.get("sort_by")
        order = kwargs.get("order")
        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 10)
        args = []
        
        if role == "admin":
            query = """
            SELECT oz.titel AS onderzoek,
            oz.beperking_categorie AS onderzoeksbeperkingcategorie,
            g.voornaam || ' ' || COALESCE(g.tussenvoegsel || ' ', '') || g.achternaam AS ervaringsdeskundige,
            b.beperking_naam AS e_beperking,
            go.status AS status,
            oz.onderzoek_id AS onderzoek_id,
            g.gebruiker_id AS gebruiker_id
            FROM gebruiker_onderzoek AS go
            INNER JOIN onderzoeken AS oz ON oz.onderzoek_id = go.onderzoek_id
            INNER JOIN gebruikers AS g ON g.gebruiker_id = go.gebruiker_id
            INNER JOIN gebruiker_beperking AS gb ON gb.gebruiker_id = g.gebruiker_id
            INNER JOIN beperkingen AS b ON b.beperking_id = gb.beperking_id
            WHERE go.status = "Nieuw"
            """
            
            if search_term:
                query += """
                 AND (
                    LOWER(oz.titel) LIKE LOWER(?)
                    OR LOWER(oz.beperking) LIKE LOWER(?)
                    OR LOWER(ervaringsdeskundige) LIKE LOWER(?)
                    OR LOWER(go.status) LIKE LOWER(?)
                )
                """
                args.extend([f"%{search_term}%"] * 4)
                
            if sort_by:
                query += f" ORDER BY {sort_by} {order}"

            query += f"LIMIT {limit} OFFSET {offset}"

            if args:
                return self.fetch_all(query, *args)
            
            return self.fetch_all(query)
        
        if role == "ervaringsdeskundige":
            query = """
            SELECT DISTINCT oz.titel, oz.onderzoek_type, oz.begindatum, oz.einddatum, go.status AS status, oz.onderzoek_id   
            FROM onderzoeken AS oz
            INNER JOIN beperkingen AS bp ON bp.beperking_categorie = oz.beperking_categorie
            INNER JOIN gebruiker_beperking AS gbp ON gbp.beperking_id = bp.beperking_id
            INNER JOIN gebruikers AS g ON g.gebruiker_id = gbp.gebruiker_id
            INNER JOIN gebruiker_onderzoek AS go ON go.onderzoek_id = oz.onderzoek_id
            WHERE go.gebruiker_id = ?
            """
            args = [id]

            if search_term:
                query += """
                AND (
                    LOWER(oz.titel) LIKE LOWER(?)
                    OR LOWER(oz.onderzoek_type) LIKE LOWER(?)
                    OR LOWER(oz.begindatum) LIKE LOWER(?)
                    OR LOWER(oz.einddatum) LIKE LOWER(?)
                    OR LOWER(go.status) LIKE LOWER(?)
                )
                """
                args.extend([f"%{search_term}%"] * 5)

            if sort_by:
                query += f" ORDER BY {sort_by} {order}"

            query += f" LIMIT {limit} OFFSET {offset}"

            if args:
                return self.fetch_all(query, *args)
            
            return self.fetch_all(query)
        
    def get_all_subscription_count(self, **kwargs):
        id = kwargs.get("id")
        role = kwargs.get("role")
        search_term = kwargs.get("search_term")

        args = []

        if role == "admin":
            query = """
            SELECT COUNT(*) as total
            FROM gebruiker_onderzoek AS go
            INNER JOIN onderzoeken AS oz ON oz.onderzoek_id = go.onderzoek_id
            INNER JOIN gebruikers AS g ON g.gebruiker_id = go.gebruiker_id
            INNER JOIN gebruiker_beperking AS gb ON gb.gebruiker_id = g.gebruiker_id
            INNER JOIN beperkingen AS b ON b.beperking_id = gb.beperking_id
            WHERE go.status = "Nieuw"
            """

            if search_term:
                query += """
                AND (
                    LOWER(oz.titel) LIKE LOWER(?)
                    OR LOWER(oz.beperking) LIKE LOWER(?)
                    OR LOWER(ervaringsdeskundige) LIKE LOWER(?)
                    OR LOWER(go.status) LIKE LOWER(?)
                )
                """
                args = [f"%{search_term}%"] * 11

        if role == "ervaringsdeskundige":
            query = """
            SELECT DISTINCT COUNT(*) as total
            FROM onderzoeken AS oz
            INNER JOIN gebruiker_onderzoek AS go ON go.onderzoek_id = oz.onderzoek_id
            WHERE go.gebruiker_id = ?
            """
            args = [id]

            if search_term:
                query += """
                AND (
                    LOWER(oz.titel) LIKE LOWER(?)
                    OR LOWER(oz.onderzoek_type) LIKE LOWER(?)
                    OR LOWER(oz.begindatum) LIKE LOWER(?)
                    OR LOWER(oz.einddatum) LIKE LOWER(?)
                    OR LOWER(go.status) LIKE LOWER(?)
                )
                """
                args.extend([f"%{search_term}%"] * 5)

        result = self.fetch_one(query, *args)
        if result:
            return result['total']

    def get_subscription(self, research_id, user_id):
        query = """
        SELECT oz.*, g.*, go.status AS aanmelding_status
        FROM gebruiker_onderzoek AS go
        INNER JOIN onderzoeken AS oz ON oz.onderzoek_id = go.onderzoek_id
        INNER JOIN gebruikers AS g ON g.gebruiker_id = go.gebruiker_id
        WHERE go.onderzoek_id = ? AND go.gebruiker_id = ?
        """
        return self.fetch_one(query, research_id, user_id)
    
    def update_subscription_status(self, data):
        status = data.get("status", "Nieuw")
        research_id = data.get("onderzoek_id")
        user_id = data.get("gebruiker_id")
        
        query = """
        UPDATE gebruiker_onderzoek
        SET
        status = ?
        WHERE onderzoek_id = ?
        AND gebruiker_id = ?
        """
        return self.update(query, status, research_id, user_id)