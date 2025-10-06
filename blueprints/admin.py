from flask import Blueprint, render_template, request
from flask_jwt_extended import get_jwt

admin = Blueprint("admin",
                  __name__,
                  template_folder="../templates/admin")

@admin.route('/')
def dashboard():
    payload = get_jwt()
    role = payload.get("role")
    return render_template("admin/dashboard.html", role=role)

@admin.route("/user-detail")
def user_detail():
    payload = get_jwt()
    role = payload.get("role")
    user_id = request.args.get("id")
    if not user_id:
        return "Geen gebruiker ID opgegeven", 400
    return render_template("admin/users-details.html", role=role, user_id=user_id)

@admin.route("/research-detail")
def research_detail():
    payload = get_jwt()
    role = payload.get("role")
    research_id = request.args.get("id")
    if not research_id:
        return "Geen onderzoek ID opgegeven", 400
    return render_template("admin/onderzoek-details.html", role=role, research_id=research_id)


@admin.route("/organization-detail")
def organization_detail():
    payload = get_jwt()
    role = payload.get("role")
    organization_id = request.args.get("id")
    if not organization_id:
        return "Geen organisatie ID opgegeven", 400
    return render_template("admin/organisatie_details.html", role=role, organization_id=organization_id)

@admin.route("/subscription-detail")
def subscription_detail():
    payload = get_jwt()
    role = payload.get("role")
    
    research_id = request.args.get("onderzoek_id")
    user_id = request.args.get("gebruiker_id")
    return render_template("admin/subscription_details.html", role=role, research_id=research_id, user_id=user_id)