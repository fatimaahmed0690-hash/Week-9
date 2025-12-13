from database_manager import DatabaseManager

db = DatabaseManager()

def register_user(username, password):
    if not username or not password:
        return False
    if db.get_user(username):
        return False
    return db.add_user(username, password)

def login_user(username, password):
    user = db.get_user(username)
    if user and user["password"] == password:
        return True
    return False
