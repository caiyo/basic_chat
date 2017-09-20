from app import app
from app.routes import sockets
from app.services import userservice, shared, chat_group_service
from app.models.exception import UserExistsException, UserNotCreatedException
from flask import request, make_response, abort, render_template, session
from flask_jwt import JWT, jwt_required, current_identity

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return ''


@app.route('/api/user', methods = ['GET'])
@jwt_required()
def get_user():
    userid = current_identity
    current_user = userservice.get_current_user_data(userid)

    # jwt is set for sockets to authenticate
    session['jwt'] = request.headers.get('Authorization').split('JWT ')[1]
    return shared.to_json({'user' : current_user})

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
        sockets.join_group(created_user, general_group.id)

    except UserExistsException as uee:
        return make_response((str(uee), 400, None))
    except UserNotCreatedException as unce:
        return make_response((str(unce), 400, None))
    
    return shared.to_json(created_user)


# TODO add validation that userid being passed is the user requesting it
@app.route('/api/user/<userid>/chatgroups', methods=['GET'])
@jwt_required()
def get_chat_groups(userid):
    if not userid == current_identity:
        return abort(403)
    chat_groups = userservice.get_user_chat_groups(userid)
    return shared.to_json(chat_groups)

@app.route('/api/chatgroup/<groupid>/messages/viewed', methods=['POST'])
@jwt_required()
def viewed_messages(groupid):
    user_id = current_identity
    userservice.update_last_viewed(user_id, groupid)
    return ('', 204)


# TODO add validation that userid has access to group
@app.route('/api/chatgroup/<groupid>/messages', methods=['GET'])
@jwt_required()
def get_messages(groupid):
    user_id = current_identity
    before_message_id = request.args.get('beforemsgid', None)
    if before_message_id:
        limit = 20;
    limit = request.args.get('limit', limit)
    messages = userservice.get_group_messages(groupid, user_id, before_message_id=before_message_id, limit=limit)
    return shared.to_json(messages)



# TODO add validation that userid has access to group
@app.route('/api/chatgroup/<groupid>/messages/latest', methods=['GET'])
@jwt_required()
def get_messages_latest(groupid):
    user_id = current_identity
    messages = userservice.get_group_messages(groupid, user_id, latest_messages=True)
    return shared.to_json(messages) if messages else ('', 204)


def identity(payload):
    return payload['identity']


# /auth route
# Requires json with username and password fields
JWT(app, userservice.validate_user_login, identity)



@app.route('/api/protected')
@jwt_required()
def protected():
    return '%s' % current_identity