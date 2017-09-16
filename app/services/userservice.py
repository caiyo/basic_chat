from app.services import shared
from app.models.user import User
from app.models.exception import UserExistsException, UserPermissionException, UserNotCreatedException


def create_user(username, password, confirm_password):
    existing_user = User.get(username)

    if not username:
        raise UserNotCreatedException("No username provided")

    if existing_user:
        raise UserExistsException("Username already exists")

    if password != confirm_password:
        raise UserNotCreatedException("Password and confirm password don't match")

    if not password or not confirm_password:
        raise UserNotCreatedException("Password cannot be blank")

    new_salt = shared.create_salt()
    hashed_pass = shared.hash_string(password+new_salt)
    new_user = User(username, password=hashed_pass, pass_salt=new_salt)
    new_user.create()
    return new_user


def get_user(username=None, user_id=None):
    user = User.get(username=username, user_id=user_id)
    return user


def get_user_chat_groups(userid):
    user = User(user_id=userid)
    chat_groups = user.get_groups()

    for chat_group in chat_groups:
        chat_group.get_members()

    return chat_groups


def post_message(user_id, group_id, msg):
    user = User(user_id=user_id)
    user.get_groups()
    permitted_to_post = None
    for group in user.groups:
        if group.id == group_id:
            permitted_to_post = True

    if not permitted_to_post:
        raise UserPermissionException('Not permitted to post to {0}'.format(group_id))

    user.post_message(group_id, msg)


def validate_user_login(username, password):
    user = User.get(username=username)
    if not user:
        return None

    if user.validate_password(password):
        return user
    return None
