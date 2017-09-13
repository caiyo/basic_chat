import uuid
from app.services import shared

class User(object):

    def __init__(self, username, user_id=None, password=None, pass_salt=None, display_name=None):
        
        self.username = username
        self.password = password
        self.display_name = display_name
        self.pass_salt = pass_salt
        self.id = user_id if user_id else str(uuid.uuid4())

    def create(self):
        sql = "INSERT INTO USER (user_guid, username, password, pass_salt, created_when, updated_when, deleted_when) \
            VALUES (%s, %s, %s, %s, NOW(), NOW(), '2050-01-01')"
        shared.run_sql(sql, (self.user_id, self.username, self.password, self.pass_salt), commit=True)

    def public_data(self):
        return User(self.id, self.username)
    
    @classmethod
    def get(cls, username=None, user_id=None):
        if not username or user_id:
            return None

        sql = "SELECT * FROM USER where {0} = %s"
        sql = sql.format('username' if username else 'user_guid')
        user = shared.run_sql(sql, (username), fetchone=True)
        user_obj = None
        if user:
            user_obj = User(user['user_guid'], user['username'], user['password'], 
                user['pass_salt'], user['displayname'])
        
        return user_obj

