from flask import Blueprint
from app.controllers.report_controller import share_report, save_report, view_report, delete_report, report_management

report_bp = Blueprint('report', __name__, url_prefix='/report')

report_bp.route('/share_report', methods=['POST'])(share_report)
report_bp.route('/save_report', methods=['GET'])(save_report)
report_bp.route('/view_report', methods=['GET'])(view_report)
report_bp.route('/save_report/<int:total_score>/<first_name>/<last_name>/<int:age>/<form_type>', methods=['GET'])(save_report)
report_bp.route('/view_report/<int:total_score>/<first_name>/<last_name>/<int:age>/<form_type>', methods=['GET'])(view_report)
report_bp.route('/delete/<report_id>', methods=['DELETE'])(delete_report)
report_bp.route('/management', methods=['GET'])(report_management)
