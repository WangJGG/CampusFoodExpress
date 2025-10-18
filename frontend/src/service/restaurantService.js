import axios from '../utils/axios'; // 引入已配置的 axios 实例

// 获取所有商家信息
export const getAllRestaurants = async () => {
  try {
    // 调用后端的 '/get_all' 路由
    const response = await axios.get('/restaurant/user_get_all',
      {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      }
    );
    return response.data;
  } catch (error) {
    throw new Error("Failed to fetch restaurants");
  }
};

// 根据商家id获取单个商家信息
export function getRestaurantById(id) {
  return axios.get(`/restaurant/get_by_id/${id}`, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });
}
