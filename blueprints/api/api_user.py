from flask import Blueprint, abort, request, url_for, jsonify
from werkzeug.exceptions import HTTPException
from flask_jwt_extended import get_jwt, get_jwt_identity, unset_access_cookies
from utils import send_email
from models.user_model import UserModel
from models.admin_model import AdminModel

api_user = Blueprint("api_user", __name__)


@api_user.route("/", methods=["GET"])
def get_all_user():
    payload = get_jwt()
    role = payload.get("role")

    if role != "admin":
        abort(401, description="U kunt geen overzicht krijgen van alle gebruikers")

    search_term = request.args.get("zoekterm")
    sort_by = request.args.get("sorteer_op")
    order = request.args.get("volgorde", "ASC")

    page = request.args.get("pagina", "1")
    records = request.args.get("aantal", "10")

    try:
        page = int(page)
        records = int(records)
    except ValueError:
        page, records = 1, 10

    try:
        um = UserModel()
        all_results = um.get_all_user(search_term=search_term, sort_by=sort_by, order=order)

        # **Paginatie toepassen binnen Python**
        total_records = len(all_results)
        total_pages = (total_records // records) + (1 if total_records % records > 0 else 0)

        # Bepalen welke records op de huidige pagina worden weergegeven
        start = (page - 1) * records
        end = start + records
        paginated_results = all_results[start:end]

        if paginated_results:
            return {
                "success": True,
                "data": paginated_results,
                "message": "Gebruikers gevonden",
                "total_records": total_records,
                "current_page": page,
                "total_pages": total_pages
            }, 200
        return {
            "success": False,
            "message": "Gebruikers niet gevonden"
        }, 200
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        abort(500)


@api_user.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    id = get_jwt_identity()
    payload = get_jwt()
    role = payload.get("role")

    if role == "ervaringsdeskundige" and id != int(user_id):
        abort(401, description="U kunt geen gegevens van een andere gebruiker ophalen.")

    if role == "organisatie":
        abort(401, description="U kunt geen gegevens van een gebruiker ophalen.")

    try:
        um = UserModel()
        result = um.get_user(user_id)
        if result:
            disabilities = um.get_user_disabilities_as_name(user_id)
            result["beperkingen"] = disabilities
            return {
                "success": True,
                "data": result,
                "message": "Gebruiker gevonden"
            }, 200
        abort(404, description="Gebruiker niet gevonden")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        abort(500)


@api_user.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data.get("voorwaarden_akkoord"):
        abort(500, description="Registratie mislukt")

    beperkingen = data.get("beperkingen", [])
    try:
        um = UserModel()
        user_id = um.create_user(data)
        if user_id:
            if beperkingen:
                um.add_user_disabilities(user_id, beperkingen)
            send_email(
                data.get("email"),
                "Registratie succesvol",
                "Uw registratie is succesvol verwerkt, u krijgt binnenkort te horen of u bent goedgekeurd om in te kunnen loggen."
            )
            return {
                "success": True,
                "message": "Registratie succesvol",
                "redirect": url_for("authorization.login")
            }, 201
        abort(500, description="Registratie mislukt")
    except HTTPException as e:
        raise e
    except Exception as e:
        abort(500, description=f"Registratie mislukt, ${e}")


@api_user.route("/<user_id>", methods=["PUT", "PATCH"])
def update_user(user_id):
    id = get_jwt_identity()
    payload = get_jwt()
    role = payload.get("role")

    if role == "ervaringsdeskundige" and id != int(user_id):
        abort(403, description="U kunt de gegevens van andere gebruikers niet wijzigen :)")
    elif role == "organisatie":
        abort(403, description="U kunt de gegevens van een ervaringsdeskundige niet wijzigen")

    data = request.get_json()
    beperkingen = data.get("beperkingen")
    try:
        um = UserModel()
        rowcount = 0
        if role == "admin":
            rowcount = um.update_user_status(user_id, data)
            if rowcount:
                result = um.get_user(user_id)
                
                status = data.get("status", "Nieuw")
                am = AdminModel()
                user_full_name = " ".join(word for word in [result.get("voornaam", ""), result.get("tussenvoegsel", ""), result.get("achternaam", "")] if word)
                action = f"Gebruiker: {user_full_name} is {status}"
                am.log_action(id, action)
                
                status_messages = {
                    "Goedgekeurd": "Uw account is goedgekeurd, u kunt nu inloggen. <a href='http://127.0.0.1:5000/login'>Klik hier om in te loggen</a>",
                    "Afgekeurd": "Uw account is helaas afgekeurd, neem contact met ons op voor meer informatie.",
                    "Nieuw": "Uw account is nog in behandeling, u krijgt binnenkort een e-mail van ons."
                }
                if result:
                    send_email(
                        result["email"],
                        f"Account status: {status}",
                        f"{status_messages[status]}"
                    )
                return {
                    "success": True,
                    "message": "Wijzigingen zijn succesvol opgeslagen"
                }, 200
        else:
            rowcount = um.update_user(user_id, data)
        if rowcount:
            resp = um.update_user_disabilities(user_id, beperkingen)
            if resp:
                return {
                    "success": True,
                    "message": "Wijzigingen zijn succesvol opgeslagen",
                    "redirect": url_for("user.profile")
                }, 200
        abort(500, description="Iets ging mis tijdens het wijzigen van uw gegevens")
    except HTTPException as e:
        raise e
    except Exception as e:
        abort(500, description=f"Iets ging mis tijdens het wijzigen van uw gegevens, ${e}")


@api_user.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    id = get_jwt_identity()
    payload = get_jwt()
    role = payload.get("role")

    if role != "ervaringsdeskundige":
        abort(403, description="U kunt geen gebruikers verwijderen")

    if id != int(user_id):
        abort(403, description="U kunt geen andere gebruikers verwijderen :)")

    try:
        rm = UserModel()
        rowcount = rm.delete_user(user_id)
        if rowcount:
            response =  jsonify({
                "success": True,
                "message": "Uw gegevens zijn verwijderd",
                "redirect": url_for("authorization.login")
            })
            
            unset_access_cookies(response)
            return response, 200
        abort(500, description="Er ging iets mis tijdens het verwerken van uw verzoek.")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        abort(500)
