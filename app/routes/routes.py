from app import app
from app.services import userservice, shared, chat_group_service
from app.models.exception import UserExistsException, UserPermissionException, UserNotCreatedException
from flask import request, make_response, abort, render_template
from flask_jwt import JWT, jwt_required, current_identity

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/user', methods = ['GET'])
@jwt_required()
def get_user():
    userid = current_identity
    current_user =userservice.get_user(user_id=userid)
    return shared.to_json(current_user)

@app.route('/api/user', methods = ['POST'])
def create_user():
    data = request.get_json()

    username = data.get('username', None)
    password = data.get('password', None)
    confirm_password = data.get('confirmPassword', None)
    
    try:
        created_user = userservice.create_user(username, password, confirm_password)

        # After user is created, add them to the 'General' group which is
        # the default group for all users
        general_group = chat_group_service.get_group(group_name='General')
        created_user.join_group(general_group.id)
    except UserExistsException as uee:
        return make_response((str(uee), 400, None))
    except UserNotCreatedException as unce:
        return make_response((str(unce), 400, None))
    
    return shared.to_json(created_user)


# TODO add validation that userid being passed is the user requesting it
@app.route('/api/user/<userid>/chatgroups', methods=['GET'])
def get_chat_groups(userid):
    # if not userid == current_identity:
    #     return abort(403)
    chat_groups = userservice.get_user_chat_groups(userid)
    return shared.to_json(chat_groups)

# TODO add validation that userid has access to group
@app.route('/api/user/<userid>/message', methods=['POST'])
def post_message(userid):
    data = request.get_json()
    group_id = data.get('groupid', None)
    msg = data.get('message', None)

    if not group_id or not msg:
        return abort(400)

    try:
        userservice.post_message(userid, group_id, msg)
        return "success"
    except UserPermissionException as upe:
        return make_response((str(upe), 403, None))

# TODO add validation that userid has access to group
@app.route('/api/chatgroup/<groupid>/messages', methods=['GET'])
def get_messages(groupid):
    messages = chat_group_service.get_group_messages(groupid)
    return shared.to_json(messages)


def identity(payload):
    return payload['identity']


# /auth route
# Requires json with username and password fields
JWT(app, userservice.validate_user_login, identity)


@app.route('/api/protected')
@jwt_required()
def protected():
    return '%s' % current_identity