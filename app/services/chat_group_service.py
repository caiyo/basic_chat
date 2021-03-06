from app.models.group import ChatGroup


def get_group(group_id=None, group_name=None):
    return ChatGroup.get(group_id=group_id, group_name=group_name)


def get_group_messages(group_id, on_or_after=None, limit=50, before_message_id=None):
    chat_group = ChatGroup(id=group_id)
    # if on or after is set, that means we requesting new messages for a user
    # in which case we want all of them
    limit = None if on_or_after else limit
    messages = chat_group.get_messages(on_or_after=on_or_after,limit=limit, before_message_id=before_message_id)
    return messages
