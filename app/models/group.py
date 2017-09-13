import uuid
from app.services import shared
import user


class ChatGroup(object):

    def __init__(self, id=None, group_name=None, is_public=None, created_by=None):
        self.id = id if id else str(uuid.uuid4())
        self.group_name = group_name
        self.is_public = is_public
        self.created_by = created_by

        # Lazy loaded via get_members()
        self.members = None

    def get_members(self):
        from app.models.user import User
        if self.members:
            return self.members
        sql = """
            SELECT u.user_guid as user_id,
                   u.username as username
            FROM chat_group_members cgm
            JOIN user u on u.user_guid = cgm.user_id
            WHERE group_id = %s
        """
        results = shared.run_sql(sql, (self.id,))
        members = None
        if results:
            members = [user.User(username=row['username'], user_id=row['user_id']) for row in results]
            self.members = members

        return members

    @classmethod
    def get(cls, group_id=None, group_name=None):
        if not group_id and not group_name:
            return None

        sql = """
            SELECT group_id, 
                   group_name, 
                   is_public, 
                   created_by
            FROM chat_group
            WHERE {0} = %s
        """.format('group_id' if group_id else 'group_name')

        results = shared.run_sql(sql, (group_id or group_name,), fetchone=True)
        chat_group = None
        if results:
            chat_group = ChatGroup(results['group_id'], results['group_name'], results['is_public'], results['created_by'])

        return chat_group
