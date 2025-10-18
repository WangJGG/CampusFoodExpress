import axios from '../utils/axios';

// 获取所有商家信息
export const getAllRestaurants = async () => {
  try {
    // 调用后端的 '/get_all' 路由
    const response = await axios.get('/restaurant/get_all',
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

// 创建新商家
export function addRestaurant(data) {
  return axios.post('/restaurant/add', data, {
    headers: {
      'Content-Type': 'multipart/form-data',
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });
}

// 更新商家信息
export function updateRestaurant(restaurantId, data) {
  return axios.put(`/restaurant/update/${restaurantId}`, data, {
    headers: {
      'Content-Type': 'multipart/form-data',
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });
}

// 删除商家
export function deleteRestaurant(restaurantId) {
  return axios.delete(`/restaurant/delete/${restaurantId}`, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });
}

// 禁用商家
export function forbidRestaurant(id) {
  return axios.patch(`/restaurant/forbid/${id}`, {}, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });
}

// 取消禁用商家
export function unforbidRestaurant(id) {
  return axios.patch(`/restaurant/unforbid/${id}`, {}, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });
}
