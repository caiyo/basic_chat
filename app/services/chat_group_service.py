from app.models.group import ChatGroup


def get_group(group_id=None, group_name=None):
    return ChatGroup.get(group_id=group_id, group_name=group_name)