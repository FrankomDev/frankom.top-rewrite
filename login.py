from werkzeug.security import generate_password_hash, check_password_hash
import os

class Login:
    def __init__(self):
        self.pwd_hash = generate_password_hash(os.getenv("PASSWORD"))

    def try_login(self, pwd : str) -> bool:
        return check_password_hash(self.pwd_hash, pwd)