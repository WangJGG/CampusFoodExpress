from repository.friend_repository import FriendRepository

class FriendService:
    @staticmethod
    def add_friend(current_user_id, friend_id):
        # 不能添加自己为好友
        if friend_id == current_user_id:
            return False

        # 检查好友是否存在
        friend = FriendRepository.get_user_by_id(friend_id, is_admin=False)
        if not friend:
            return False

        # 检查是否已存在好友关系
        existing = FriendRepository.get_friendship(current_user_id, friend_id)
        if existing:
            return False

        # 添加好友关系（双向关系）
        FriendRepository.create_friendship(current_user_id, friend_id)
        reverse = FriendRepository.get_friendship(friend_id, current_user_id)
        if not reverse:
            FriendRepository.create_friendship(friend_id, current_user_id)

        FriendRepository.commit_session()
        return True

    @staticmethod
    def delete_friend(user_id, friend_id):
        friendship = FriendRepository.get_friendship(user_id, friend_id)
        if not friendship:
            return False

        # 删除双向好友关系（如果存在）
        reverse = FriendRepository.get_friendship(friend_id, user_id)
        if reverse:
            FriendRepository.delete_friendship(reverse)

        FriendRepository.delete_friendship(friendship)
        FriendRepository.commit_session()
        return True

    @staticmethod
    def check_friendship(user_id, friend_id):
        friendship = FriendRepository.get_friendship(user_id, friend_id)
        return True if friendship is not None else False

    @staticmethod
    def get_friends(user_id, search_query, host_url, get_unread_count):
        friendships = FriendRepository.get_friendships(user_id)
        unread_counts = get_unread_count(user_id)
        friends = []

        for friendship in friendships:
            # 如果对方被禁用则跳过
            friend = FriendRepository.get_user_by_id(friendship.friend_id, is_admin=False)
            if friend.is_forbidden:
                continue
            last_message = FriendRepository.get_last_message_between(user_id, friendship.friend_id)
            friend_info = {
                'id': friend.id,
                'nickname': friend.nickname,
                'phone': friend.phone,
                'avatar': f"{host_url}{friend.avatar}" if friend.avatar
                          else f"{host_url}static/default/default_avatar.png",
                'bio': friend.bio,
                'is_admin': friend.is_admin,
                'is_forbidden': friend.is_forbidden,
                'auth_status': friend.auth_status,
                'created_at': str(friendship.created_at),
                'last_message': last_message.to_dict() if last_message else None,
                'unread_count': unread_counts.get(str(friend.id), 0)
            }
            friends.append(friend_info)

        if search_query:
            search_query_lower = search_query.lower()
            friends = [
                friend for friend in friends
                if search_query_lower in friend['nickname'].lower() or search_query_lower in friend['phone']
            ]
        return friends

    @staticmethod
    def find_user_by_phone(current_user_id, phone, host_url):
        user = FriendRepository.get_user_by_phone(phone, is_admin=False)
        if not user or user.id == current_user_id:
            return False

        avatar_url = f"{host_url}{user.avatar}" if user.avatar else f"{host_url}static/default/default_avatar.png"
        return {
            'id': user.id,
            'nickname': user.nickname,
            'phone': user.phone,
            'avatar': avatar_url,
            'bio': user.bio,
            'is_admin': user.is_admin,
            'is_forbidden': user.is_forbidden,
            'auth_status': user.auth_status
        }

    @staticmethod
    def find_user_by_id(current_user_id, target_user_id, host_url):
        user = FriendRepository.get_user_by_id(target_user_id, is_admin=False)
        if not user:
            return False

        friendship = FriendRepository.get_friendship(current_user_id, target_user_id)
        is_friend = True if friendship is not None else False
        avatar_url = f"{host_url}{user.avatar}" if user.avatar else f"{host_url}static/default/default_avatar.png"
        user_status = FriendRepository.get_user_status(target_user_id)

        return {
            'id': user.id,
            'nickname': user.nickname,
            'phone': user.phone,
            'avatar': avatar_url,
            'bio': user.bio,
            'is_admin': user.is_admin,
            'is_forbidden': user.is_forbidden,
            'auth_status': user.auth_status,
            'is_friend': is_friend,
            'status': user_status.to_dict() if user_status else None
        }
