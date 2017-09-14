from app.models.group import ChatGroup


def get_group(group_id=None, group_name=None):
    return ChatGroup.get(group_id=group_id, group_name=group_name)


def get_group_messages(group_id):
    chat_group = ChatGroup(id=group_id)

    messages = chat_group.get_messages()
    return messages