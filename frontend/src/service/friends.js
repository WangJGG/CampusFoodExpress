import axios from '../utils/axios';

// 获取用户详细信息并检查好友关系
export function getUserDetails(userId) {
    return axios.post(`/friend/find_user`, {
        user_id: userId
    },
        {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
}

// 添加好友
export function addFriend(friendId) {
    return axios.post('/friend/add', { friend_id: friendId }, {
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
    });
}

// 删除好友
export function deleteFriend(friendId) {
    return axios.delete('/friend/delete', {
        data: { friend_id: friendId },
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
    });
}


// 检测好友关系
export function checkFriend(friendId) {
    return axios.get('/friend/friends/check',  {
        params: { friend_id: friendId }, // 将 friend_id 作为查询参数传递
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
    });
}