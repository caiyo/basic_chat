import shared, chat_group_service
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


def get_current_user_data(userid):
    current_user = get_user(user_id=userid)
    if not current_user:
        return None
    current_user.get_groups()
    for group in current_user.groups:
        group.get_members()
        if group.group_name == 'General':
            group.messages = get_group_messages(group.id, userid)
    return current_user


def get_user_chat_groups(userid, include_members=True):
    user = User(user_id=userid)
    chat_groups = user.get_groups()

    if include_members:
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

    return user.post_message(group_id, msg)


def validate_user_login(username, password):
    user = User.get(username=username)
    if not user:
        return None

    if user.validate_password(password):
        return user
    return None


def get_group_messages(groupid, userid, latest_messages=False, before_message_id=None, limit=50):
    user = User(user_id=userid)
    last_viewed = None

    if latest_messages and not before_message_id:
        last_viewed = user.get_last_viewed(groupid)
    update_last_viewed(userid, groupid)
    messages = chat_group_service.get_group_messages(groupid, on_or_after=last_viewed, before_message_id=before_message_id, limit=limit)
    return messages


def update_last_viewed(userid, groupid):
    user = User(user_id=userid)
    user.update_last_viewed(groupid)

