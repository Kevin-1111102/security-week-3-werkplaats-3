from flask import Blueprint, abort, request
from werkzeug.exceptions import HTTPException
from flask_jwt_extended import get_jwt, get_jwt_identity
from utils import send_email
from models.research_model import ResearchModel
from models.admin_model import AdminModel

api_research = Blueprint('api_research', __name__)


@api_research.route("/", methods=["GET"])
def get_all_research():
    id = get_jwt_identity()
    payload = get_jwt()
    role = payload.get("role")

    search_term = request.args.get("zoekterm")
    sort_by = request.args.get("sorteer_op")
    order = request.args.get("volgorde", "ASC")

    page = request.args.get("pagina", "1")
    try:
        page = int(page)
    except ValueError:
        page = 1

    records = request.args.get("aantal", "10")
    try:
        records = int(records)
    except ValueError:
        records = 10

    offset = (page - 1) * records

    try:
        rm = ResearchModel()
        result = rm.get_all_research(id=id,
                                     role=role,
                                     search_term=search_term,
                                     sort_by=sort_by,
                                     order=order,
                                     offset=offset,
                                     limit=records)

        total_records = rm.get_all_research_count(id=id,
                                                  role=role,
                                                  search_term=search_term)

        total_pages = (total_records // records) + (1 if total_records % records > 0 else 0)

        if result:
            return {
                "success": True,
                "data": result,
                "message": "Onderzoeken gevonden",
                "total_records": total_records,
                "current_page": page,
                "total_pages": total_pages
            }, 200
        return {
            "success": False,
            "message": "Onderzoeken niet gevonden"
        }, 200
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        abort(500)


@api_research.route("/<research_id>", methods=["GET"])
def get_research(research_id):
    id = get_jwt_identity()
    payload = get_jwt()
    role = payload.get("role")

    try:
        rm = ResearchModel()
        result = rm.get_research(research_id, id, role)
        if result:
            result["beperkingen"] = rm.get_research_disabilities(research_id)
            if role == "organisatie":
                result["participants"] = rm.get_research_participants(research_id)
            return {
                "success": True,
                "data": result,
                "message": "Onderzoek gevonden"
            }, 200
        abort(404, description="Onderzoek niet gevonden")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        abort(500)


@api_research.route("/", methods=["POST"])
def create_research():
    id = get_jwt_identity()
    payload = get_jwt()
    role = payload.get("role")

    data = request.get_json()

    if role != "organisatie":
        abort(403, description="U kunt geen onderzoeken aanmaken")

    try:
        rm = ResearchModel()
        last_row_id = rm.create_research(data=data, id=id)
        if last_row_id:
            return {
                "success": True,
                "data": last_row_id,
                "message": "Onderzoek aangemaakt"
            }, 201
        abort(500, description="Er ging iets mis tijdens het verwerken van uw verzoek.")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        abort(500)


@api_research.route("/<research_id>", methods=["PATCH"])
def update_research(research_id):
    id = get_jwt_identity()
    payload = get_jwt()
    role = payload.get("role")

    data = request.get_json()

    if role == "ervaringsdeskundige":
        abort(401, description="U kunt geen onderzoeken wijzigen")

    try:
        rm = ResearchModel()
        rowcount = 0
        if role == "admin":
            rowcount = rm.update_research_status(data, research_id)
        else:
            rowcount = rm.update_research(data, research_id, id)
        if rowcount:
            if role == "admin":
                data_rs_org = rm.get_research_organisation(research_id)
                titel = data_rs_org.get("titel")
                email = data_rs_org.get("email")

                status = data.get("status", "Nieuw")
                am = AdminModel()
                action = f"Onderzoek: {titel} is {status}"
                am.log_action(id, action)
                
                status_messages = {
                    "Goedgekeurd": f"Uw onderzoek \"{titel}\" is goedgekeurd en zichtbaar voor ervaringsdeskundigen.",
                    "Afgekeurd": f"Uw onderzoek \"{titel}\" is afgekeurd en niet zichtbaar voor ervaringsdeskundigen.",
                    "Nieuw": f"Uw onderzoek \"{titel}\" is nog in behandeling, u krijgt binnenkort een e-mail van ons."
                }
                send_email(
                    f"{email}",
                    f"Onderzoek status: {status}",
                    f"{status_messages[status]}"
                )
            return {
                "success": True,
                "message": "Wijzigingen voor dit onderzoek zijn opgeslagen"
            }, 200
        abort(500, description="Er ging iets mis tijdens het verwerken van uw verzoek.")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        abort(500)


@api_research.route("/<research_id>", methods=["DELETE"])
def delete_research(research_id):
    id = get_jwt_identity()
    payload = get_jwt()
    role = payload.get("role")

    if role != "organisatie":
        abort(401, description="U kunt geen onderzoeken verwijderen")

    try:
        rm = ResearchModel()
        response = rm.delete_research(research_id, id)
        if response:
            return {
                "success": True,
                "message": "Onderzoek verwijderd"
            }, 200
        abort(500, description="Er ging iets mis tijdens het verwerken van uw verzoek.")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        abort(500)