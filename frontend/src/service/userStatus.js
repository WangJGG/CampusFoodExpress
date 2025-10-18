import axios from '../utils/axios'

// 设置 Axios 拦截器，统一添加 Authorization 头
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 响应拦截器，统一处理错误
// axios.interceptors.response.use(
//   (response) => response,
//   (error) => {
//     const errorMessage = error.response?.data?.message || error.message;
//     console.error('请求错误:', errorMessage);
//     alert(`请求错误: ${errorMessage}`);
//     return Promise.reject(error.response?.data || error);
//   }
// );

// API 基础路径
const API_BASE_URL = '/status';

/**
 * 获取历史状态列表
 * @returns {Promise}
 */
export const getStatusHistory = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/history`);
    return response.data;
  } catch (error) {
    console.error('获取历史状态列表失败:', error);
    throw error;
  }
};

/**
 * 创建新状态
 * @param {number|string} statusId - 状态 ID
 * @param {string} content - 状态内容
 * @returns {Promise}
 */
export const createStatus = async (statusId, content) => {
  try {
    const payload = {
      status_id: String(statusId),
      content: String(content),
    };
    const response = await axios.post(`${API_BASE_URL}/create`, payload);
    return response.data;
  } catch (error) {
    console.error('创建状态失败:', error);
    throw error;
  }
};

/**
 * 更新用户状态
 * @param {number|string} statusId - 状态 ID
 * @param {string} content - 新的状态内容
 * @returns {Promise}
 */
export const updateStatus = async (id, statusId, content) => {
  try {
    const payload = {
      status_id: String(statusId),
      content: String(content),
    };
    const response = await axios.put(`${API_BASE_URL}/update/${id}`, payload);
    return response.data;
  } catch (error) {
    console.error('修改状态失败:', error);
    throw error;
  }
};

/**
 * 结束用户状态
 * @param {number|string} statusId - 状态 ID
 * @returns {Promise}
 */
export const endStatus = async (statusId) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/end/${statusId}`);
    return response.data;
  } catch (error) {
    console.error('结束状态失败:', error);
    throw error;
  }
};

/**
 * 获取用户当前活动状态
 * @returns {Promise}
 */
export const getStatus = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/getstatus`);
    return response.data;
  } catch (error) {
    console.error('获取当前状态失败:', error);
    throw error;
  }
};

/**
 * 检查用户是否有活动状态
 * @returns {Promise}
 */
export const checkActiveStatus = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/active`);
    return response.data;
  } catch (error) {
    console.error('检查活动状态失败:', error);
    throw error;
  }
};
