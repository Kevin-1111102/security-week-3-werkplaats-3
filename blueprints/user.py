from flask import Blueprint, render_template
from flask_jwt_extended import get_jwt_identity, get_jwt
from models.disability_model import DisabilityModel


user = Blueprint("user",
                 __name__,
                 template_folder="../templates/user")

@user.route('/')
def dashboard():
    payload = get_jwt()
    role = payload.get("role")
    return render_template("user/dashboard.html", role=role)

@user.route('/profiel')
def profile():
    user_id = get_jwt_identity()
    payload = get_jwt()
    role = payload.get("role")
    return render_template("user/profile.html", role=role, user_id=user_id)

@user.route('/profiel/bewerken')
def update_profile():
    user_id = get_jwt_identity()
    payload = get_jwt()
    role = payload.get("role")
    
    dm = DisabilityModel()
    disabilities = dm.get_disabilities()
    return render_template("user/update_profile.html", role=role, user_id=user_id, beperkingen=disabilities)
