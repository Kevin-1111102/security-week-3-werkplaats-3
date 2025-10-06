from flask import Blueprint, abort, request
from werkzeug.exceptions import HTTPException
from flask_jwt_extended import get_jwt, get_jwt_identity
from utils import send_email
from models.subscription_model import SubscriptionModel
from models.admin_model import AdminModel
from models.user_model import UserModel
from models.research_model import ResearchModel


api_subscription = Blueprint('api_subscription', __name__)

@api_subscription.route("/", methods=["GET"])
def get_all_subscription():
    id = get_jwt_identity()
    payload = get_jwt()
    role = payload.get("role")
    
    if role == "organisatie":
        abort(403, description="U kunt geen aanmeldingen inzien")
        
    search_term = request.args.get("zoekterm")
    sort_by = request.args.get("sorteer_op")
    order = request.args.get("volgorde", "ASC")

    page = int(request.args.get("pagina", 1))
    records = int(request.args.get("aantal", 10))
    offset = (page - 1) * records

    try:
        sbm = SubscriptionModel()
        result = sbm.get_all_subscription(id=id,
                                           role=role,
                                           search_term=search_term,
                                           sort_by=sort_by,
                                           order=order,
                                           offset=offset,
                                           limit=records)

        total_records = sbm.get_all_subscription_count(id=id,
                                                        role=role,
                                                        search_term=search_term)

        total_pages = (total_records // records) + (1 if total_records % records > 0 else 0)

        if result:
            return {
                "success": True,
                "data": result,
                "message": "Aanmeldingen gevonden",
                "total_records": total_records,
                "current_page": page,
                "total_pages": total_pages
            }, 200
        return {
            "success": False,
            "message": "Aanmeldingen niet gevonden"
        }, 200
    except HTTPException as e:
        raise e     
    except Exception as e:
        print(e)
        abort(500)
        
@api_subscription.route("/<research_id>", methods=["GET"])
def get_subscription(research_id):
    id = get_jwt_identity()
    payload = get_jwt()
    role = payload.get("role")
    
    if role == "organisatie":
        abort(401, description="U kunt geen aanmeldingen inzien")
        
    try:
        sbm = SubscriptionModel()
        result = sbm.get_subscription(research_id, id)
        if result:
            return {
                "success": True,
                "data": result,
                "message": "Aanmelding gevonden"
            }, 200
        abort(404, description="Aanmelding niet gevonden")
    except HTTPException as e:
        raise e     
    except Exception as e:
        print(e)
        abort(500)
        
@api_subscription.route("/<research_id>", methods=["POST"])
def join_research(research_id):
    id = get_jwt_identity()
    payload = get_jwt()
    role = payload.get("role")

    if role != "ervaringsdeskundige":
        abort(401, description="U kunt niet deelnemen aan onderzoeken")

    try:
        sbm = SubscriptionModel()
        response = sbm.create_subscription(research_id, id)
        if response:
            if response == "already_joined":
                return {
                    "success": False,
                    "message": "U bent al aangemeld voor dit onderzoek"
                }, 200

            return {
                "success": True,
                "message": "Aangemeld voor onderzoek"
            }, 201
        abort(500, description="Er ging iets mis tijdens het verwerken van uw verzoek.")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        abort(500)
        
@api_subscription.route("/<research_id>", methods=["DELETE"])
def withdraw_from_research(research_id):
    id = get_jwt_identity()
    payload = get_jwt()
    role = payload.get("role")

    if role != "ervaringsdeskundige":
        abort(405)

    try:
        sbm = SubscriptionModel()
        response = sbm.delete_subscription(research_id, id)
        if response:
            return {
                "success": True,
                "message": "Afgemeld voor onderzoek"
            }, 200
        abort(500, description="Er ging iets mis tijdens het verwerken van uw verzoek.")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        abort(500)
          
@api_subscription.route("/", methods=["PATCH"])
def update_subscription():
    id = get_jwt_identity()
    payload = get_jwt()
    role = payload.get("role")

    data = request.get_json()

    if role != "admin":
        abort(401, description="U kunt geen aanmeldingen wijzigen :)")

    try:
        sm = SubscriptionModel()
        rowcount = sm.update_subscription_status(data)
        if rowcount:
            research_id = data.get("onderzoek_id")
            user_id = data.get("gebruiker_id")
            status = data.get("status", "Nieuw")
            
            um = UserModel()
            user = um.get_user(user_id)
            user_full_name = " ".join(word for word in [user.get("voornaam", ""), user.get("tussenvoegsel", ""), user.get("achternaam", "")] if word)
            user_email = user.get("email")
            
            rm = ResearchModel()
            research = rm.get_research(research_id, id, role)
            research_title = research.get("titel")

            am = AdminModel()
            action = f"Aanmelding van gebruiker: {user_full_name} op onderzoek: {research_title} is {status}"
            am.log_action(id, action)
            
            status_messages = {
                    "Goedgekeurd": f"Uw aanmelding op onderzoek \"{research_title}\" is goedgekeurd.",
                    "Afgekeurd": f"Uw aanmelding op onderzoek \"{research_title}\" is afgekeurd.",
                    "Nieuw": f"Uw aanmelding op onderzoek \"{research_title}\" is nog in behandeling, u krijgt binnenkort een e-mail van ons."
                }
            
            send_email(
                f"{user_email}",
                f"Aanmelding status: {status}",
                f"{status_messages[status]}"
            )
            return {
                "success": True,
                "message": "Wijzigingen voor de status van deze aanmelding zijn opgeslagen"
            }, 200
        abort(500, description="Er ging iets mis tijdens het verwerken van uw verzoek.")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        abort(500)