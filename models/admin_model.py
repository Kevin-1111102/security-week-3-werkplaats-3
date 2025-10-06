from models.model import Model

class AdminModel(Model):
    
    def log_action(self, admin_id, actie):
        query = """
        INSERT INTO admin_logs (admin_id, actie)
        VALUES (?, ?)
        """
        return self.insert_one(query, admin_id, actie)