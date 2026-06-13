from flask import Blueprint
from app.controllers.form_controller import get_form, form, submit_form, details

form_bp = Blueprint('form', __name__, url_prefix='/form')

form_bp.route('/api/<form_type>', methods=['GET'])(get_form)
from flask import request

form_bp.route('/<form_type>', methods=['GET'])(form)
form_bp.route('/submit', methods=['POST'])(submit_form)
form_bp.route('/details/<int:total_score>/<form_type>', methods=['GET', 'POST'])(details)