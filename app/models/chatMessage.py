import uuid
from app.services import shared

class ChatMessage(object):

    def __init__(self, msg, group_id, created_by, username=None, msg_id=None):
        self.msg_id = msg_id if msg_id else str(uuid.uuid4())
        self.group_id = group_id
        self.message = msg
        self.username = username
        self.created_by = created_by

    def post(self):
        sql = """
            INSERT INTO chat_message (message_id, group_id, created_by, message, created_when, updated_when)
            VALUES (%s, %s, %s,%s, NOW(), NOW())
        """
        shared.run_sql(sql, (self.msg_id, self.group_id, self.created_by, self.msg), commit=True)
    
    @classmethod
    def get_messages(cls, group_id, on_or_after=None, limit=50):
        sql = """
            SELECT  msg.message_id as msg_id
                    msg.message as msg,
                    msg.created_by as user_guid,
                    usr.username as username,
                    msg.created_when as created_when,
            FROM chat_message msg
            JOIN user usr on msg.created_by = usr.user_guid
            WHERE 1=1
            {0}
            ORDER BY msg.created_when DESC
            LIMIT {1}
        """
        and_clause = ''
        params = None
        if on_or_after:
            and_clause = "AND created_when >=%s"
            params = (on_or_after)
        sql = sql.format(and_clause, limit)
        results = shared.run_sql(sql, params)
        msgs = [User(r.msg, group_id, r.user_guid, r.username, r.msg_id) for r in results]
        return msgs
