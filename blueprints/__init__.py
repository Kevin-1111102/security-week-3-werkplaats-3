from blueprints.api.api_organization import api_organization
from blueprints.api.api_research import api_research
from blueprints.api.api_user import api_user
from blueprints.api.api_disability import api_disability
from blueprints.api.api_subscription import api_subscription

from blueprints.admin import admin
from blueprints.organization import organization
from blueprints.user import user
from blueprints.research import research

from blueprints.components import components
from blueprints.auth import authorization

def register_blueprints(app):
    app.register_blueprint(api_organization, url_prefix="/api/organizations")
    app.register_blueprint(api_research, url_prefix="/api/researches")
    app.register_blueprint(api_user, url_prefix="/api/users")
    app.register_blueprint(api_disability, url_prefix="/api/disabilities")
    app.register_blueprint(api_subscription, url_prefix="/api/subscriptions")
    
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(organization, url_prefix="/organisatie")
    app.register_blueprint(user, url_prefix="/gebruiker")
    app.register_blueprint(research, url_prefix="/onderzoek")
    
    app.register_blueprint(components, url_prefix="/components")
    app.register_blueprint(authorization)