import bcrypt
from database_manager import DatabaseManager

db = DatabaseManager()

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, password_hash):
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def register_user(username, password, role="analyst"):
    if db.get_user(username):
        return False
    db.add_user(username, hash_password(password), role)
    return True

def verify_user(username, password):
    user = db.get_user(username)
    if not user:
        return False
    return verify_password(password, user[2])  # password_hash is second column
