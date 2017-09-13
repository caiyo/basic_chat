from app.services import shared
from app.models.user import User
from app.models.exception import UserExistsException


def create_user(username, password, confirm_password):
    existing_user = User.get(username)
    if existing_user:
        raise UserExistsException("username already exists")

    if password != confirm_password:
        return None

    new_salt = shared.create_salt()
    hashed_pass = shared.hash_string(password+new_salt)
    new_user = User(username, password=hashed_pass, pass_salt=new_salt)
    new_user.create()
    return new_user.public_data()


def get_user(username):
    user = User.get(username)
    return user


def validate_user_login(username, password):
    user = User.get(username)
    
    if not user:
        return None

    user_salt = user.pass_salt
    user_pass = user.password

    input_pass_hash = shared.hash_string("{0}{1}".format(password,user_salt))
    if input_pass_hash == user_pass:
        return user.public_data()
    return None
