from app import db, bcrypt
from datetime import datetime

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def save(self):
        collection = db['users']
        result = collection.find_one({'email': self.email})
        if result is None:
            collection.insert_one({
                'name': self.name,
                'email': self.email,
                'password': self.password,
            })
            return True
        return False

    @staticmethod
    def authenticate(email, password):
        collection = db['users']
        result = collection.find_one({'email': email})
        if result and bcrypt.check_password_hash(result['password'], password):
            return result
        return None

    @staticmethod
    def find_by_email(email):
        collection = db['users']
        return collection.find_one({'email': email})

    @staticmethod
    def save_password_reset_code(email, otp_code, expires_at):
        collection = db['users']
        otp_hash = bcrypt.generate_password_hash(otp_code).decode('utf-8')
        result = collection.update_one(
            {'email': email},
            {
                '$set': {
                    'password_reset_code_hash': otp_hash,
                    'password_reset_expires_at': expires_at,
                    'password_reset_created_at': datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0

    @staticmethod
    def verify_password_reset_code(email, otp_code):
        user = User.find_by_email(email)
        if not user:
            return False, 'invalid'

        otp_hash = user.get('password_reset_code_hash')
        expires_at = user.get('password_reset_expires_at')

        if not otp_hash or not expires_at:
            return False, 'invalid'

        if datetime.utcnow() > expires_at:
            User.clear_password_reset(email)
            return False, 'expired'

        if bcrypt.check_password_hash(otp_hash, otp_code):
            return True, 'valid'

        return False, 'invalid'

    @staticmethod
    def has_active_password_reset(email):
        user = User.find_by_email(email)
        if not user:
            return False

        expires_at = user.get('password_reset_expires_at')
        if not expires_at:
            return False

        if datetime.utcnow() > expires_at:
            User.clear_password_reset(email)
            return False

        return True

    @staticmethod
    def update_password(email, new_password):
        collection = db['users']
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        result = collection.update_one(
            {'email': email},
            {
                '$set': {'password': hashed_password},
                '$unset': {
                    'password_reset_code_hash': '',
                    'password_reset_expires_at': '',
                    'password_reset_created_at': ''
                }
            }
        )
        return result.modified_count > 0

    @staticmethod
    def clear_password_reset(email):
        collection = db['users']
        collection.update_one(
            {'email': email},
            {
                '$unset': {
                    'password_reset_code_hash': '',
                    'password_reset_expires_at': '',
                    'password_reset_created_at': ''
                }
            }
        )
