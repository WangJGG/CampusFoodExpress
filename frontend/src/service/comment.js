import axios from '../utils/axios'; // 引入已配置的 axios 实例
// 根据商家名称获取单个商家信息
export function getRestaurantById(id) {
  return axios.get(`/restaurant/get_by_id/${id}`, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });
}

// 添加评论
export const addComment = (formData) => {
  return axios.post('/comment/add', formData, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
      'Content-Type': 'multipart/form-data'
    },
  });
};

// 根据餐厅 ID 获取评论列表
export const getCommentsByRestaurant = async (restaurantId) => {
  return axios.get(`/comment/get_by_restaurant/${restaurantId}`, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });
};
