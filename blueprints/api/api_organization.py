from flask import Blueprint, request, abort
from werkzeug.exceptions import HTTPException
from flask_jwt_extended import get_jwt, get_jwt_identity
from utils import send_email
from models.organization_model import OrganizationModel
from models.admin_model import AdminModel

api_organization = Blueprint("api_organization", __name__)


@api_organization.route("/", methods=["GET"])
def get_all_organization():
    payload = get_jwt()
    role = payload.get("role")

    if role != "admin":
        abort(403, description="U kunt geen overzicht krijgen van alle organisaties")

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
        om = OrganizationModel()
        all_results = om.get_all_organization(search_term=search_term, sort_by=sort_by, order=order)

        total_records = len(all_results)
        total_pages = (total_records // records) + (1 if total_records % records > 0 else 0)

    
        start = (page - 1) * records
        end = start + records
        paginated_results = all_results[start:end]

        if paginated_results:
            return {
                "success": True,
                "data": paginated_results,
                "message": "Organisaties gevonden",
                "total_records": total_records,
                "current_page": page,
                "total_pages": total_pages
            }, 200
        return {
            "success": False,
            "message": "Organisaties niet gevonden"
        }, 200
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        abort(500)


@api_organization.route("/<organization_id>", methods=["GET"])
def get_organization(organization_id):
    id = get_jwt_identity()
    payload = get_jwt()
    role = payload.get("role")

    if role != "organisatie" and role != "admin":
        abort(401, description="U kunt geen gegevens van deze organisatie ophalen.")

    if role == "organisatie" and id != int(organization_id):
        abort(401, description="U kunt geen gegevens van deze organisatie ophalen.")

    try:
        om = OrganizationModel()
        result = om.get_organization(organization_id)
        if result:
            return {
                "success": True,
                "data": result,
                "message": "Organisatie gevonden"
            }, 200
        abort(500, description="Er ging iets mis tijdens het verwerken van uw verzoek.")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        abort(500)


@api_organization.route("/", methods=["POST"])
def create_organization():
    data = request.get_json()

    try:
        om = OrganizationModel()
        last_row_id = om.create_organization(data)
        if last_row_id:
            return {
                "success": True,
                "data": last_row_id,
                "message": "Organisatie succesvol geregistreerd"
            }, 201
        abort(500, description="Er ging iets mis tijdens het verwerken van uw verzoek.")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        abort(500)


@api_organization.route("/<organization_id>", methods=["PUT", "PATCH"])
def update_organization(organization_id):
    id = get_jwt_identity()
    payload = get_jwt()
    role = payload.get("role")

    data = request.get_json()

    if role == "organisatie" and id != int(organization_id):
        abort(401, description="U kunt geen andere organisaties wijzigen :)")
    elif role == "ervaringsdeskundige":
        abort(401, description="U kunt geen organisatie wijzigen")

    try:
        om = OrganizationModel()
        rowcount = 0
        if role == "admin":
            rowcount = om.update_organization_status(organization_id, data)
        else:
            rowcount = om.update_organization(organization_id, data)
        if rowcount:
            if role == "admin":
                result = om.get_organization(organization_id)
                email = result.get("email")
                org_naam = result.get("organisatie_naam")
                
                status = data.get("status", "Nieuw")
                am = AdminModel()
                action = f"Organisatie: {org_naam} is {status}"
                am.log_action(id, action)
                
                status_messages = {
                    "Goedgekeurd": "Uw account is goedgekeurd, u kunt nu inloggen. <a href='http://127.0.0.1:5000/login'>Klik hier om in te loggen</a>",
                    "Afgekeurd": "Uw account is helaas afgekeurd, neem contact met ons op voor meer informatie.",
                    "Nieuw": "Uw account is nog in behandeling, u krijgt binnenkort een e-mail van ons."
                }
                send_email(
                    f"{email}",
                    f"Account status: {status}",
                    f"{status_messages[status]}"
                )
            return {
                "success": True,
                "message": "Wijzigingen voor uw organisatie zijn opgeslagen"
            }, 200
        abort(500, description="Er ging iets mis tijdens het verwerken van uw verzoek.")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        abort(500)


@api_organization.route("/<organization_id>", methods=["DELETE"])
def delete_organization(organization_id):
    id = get_jwt_identity()
    payload = get_jwt()
    role = payload.get("role")

    if role != "organisatie":
        abort(401, description="U kunt geen organisaties verwijderen")

    if id != int(organization_id):
        abort(401, description="U kunt geen andere organisaties verwijderen :)")

    try:
        om = OrganizationModel()
        rowcount = om.delete_organization(organization_id)
        if rowcount:
            return {
                "success": True,
                "message": "Organisatie verwijderd"
            }, 200
        abort(500, description="Er ging iets mis tijdens het verwerken van uw verzoek.")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        abort(500)
