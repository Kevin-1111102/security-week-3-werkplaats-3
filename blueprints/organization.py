from flask import Blueprint, render_template
from flask_jwt_extended import get_jwt


organization = Blueprint("organization",
                         __name__,
                         template_folder="../templates/organization")

@organization.route('/')
def dashboard():
    payload = get_jwt()
    role = payload.get("role")
    return render_template("organization/dashboard.html", role=role)

@organization.route("/nieuw-onderzoek-aanmaken")
def new_research():
    payload = get_jwt()
    role = payload.get("role")
    return render_template("organization/create_research.html", role=role)