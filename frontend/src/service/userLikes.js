import axios from '../utils/axios';

// 获取用户收藏列表 API 函数
export async function getUserFavorites() {
  try {
    // 调用后端的 GET /favorite/favorites API
    const response = await axios.get('/favorite/favorites',{
      headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
  }
});
    if (response.status === 200 && response.data) {
      return response.data; // 返回收藏列表数据
    } else {
      throw new Error('获取收藏列表失败：服务器未返回正确的数据');
    }
  } catch (error) {
    console.error('获取收藏列表请求出错:', error.message);
    throw error;
  }
}

// 添加收藏 API 函数
export async function addFavorite(restaurantId) {
  try {
    // 调用后端的 POST /favorite/favorites API
    const response = await axios.post('/favorite/favorites', { restaurant_id: restaurantId },{
      headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
  }
});
    if (response.status === 201 && response.data) {
      return response.data; // 返回添加收藏的状态
    } else {
      throw new Error('添加收藏失败：服务器未返回正确的数据');
    }
  } catch (error) {
    console.error('添加收藏请求出错:', error.message);
    throw error;
  }
}

// 取消收藏 API 函数
export async function removeFavorite(restaurantId) {
  try {
    // 调用后端的 DELETE /favorite/favorites/<restaurant_id> API
    const response = await axios.delete(`/favorite/favorites/${restaurantId}`);
    if (response.status === 200 && response.data) {
      return response.data; // 返回取消收藏的状态
    } else {
      throw new Error('取消收藏失败：服务器未返回正确的数据');
    }
  } catch (error) {
    console.error('取消收藏请求出错:', error.message);
    throw error;
  }
}
