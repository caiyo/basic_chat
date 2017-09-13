from app import app
from app.services import userservice, shared, chat_group_service
from app.models.exception import UserExistsException
from flask import request, make_response 
from flask_jwt import JWT, jwt_required, current_identity
import json

@app.route('/test')
def test():
    sql = "SELECT * FROM test where col = 1"
    result = shared.run_sql(sql, fetchone=True)
    print result
    return json.dumps(result)

@app.route('/user', methods = ['POST'])
def create_user():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    try:
        created_user = userservice.create_user(username, password, confirm_password)

        # After user is created, add them to the 'General' group which is
        # the default group for all users
        general_group = chat_group_service.get_group(group_name='General')
        created_user.join_group(general_group.id)
    except UserExistsException as uee:
        return make_response((str(uee), 403, None))
    
    return "success"


def identity(payload):
    return payload['identity']

#/auth route
#Requires json with username and password fields
JWT(app, userservice.validate_user_login, identity)

@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity