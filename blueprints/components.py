from flask import Blueprint, url_for, abort, jsonify
from werkzeug.exceptions import HTTPException
from flask_jwt_extended import get_jwt

components = Blueprint("components",
                          __name__,
                          template_folder="../templates/components")

@components.route("/navbar")
def navbar():
    try:
        payload = get_jwt()
        role = payload.get("role")
        if payload.get("role"):
            role = payload.get("role")
            nav_selection = {
                "ervaringsdeskundige": [
                    ("Dashboard", url_for("user.dashboard")),
                    ("Profiel", url_for("user.profile")),
                    ("Logout", None)
                ],
                "organisatie": [
                    ("Dashboard", url_for("organization.dashboard")),
                    ("Logout", None)
                ],
                "admin": [
                    ("Dashboard", url_for("admin.dashboard")),
                    ("Logout", None)
                ]
            }
            return jsonify(nav_selection.get(role)), 200
        else:   
            abort(404)     
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        abort(500) 