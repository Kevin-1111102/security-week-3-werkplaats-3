from models.model import Model


class ResearchModel(Model):
        
    def get_all_research(self, **kwargs):
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
            SELECT *
            FROM onderzoeken
            WHERE status = 'Nieuw'
            """
            
            if search_term:
                query += """
                 AND (
                    LOWER(titel) LIKE LOWER(?)
                    OR LOWER(status) LIKE LOWER(?)
                    OR LOWER(onderzoek_type) LIKE LOWER(?)
                )
                """
                args.extend([f"%{search_term}%"] * 3)
                
            if sort_by:
                query += f" ORDER BY {sort_by} {order}"

            query += f" LIMIT {limit} OFFSET {offset}"

            if args:
                return self.fetch_all(query, *args)
            
            return self.fetch_all(query)
        
        if role == "organisatie":
            query = """
            SELECT oz.*
            FROM onderzoeken AS oz
            INNER JOIN organisaties AS org ON org.organisatie_id = oz.organisatie_id
            WHERE org.organisatie_id = ?
            """

            args = [id]
            if search_term:
                query += """
                 AND (
                    LOWER(oz.titel) LIKE LOWER(?)
                    OR LOWER(oz.status) LIKE LOWER(?)
                    OR LOWER(oz.begindatum) LIKE LOWER(?)
                    OR LOWER(oz.einddatum) LIKE LOWER(?)
                    OR LOWER(oz.onderzoek_type) LIKE LOWER(?)
                )
                """
                args.extend([f"%{search_term}%"] * 5)

            if sort_by:
                query += f" ORDER BY {sort_by} {order}"

            query += f" LIMIT {limit} OFFSET {offset}"

            return self.fetch_all(query, *args)

        if role == "ervaringsdeskundige":
            query = """
            SELECT DISTINCT oz.*
            FROM onderzoeken AS oz
            INNER JOIN beperkingen AS bp ON bp.beperking_categorie = oz.beperking_categorie
            INNER JOIN gebruiker_beperking AS gbp ON gbp.beperking_id = bp.beperking_id
            INNER JOIN gebruikers AS g ON g.gebruiker_id = gbp.gebruiker_id
            LEFT JOIN gebruiker_onderzoek AS go ON go.onderzoek_id = oz.onderzoek_id AND go.gebruiker_id = ?
            WHERE g.gebruiker_id = ?
            AND go.onderzoek_id IS NULL
            AND oz.status = 'Goedgekeurd'
            AND oz.beschikbaar = 1
            AND (JULIANDAY('now') - JULIANDAY(g.geboortedatum)) / 365.25 BETWEEN oz.leeftijd_doelgroep_van AND oz.leeftijd_doelgroep_tot
            AND einddatum > DATE('now')
            """
            args = [id, id]

            if search_term:
                query += """
                 AND (
                    LOWER(oz.titel) LIKE LOWER(?)
                    OR LOWER(oz.begindatum) LIKE LOWER(?)
                    OR LOWER(oz.einddatum) LIKE LOWER(?)
                    OR LOWER(oz.onderzoek_type) LIKE LOWER(?)
                    OR LOWER(oz.beloning) LIKE LOWER(?)
                )
                """
                args.extend([f"%{search_term}%"] * 5)

            if sort_by:
                query += f" ORDER BY {sort_by} {order}"

            query += f" LIMIT {limit} OFFSET {offset}"

            return self.fetch_all(query, *args)

    def get_all_research_count(self, **kwargs):
        id = kwargs.get("id")
        role = kwargs.get("role")
        search_term = kwargs.get("search_term")

        query = None
        args = []

        if role == "admin":
            query = """
            SELECT COUNT(*) as total
            FROM onderzoeken
            WHERE status = 'Nieuw'
            """

            if search_term:
                query += """
                 AND (
                    LOWER(titel) LIKE LOWER(?)
                    OR LOWER(status) LIKE LOWER(?)
                    OR LOWER(onderzoek_type) LIKE LOWER(?)
                )
                """
                args = [f"%{search_term}%"] * 3

        elif role == "organisatie":
            query = """
            SELECT COUNT(*) as total
            FROM onderzoeken AS oz
            INNER JOIN organisaties AS org ON org.organisatie_id = oz.organisatie_id
            WHERE org.organisatie_id = ?
            """
            args = [id]

            if search_term:
                query += """
                 AND (
                    LOWER(oz.titel) LIKE LOWER(?)
                    OR LOWER(oz.status) LIKE LOWER(?)
                    OR LOWER(oz.begindatum) LIKE LOWER(?)
                    OR LOWER(oz.einddatum) LIKE LOWER(?)
                    OR LOWER(oz.onderzoek_type) LIKE LOWER(?)
                )
                """
                args.extend([f"%{search_term}%"] * 5)

        elif role == "ervaringsdeskundige":
            query = """
            SELECT COUNT(DISTINCT oz.onderzoek_id) as total
            FROM onderzoeken AS oz
            INNER JOIN beperkingen AS bp ON bp.beperking_categorie = oz.beperking_categorie
            INNER JOIN gebruiker_beperking AS gbp ON gbp.beperking_id = bp.beperking_id
            INNER JOIN gebruikers AS g ON g.gebruiker_id = gbp.gebruiker_id
            LEFT JOIN gebruiker_onderzoek AS go ON go.onderzoek_id = oz.onderzoek_id AND go.gebruiker_id = ?
            WHERE g.gebruiker_id = ?
            AND go.onderzoek_id IS NULL
            AND oz.status = 'Goedgekeurd'
            AND oz.beschikbaar = 1
            AND (JULIANDAY('now') - JULIANDAY(g.geboortedatum)) / 365.25 BETWEEN oz.leeftijd_doelgroep_van AND oz.leeftijd_doelgroep_tot
            AND einddatum > DATE('now')
            """
            args = [id, id]
                
            if search_term:
                query += """
                 AND (
                    LOWER(oz.titel) LIKE LOWER(?)
                    OR LOWER(oz.begindatum) LIKE LOWER(?)
                    OR LOWER(oz.einddatum) LIKE LOWER(?)
                    OR LOWER(oz.onderzoek_type) LIKE LOWER(?)
                    OR LOWER(oz.beloning) LIKE LOWER(?)
                )
                """
                args.extend([f"%{search_term}%"] * 5)

        if query:
            result = self.fetch_one(query, *args)
            if result:
                return result['total']
        return 0

    def get_research(self, research_id, id, role):
        if role == "admin":
            query = """
            SELECT *
            FROM onderzoeken
            WHERE onderzoek_id = ?;
            """
            return self.fetch_one(query, research_id)
        
        if role == "organisatie":
            query = """
            SELECT oz.*
            FROM onderzoeken AS oz
            INNER JOIN organisaties AS org ON org.organisatie_id = oz.organisatie_id
            WHERE oz.onderzoek_id = ?
            AND org.organisatie_id = ?;
            """
            return self.fetch_one(query, research_id, id)
                    
        if role == "ervaringsdeskundige":
            query = """
            SELECT oz.*
            FROM onderzoeken AS oz
            INNER JOIN beperkingen AS bp ON bp.beperking_categorie = oz.beperking_categorie
            INNER JOIN gebruiker_beperking AS gbp ON gbp.beperking_id = bp.beperking_id
            INNER JOIN gebruikers AS g ON g.gebruiker_id = gbp.gebruiker_id
            WHERE g.gebruiker_id = ?
            AND oz.status = 'Goedgekeurd'
            AND oz.beschikbaar = 1
            AND (JULIANDAY('now') - JULIANDAY(g.geboortedatum)) / 365.25 BETWEEN oz.leeftijd_doelgroep_van AND oz.leeftijd_doelgroep_tot
            AND einddatum > DATE('now')
            AND oz.onderzoek_id = ?;
            """
            return self.fetch_one(query, id, research_id)
        
    def get_research_participants(self, research_id):
        query = """
        SELECT DISTINCT g.voornaam || ' ' || COALESCE(g.tussenvoegsel || ' ', '') || g.achternaam AS ervaringsdeskundige
        FROM onderzoeken AS oz
        INNER JOIN gebruiker_onderzoek AS go ON go.onderzoek_id = oz.onderzoek_id
        INNER JOIN gebruikers AS g ON g.gebruiker_id = go.gebruiker_id
        WHERE oz.onderzoek_id = ?
        AND go.status = "Goedgekeurd";
        """
        return self.fetch_all(query, research_id)
        
    def get_research_disabilities(self, research_id):
        query = """
        SELECT bp.beperking_naam
        FROM onderzoeken AS oz
        INNER JOIN beperkingen AS bp ON bp.beperking_categorie = oz.beperking_categorie
        WHERE oz.onderzoek_id = ?;
        """
        return self.fetch_all(query, research_id)
    
    def create_research(self, **kwargs):
        data = kwargs.get('data', {})
        id = kwargs.get('id')
        title = data.get('title')
        available = data.get('available', 0)
        description = data.get('description')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        research_type = data.get('research_type')
        location = data.get('location')
        reward = data.get('reward', "")
        with_reward = 1 if reward else 0
        age_group_from = data.get('age_min')
        age_group_to = data.get('age_max')
        disability_category = data.get('disability-category')
        status = "Nieuw"

        query = """
        INSERT INTO onderzoeken
        (titel, 
        status, 
        beschikbaar, 
        beschrijving, 
        begindatum, 
        einddatum, 
        onderzoek_type, 
        locatie, 
        met_beloning, 
        beloning, 
        leeftijd_doelgroep_van, 
        leeftijd_doelgroep_tot, 
        beperking_categorie, 
        organisatie_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        return self.insert_one(query,
                                title, status, available, description, start_date,
                                end_date, research_type, location, with_reward,
                                reward, age_group_from, age_group_to, disability_category, id)

    def update_research(self, data, research_id, id):
        title = data.get('title')
        current_status = self.get_current_research_status(research_id)["status"]
        status = "Gesloten" if data.get("status") == "Gesloten" else current_status
        available = data.get('available', 0)
        description = data.get('description')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        with_reward = data.get('with_reward')
        reward = data.get('reward')

        query = """
        UPDATE onderzoeken
        SET
        titel = ?, 
        status = ?,
        beschikbaar = ?,
        beschrijving = ?, 
        begindatum = ?, 
        einddatum = ?,
        met_beloning = ?, 
        beloning = ?
        WHERE onderzoek_id = ?
        AND organisatie_id = ?;
        """
        return self.update(query,
                           title, status, available, description, start_date, end_date,
                           with_reward, reward, research_id, id)
    
    def get_current_research_status(self, research_id):
        query = """
        SELECT status
        FROM onderzoeken
        WHERE onderzoek_id = ?;
        """
        return self.fetch_one(query, research_id)

    def get_research_organisation(self, research_id):
        query = """
        SELECT org.email, oz.titel
        FROM onderzoeken AS oz
        INNER JOIN organisaties AS org ON org.organisatie_id = oz.organisatie_id
        WHERE oz.onderzoek_id = ?;
        """
        return self.fetch_one(query, research_id)

    def update_research_status(self, data, research_id):
        status = data.get("status", "Nieuw")
        
        query = """
        UPDATE onderzoeken
        SET 
        status = ?
        WHERE onderzoek_id = ?;
        """
        return self.update(query, status, research_id)
    
    def delete_research(self, research_id, id):
        query = """
        DELETE FROM onderzoeken 
        WHERE onderzoek_id = ?
        AND organisatie_id = ?;
        """
        return self.delete(query, research_id, id)