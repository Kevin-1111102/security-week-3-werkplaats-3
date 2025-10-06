from flask import Blueprint, render_template, request, url_for, abort, make_response, jsonify, redirect
from werkzeug.exceptions import HTTPException
from flask_jwt_extended import create_access_token, set_access_cookies, unset_access_cookies, jwt_required
from constants import ROLES
from models.user_model import UserModel
from models.disability_model import DisabilityModel
from models.organization_model import OrganizationModel


authorization = Blueprint("authorization",
                          __name__,
                          template_folder="../templates/auth")

@authorization.route("/")
def redirect_to_login():
    return redirect(url_for("authorization.login"))

@authorization.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")
      
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    try:
        um = UserModel()
        user = um.check_user_login(email, password)
        if not user is None:
            if user["status"].lower() == "nieuw":
                abort(403, description="Uw registratie is nog niet goedgekeurd door een beheerder.")
            elif user["status"].lower() == "afgekeurd":
                abort(403, description="Uw registratie is afgekeurd door een beheerder.")
            else:
                user_id = user["gebruiker_id"]
                user_role = "admin" if user["beheerder"] else "ervaringsdeskundige"
                redirect = "/admin/" if user_role == "admin" else "/gebruiker/"
                    
                access_token = create_access_token(
                    identity=user_id,
                    additional_claims={"role": user_role}
                    )

                response = make_response({
                    "success": True,
                    "message": "Login succesvol",
                    "redirect": redirect,
                    "access_token": access_token
                    })
                set_access_cookies(response, access_token)
                return response, 200
            
        om = OrganizationModel()
        org = om.check_organization_login(email, password)
        if org is None:
            abort(401)
            
        if org["status"].lower() == "nieuw":
            abort(403, description="De registratie van uw organisatie is nog niet goedgekeurd door een beheerder.")
        elif org["status"].lower() == "afgekeurd":
            abort(403, description="De registratie van uw organisatie is afgekeurd door een beheerder.")
        else:
            org_id = org["organisatie_id"]
            access_token = create_access_token(
                identity=org_id,
                additional_claims={"role": "organisatie"}
                )
            
            response = make_response({
                "success": True,
                "message": "Login succesvol",
                "redirect": "/organisatie/",
                "access_token": access_token
            })
            
            set_access_cookies(response, access_token)
            return response, 200
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        abort(500) 
        
@authorization.route("/logout")
@jwt_required()
def logout():
    response = jsonify({
        "success": True,
        "message": "U bent succesvol uitgelogd",
        "redirect": url_for("authorization.login")
    })
    
    unset_access_cookies(response)
    return response, 200 
  
@authorization.route('/registreren')
def register_user_route():
    dm = DisabilityModel()
    disabilities = dm.get_disabilities()
    return render_template("auth/register.html", beperkingen=disabilities)

@authorization.route('/voorwaarden')
def terms_and_conditions():
    return render_template("auth/tos.html")