// friend.js

import axios from '../utils/axios';

// 请求亲友列表
export const fetchFriends = async () => {
  try {
    const response = await axios.get('/friend/friends');  // 假设后端接口地址是 /api/friends
    console.log('friends response:', response.data.length);
    if (response.data.length > 0) {
      console.log('friends data:', response.data);
      return response.data;  // 返回亲友数据
    // } else {
    //   console.error('failed to fetch friends');
    //   return [];
    }
  } catch (error) {
    console.error('failed to fetch friends:', error);
    return [];
  }
};

// 查找用户接口
export const findUserByPhone = async (phone) => {
  try {
    // 获取当前用户的 JWT token
    const token = localStorage.getItem('token'); // 假设 token 存储在 localStorage 中
    
    if (!token) {
      throw new Error('No token found');
    }

    // 发送 POST 请求查找用户
    const response = await axios.post(
      '/friend/find_user/phone',  // 后端接口地址
      { phone },               // 请求体，发送手机号
      {
        headers: {
          'Authorization': `Bearer ${token}`, // 带上 JWT token
        }
      }
    );

    // 返回查找到的用户信息
    return response.data;
  } catch (error) {
    // 错误处理
    console.error('Error finding user by phone:', error.response ? error.response.data : error.message);
    throw error; // 抛出错误供调用者处理
  }
};


// 请求亲友信息示例数据
// [
//     {
//       "id": 123,
//       "nickname": "John",
//       "phone": "1234567890",
//       "avatar": "/images/avatar.jpg",
//       "bio": "Hello World",
//       "is_admin": false,
//       "is_forbidden": false,
//       "auth_status": "verified",
//       "created_at": "2023-11-27T14:33:07"
//     }
//   ]