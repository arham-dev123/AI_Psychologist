from flask import Blueprint
from app.controllers.main_controller import home, dashboard, settings, contact_us, services

main_bp = Blueprint('main', __name__)

main_bp.route('/', methods=['GET'])(home)
main_bp.route('/dashboard', methods=['GET'])(dashboard)
main_bp.route('/settings', methods=['GET', 'POST'])(settings)
main_bp.route('/contactUs', methods=['GET'])(contact_us)
main_bp.route('/services', methods=['GET'])(services)