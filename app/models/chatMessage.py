import uuid
from app.services import shared
from baseModel import BaseModel


class ChatMessage(BaseModel):

    def __init__(self, msg, group_id, created_by, username=None, msg_id=None, created_when=None):
        self.msg_id = msg_id if msg_id else str(uuid.uuid4())
        self.group_id = group_id
        self.message = msg
        self.username = username
        self.created_by = created_by
        self.created_when = created_when

    def post(self):
        sql = """
            INSERT INTO chat_message (message_id, group_id, created_by, message, created_when, updated_when)
            VALUES (%s, %s, %s,%s, NOW(4), NOW())
        """
        shared.run_sql(sql, (self.msg_id, self.group_id, self.created_by, self.message), commit=True)
        return self.get(self.msg_id)

    @classmethod
    def get(cls, msg_id):
        sql = """
            SELECT cm.*, u.username 
            FROM chat_message cm 
            JOIN user u on cm.created_by = u.user_guid
            WHERE message_id = %s
        """

        result = shared.run_sql(sql, (msg_id,), fetchone=True)
        if result:
            msg = ChatMessage(result['message'], result['group_id'], result['created_by'], username=result['username'],
                              msg_id=result['message_id'], created_when=result['created_when'])
            return msg
        return None

