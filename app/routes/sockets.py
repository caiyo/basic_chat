from app import socketio, app
from flask_socketio import send, emit, join_room, leave_room, disconnect
from flask import session
import jwt
import functools
from app.services import userservice, shared
import json


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        user_id = validate_token(session.get('jwt', None))
        print "authenticating user id: {0}".format(user_id)
        if not user_id:
            print "not authenticated, disconnecting"
            disconnect()
        else:
            session['user_id'] = user_id
            return f(*args, **kwargs)
    return wrapped



@socketio.on('connect')
@authenticated_only
def connect():
    print "connected"
    emit('socket_connected')


@socketio.on('disconnect')
def test_disconnect():
    print 'disconnected'
    disconnect()

@socketio.on('join_room')
@authenticated_only
def on_join(data):
    userid = session['user_id']
    group_ids = data['groupIds']
    chat_groups = userservice.get_user_chat_groups(userid, include_members=False)
    chat_group_ids = [group.id for group in chat_groups]

    if isinstance(group_ids, (str, unicode)):
        group_ids = [group_ids]

    chat_group_ids = [group_id for group_id in group_ids if group_id in chat_group_ids]

    for group_id in chat_group_ids:
        join_room(group_id)
        send(userid + ' has entered the room.', room=group_id)

@socketio.on('post_message')
@authenticated_only
def post_message(data):
    userid = session['user_id']
    msg = data['message']
    groupid = data['groupid']

    msg = userservice.post_message(userid, groupid, msg)
    msg = json.loads(shared.to_json(msg))
    emit("new_message", msg, room=groupid)


def join_group(user, groupid):
    user.join_group(groupid)
    data = {
        'group_id' : groupid,
        'user' : user
    }
    socketio.emit('new_group_member', json.loads(shared.to_json(data)), room=groupid)


def validate_token(token):
    if not token:
        return None
    try:
        token_decode = jwt.decode(token, app.config['SECRET_KEY'])
        userid = token_decode['identity']
        return userid
    except Exception as e:
        print "Error validating token: {0}".format(str(e))