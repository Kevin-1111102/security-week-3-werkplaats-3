from models.model import Model

class DisabilityModel(Model):
    
    def get_disabilities(self):
        query = """
        SELECT beperking_id, beperking_naam, beperking_categorie 
        FROM beperkingen
        """
        return self.fetch_all(query)
    
    def get_disability_categories(self):
        query = """
        SELECT DISTINCT beperking_categorie 
        FROM beperkingen
        """
        return self.fetch_all(query)