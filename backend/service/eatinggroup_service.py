from repository.eatinggroup_repository import EatingGroupRepository

class EatingGroupService:
    @staticmethod
    def add_group(data, user_id, host_url):
        """
        创建群聊：
         - 调用 repository 层创建群聊记录，并添加当前用户为 owner 成员
         - 遍历 member_user_ids 列表，为群聊添加其他群成员
         成功返回 (group, owner_member)，失败返回 False
        """
        try:
            new_group = EatingGroupRepository.create_group(
                name=data.get('name'),
                description=data.get('description'),
                owner_user_id=user_id,
                host_url=host_url,
                image=data.get('image')
            )
            owner_member = EatingGroupRepository.add_group_member(new_group.id, user_id, role='owner')
            member_user_ids = data.get('member_user_ids', [])
            for member_user_id in member_user_ids:
                if member_user_id != user_id:
                    EatingGroupRepository.add_group_member(new_group.id, member_user_id, role='member')
            EatingGroupRepository.commit_session()
            return new_group, owner_member
        except Exception:
            return False

    @staticmethod
    def get_groups_by_user(user_id, get_group_unread_count):
        """
        根据用户 ID 获取所属群聊，并添加最新消息及未读消息计数信息，
         返回群聊列表数据
        """
        try:
            groups = EatingGroupRepository.get_groups_by_user_id(user_id)
            groups.sort(key=lambda x: x.latest_message_id if x.latest_message_id else -1, reverse=True)
            unread_counts = get_group_unread_count(user_id)
            groups_list = []
            for group in groups:
                member = EatingGroupRepository.get_group_members(group.id)
                if group.latest_message_id:
                    message = EatingGroupRepository.get_message_by_id(group.latest_message_id)
                    last_message = message.to_dict() if message else None
                else:
                    last_message = None
                group_msg = {
                    **group.to_dict_without_messages(),
                    'members': [m.to_dict() for m in member],
                    'last_message': last_message,
                    'unread_count': unread_counts.get(group.id, 0)
                }
                groups_list.append(group_msg)
            return groups_list
        except Exception:
            return False

    @staticmethod
    def get_all_groups():
        try:
            groups = EatingGroupRepository.get_all_groups()
            # 获取每个群聊所有成员信息，也加入到返回数据中
            for group in groups:
                members = EatingGroupRepository.get_group_members(group.id)
                
            return [
                {
                    **group.to_dict(),
                    'members': [member.to_dict() for member in EatingGroupRepository.get_group_members(group.id)]
                }
                for group in groups
            ]
        except Exception:
            return False

    @staticmethod
    def get_group_by_id(group_id):
        try:
            group = EatingGroupRepository.get_group_by_id(group_id)
            members = EatingGroupRepository.get_group_members(group_id)
            if group:
                return {
                    **group.to_dict_without_messages(),
                    'members': [member.to_dict() for member in members]
                }
            return False
        except Exception:
            return False

    @staticmethod
    def update_group(data):
        try:
            group = EatingGroupRepository.get_group_by_id(data.get('id'))
            if not group:
                return False
            EatingGroupRepository.update_group(
                group,
                name=data.get('name'),
                description=data.get('description'),
                image=data.get('image')
            )
            EatingGroupRepository.commit_session()
            return True
        except Exception:
            return False

    @staticmethod
    def delete_group(group_id):
        try:
            group = EatingGroupRepository.get_group_by_id(group_id)
            if not group:
                return False
            EatingGroupRepository.delete_group(group)
            EatingGroupRepository.commit_session()
            return True
        except Exception:
            return False

    @staticmethod
    def add_member(data):
        """
        添加群成员：
         - 检查群聊和用户是否存在，以及该成员是否已在群内
         成功返回新成员对象，失败返回 False
        """
        try:
            group = EatingGroupRepository.get_group_by_id(data.get('group_id'))
            if not group:
                return False
            user = EatingGroupRepository.get_user_by_id(data.get('user_id'))
            if not user:
                return False
            existing = EatingGroupRepository.get_group_member_by_user_and_group(
                data.get('user_id'), data.get('group_id')
            )
            if existing:
                return False
            new_member = EatingGroupRepository.add_group_member(data.get('group_id'), data.get('user_id'))
            EatingGroupRepository.commit_session()
            return new_member
        except Exception:
            return False

    @staticmethod
    def get_members(group_id):
        try:
            members = EatingGroupRepository.get_group_members(group_id)
            if members is None:
                return False
            return [member.to_dict() for member in members]
        except Exception:
            return False

    @staticmethod
    def delete_member(member_id):
        try:
            member = EatingGroupRepository.get_group_member_by_id(member_id)
            if not member:
                return False
            if member.role == 'owner':
                return False
            EatingGroupRepository.delete_group_member(member)
            EatingGroupRepository.commit_session()
            return True
        except Exception:
            return False

    @staticmethod
    def get_user_group_ids(user_id):
        try:
            groups = EatingGroupRepository.get_groups_by_user_id(user_id)
            return [group.id for group in groups]
        except Exception:
            return []

    @staticmethod
    def is_user_in_group(user_id, group_id):
        try:
            member = EatingGroupRepository.get_group_member_by_user_and_group(user_id, group_id)
            return bool(member)
        except Exception:
            return False