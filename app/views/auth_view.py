from flask import Blueprint
from app.controllers.auth_controller import (
    forgot_password,
    login,
    logout,
    reset_password,
    signup,
    verify_reset_code
)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

auth_bp.route('/login', methods=['GET', 'POST'])(login)
auth_bp.route('/logout')(logout)
auth_bp.route('/signup', methods=['POST'])(signup)
auth_bp.route('/forgot-password', methods=['GET', 'POST'])(forgot_password)
auth_bp.route('/verify-reset-code', methods=['GET', 'POST'])(verify_reset_code)
auth_bp.route('/reset-password', methods=['GET', 'POST'])(reset_password)
