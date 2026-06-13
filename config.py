import os


def _env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-before-deployment')

    # Configure these email values in your local .env or deployment dashboard.
    MAIL_SERVER = os.environ.get('MAIL_SERVER', '')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = _env_bool('MAIL_USE_TLS', True)
    MAIL_USE_SSL = _env_bool('MAIL_USE_SSL', False)
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or MAIL_USERNAME or 'no-reply@ai-psychologist.local'

    MONGO_URI = os.environ.get(
        'MONGO_URI',
        "mongodb+srv://arhamahmed096_db_user:Test12345@ai-psychologist.rvqipqo.mongodb.net/adsproject?retryWrites=true&w=majority"
    )
