import uuid
from app.services import shared
import group
import chatMessage
from baseModel import BaseModel


class User(BaseModel):

    def __init__(self, username=None, user_id=None, password=None, pass_salt=None, display_name=None):
        
        self.username = username
        self._password = password
        self.display_name = display_name
        self._pass_salt = pass_salt
        self.id = user_id if user_id else str(uuid.uuid4())

        # Lazy loaded via get_groups()
        self.groups = None

    def create(self):
        sql = """
            INSERT INTO USER (user_guid, username, password, pass_salt, created_when, updated_when, deleted_when) 
            VALUES (%s, %s, %s, %s, NOW(), NOW(), '2050-01-01')
            """
        shared.run_sql(sql, (self.id, self.username, self._password, self._pass_salt), commit=True)

    def get_groups(self):
        if self.groups:
            return self.groups

        sql = """
            SELECT cg.group_id as group_id,
                   cg.group_name as group_name,
                   cg.is_public as is_public,
                   cg.created_by as created_by,
                   cgm.last_viewed as last_viewed
            FROM chat_group_members cgm
            JOIN chat_group cg on cg.group_id = cgm.group_id 
            WHERE cgm.user_id = %s
        """

        results = shared.run_sql(sql, (self.id,))
        groups = []

        if results:
            groups = [group.ChatGroup(id=row['group_id'], group_name=row['group_name'],
                                is_public=row['is_public'], created_by=row['created_by'], last_viewed=row['last_viewed'])
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

    def validate_password(self, in_pass):
        hashed_inpass = shared.hash_string('{0}{1}'.format(in_pass, self._pass_salt))

        if hashed_inpass == self._password:
            return True
        return False

    def post_message(self, group_id, msg):
        msg = chatMessage.ChatMessage(msg, group_id, self.id)
        msg = msg.post()
        return msg

    def get_last_viewed(self, groupid):
        sql= """
            SELECT last_viewed 
            FROM chat_group_members cgm
            WHERE group_id = %s
            AND user_id = %s 
        """
        result = shared.run_sql(sql, (groupid, self.id), fetchone=True)
        last_viewed = None
        if result:
            last_viewed = result['last_viewed']

        return last_viewed

    def update_last_viewed(self, groupid):
        sql = """
            UPDATE chat_group_members
            SET last_viewed = NOW()
            WHERE group_id = %s
            AND user_id = %s
        """

        shared.run_sql(sql, (groupid, self.id), commit=True)
        return

    @classmethod
    def get(cls, username=None, user_id=None):
        if not username and not user_id:
            return None

        sql = "SELECT * FROM USER where {0} = %s"
        sql = sql.format('username' if username else 'user_guid')
        user = shared.run_sql(sql, (username or user_id,), fetchone=True)
        user_obj = None
        if user:
            user_obj = User(user['username'], user['user_guid'], user['password'],
                            user['pass_salt'], user['displayname'])

        return user_obj

