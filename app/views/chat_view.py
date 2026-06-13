from flask import Blueprint
from app.controllers.chat_controller import chat

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

chat_bp.route('/', methods=['GET', 'POST'])(chat)