from flask import Blueprint, abort
from werkzeug.exceptions import HTTPException
from models.disability_model import DisabilityModel

api_disability = Blueprint("api_disability", __name__)


@api_disability.route("/", methods=["GET"])
def get_all_disabilities():
    try:
        dm = DisabilityModel()
        result = dm.get_disabilities()
        if result:
            return {
                "success": True,
                "data": result,
                "message": "Beperkingen gevonden"
            }, 200
        abort(404, description="Beperkingen niet gevonden")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        abort(500)

@api_disability.route("/categories", methods=["GET"])
def get_all_disability_category():
    try:
        dm = DisabilityModel()
        result = dm.get_disability_categories()
        if result:
            return {
                "success": True,
                "data": result,
                "message": "Beperkingscategorieën gevonden"
            }, 200
        abort(404, description="Beperkingscategorieën niet gevonden")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        abort(500)