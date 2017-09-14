import uuid
from app.services import shared
import user
import chatMessage
from baseModel import BaseModel


class ChatGroup(BaseModel):

    def __init__(self, id=None, group_name=None, is_public=None, created_by=None):
        self.id = id if id else str(uuid.uuid4())
        self.group_name = group_name
        self.is_public = is_public
        self.created_by = created_by

        # Lazy loaded attributes
        self.members = None

    def get_members(self):
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

    def get_messages(self, on_or_after=None, limit=50, offset=0):
        sql = """
            SELECT  cm.message_id as msg_id,
                    cm.message as msg,
                    cm.created_by as user_guid,
                    usr.username as username,
                    cm.created_when as created_when
            FROM chat_message cm
            JOIN user usr on cm.created_by = usr.user_guid
            WHERE group_id = %s
            {0}
            ORDER BY cm.created_when DESC
            LIMIT {1} OFFSET {2}
        """
        and_clause = ''
        params = (self.id,)
        if on_or_after:
            and_clause = "AND created_when >=%s"
            params = (on_or_after)
        sql = sql.format(and_clause, limit, offset)
        results = shared.run_sql(sql, params)
        msgs = None
        if results:
            msgs = [chatMessage.ChatMessage(r['msg'], self.id, r['user_guid'], r['username'], r['msg_id']) for r in results]
        return msgs

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
