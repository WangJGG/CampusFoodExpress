// service/userComments.js
import axios from '../utils/axios';

/**
 * 获取用户评论列表
 * @returns {Promise<Array>} 评论列表数据
 */
export const getAllComments = async () => {
  try {
    const response = await axios.get('/comment/get_by_user');
    return response.data.map((comment) => ({
      id: comment.id,
      restaurant_name: comment.restaurant_name,
      rating: comment.rating,
      created_at: comment.created_at,
    }));
  } catch (error) {
    console.error('获取评论列表失败:', error);
    throw new Error(error.response?.data?.message || error.message || '未知错误');
  }
};

/**
 * 删除指定评论
 * @param {number|string} commentId 评论的 ID
 * @returns {Promise<Object>} 删除操作的响应数据
 */
export const deleteCommentById = async (commentId) => {
  try {
    // 使用模板字符串来构建删除评论的 URL
    const response = await axios.delete(`/comment/delete/${commentId}`);
    console.log('评论删除成功:', response.data);
    return response.data;
  } catch (error) {
    console.error('删除评论失败:', error);
    throw new Error(error.response?.data?.message || error.message || '未知错误');
  }
};


/**
 * 获取评论详情
 * @param {number|string} commentId 评论的 ID
 * @returns {Promise<Object>} 评论的详细数据
 */
export const getComments = async (commentId) => {
  try {
    // 使用 axios 发送 GET 请求，并传递评论 ID
    const response = await axios.get(`/comment/get_comment/${commentId}`);

    // 返回的数据结构
    const data = response.data;
    console.log('评论详情:', data);
    // 格式化返回的数据
    return {
      id: data.id,
      images: data.images || [],
      text: data.text || '',
      created_at: data.created_at || '',
      restaurant_name: data.restaurant_name || '',
      rating: data.rating || 0,
      restaurant_image: data.restaurant_image || '',
      restaurant_id: data.restaurant_id || '',
      restaurant_rating: data.restaurant_rating || 0,
    };
  } catch (error) {
    console.error('获取评论详情失败:', error.message);
    throw new Error(error.response?.data?.message || error.message || '未知错误');
  }
};