import axios from '../utils/axios'; // 引入已配置的 axios 实例

// 获取所有评论
export function getAllComments() {
    return axios.get('/comment/get_all', {
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
    });
}

// 删除评论
export function deleteComment(commentId) {
    return axios.delete(`/comment/delete/${commentId}`, {
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
    });
}
