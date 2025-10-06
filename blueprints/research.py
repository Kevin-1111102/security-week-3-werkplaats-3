from flask import Blueprint, render_template
from flask_jwt_extended import get_jwt


research = Blueprint("research",
                        __name__,
                        template_folder="../templates")

@research.route('/<research_id>')
def research_details(research_id):
    payload = get_jwt()
    role = payload.get("role")
    return render_template("research_details.html", research_id=research_id, role=role)