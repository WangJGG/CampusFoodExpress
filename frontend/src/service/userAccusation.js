import axios from '../utils/axios';

// 提交举报信息 API 函数
export async function submitReport(formData) {
  try {
    const response = await axios.post('/report/submit', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
    });
    

    if (response.status === 201 && response.data) {
      return response.data; // 返回后端的响应数据
    } else {
      throw new Error('举报提交失败：服务器未返回正确的数据');
    }
  } catch (error) {
    console.error('举报提交请求出错:', error.message);
    throw error;
  }
}
