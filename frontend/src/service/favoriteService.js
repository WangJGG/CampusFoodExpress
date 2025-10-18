import axios from '../utils/axios'; // 引入已配置的 axios 实例

// 添加收藏
export const addFavorite = async (restaurantId) => {
    try {
        const response = await axios.post(
            '/favorite/favorites',
            { restaurant_id: restaurantId },
            {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                },
            }
        );
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.error || "Failed to add favorite");
    }
};

// 取消收藏
export const deleteFavorite = async (restaurantId) => {
    try {
        const response = await axios.delete(`/favorite/favorites/${restaurantId}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
        });
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.error || "Failed to delete favorite");
    }
};

// 检查是否已收藏
export const checkFavorite = async (restaurantId) => {
    try {
        const response = await axios.get('/favorite/favorites/check', {
            params: { restaurant_id: restaurantId },
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
        });
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.error || "Failed to check favorite status");
    }
};
