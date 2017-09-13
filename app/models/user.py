import uuid
from app.services import shared
import group


class User(object):

    def __init__(self, username, user_id=None, password=None, pass_salt=None, display_name=None):
        
        self.username = username
        self.password = password
        self.display_name = display_name
        self.pass_salt = pass_salt
        self.id = user_id if user_id else str(uuid.uuid4())

        # Lazy loaded via get_groups()
        self.groups = None

    def create(self):
        sql = """
            INSERT INTO USER (user_guid, username, password, pass_salt, created_when, updated_when, deleted_when) 
            VALUES (%s, %s, %s, %s, NOW(), NOW(), '2050-01-01')
            """
        shared.run_sql(sql, (self.id, self.username, self.password, self.pass_salt), commit=True)

    def get_groups(self):
        if self.groups:
            return self.groups

        sql = """
            SELECT cg.group_id as group_id,
                   cg.group_name as group_name,
                   cg.is_public as is_public,
                   cg.created_by as created_by
            FROM chat_group_members cgm
            JOIN chat_group cg on cg.group_id = cgm.group_id 
            WHERE cgm.user_id = %s
        """

        results = shared.run_sql(sql, (self.id,))
        groups = None

        if results:
            groups = [group.ChatGroup(id=row['group_id'], group_name=row['group_name'],
                                is_public=row['is_public'], created_by=row['created_by'])
                      for row in results]
            self.groups = groups

        return groups

    def join_group(self, group_id):
        sql = """
            INSERT INTO chat_group_members (members_id, group_id, user_id, last_viewed, created_when, updated_when)
            VALUES(%s, %s, %s, NOW(), NOW(), NOW())
        """

        shared.run_sql(sql, (str(uuid.uuid4()), group_id, self.id), commit=True)

    def add_to_group(self, user, group_id):
        sql = """
        
        """

    def public_data(self):
        return User(self.username, self.id)
    
    @classmethod
    def get(cls, username=None, user_id=None):
        if not username and not user_id:
            return None

        sql = "SELECT * FROM USER where {0} = %s"
        sql = sql.format('username' if username else 'user_guid')
        user = shared.run_sql(sql, (username or user_id,), fetchone=True)
        user_obj = None
        if user:
            user_obj = User(user['user_guid'], user['username'], user['password'],
                            user['pass_salt'], user['displayname'])
        
        return user_obj

