import uuid
from app.services import shared
import user
import chatMessage
from baseModel import BaseModel
from datetime import date, datetime

class ChatGroup(BaseModel):

    def __init__(self, id=None, group_name=None, is_public=None, created_by=None, last_viewed=None):
        self.id = id if id else str(uuid.uuid4())
        self.group_name = group_name
        self.is_public = is_public
        self.created_by = created_by
        self.last_viewed = last_viewed

        # Lazy loaded attributes
        self.members = None
        self.messages = []

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

    def get_messages(self, on_or_after=None, limit=50, before_message_id=None):
        params = []
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
            {1} {2}
        """
        and_clause = ''
        limit_clause = ''
        offset_clause = ''
        params.append(self.id)

        if before_message_id:
            and_clause = """
                AND cm.created_when < (SELECT created_when
                                        FROM chat_message
                                        WHERE message_id = %s)
            """
            params.append(before_message_id)
        elif on_or_after:
            if isinstance(on_or_after, (datetime, date)):
                pass
                # on_or_after = on_or_after.isoformat()
            and_clause = "AND cm.created_when >=%s"
            params.append(on_or_after)
        if limit is not None:
            limit_clause = "LIMIT %s"
            params.append(limit)

        sql = sql.format(and_clause, limit_clause, offset_clause)
        results = shared.run_sql(sql, tuple(params))
        msgs = []
        if results:
            msgs = [chatMessage.ChatMessage(r['msg'], self.id, r['user_guid'], r['username'], r['msg_id'], r['created_when']) for r in results]
            msgs.sort(key=lambda k: k.created_when)
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
