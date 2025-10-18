import axios from '../utils/axios'

export function getUserInfo() {
  return axios.get('/user/profile',
    {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
    }
  );
}

export function getInfoById(user_id) {
  return axios.get(`/user/get_info_by_user_id/${user_id}`, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });
}

export function userLogout() {
  return axios.post('/user/logout',{},
    {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    }
  );
}

export function EditUserInfo(formData) {
  return axios.post('/user/profile/edit_profile', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });
}

export function login(params) {
  console.log(params)
  return axios.post('/user/login', params);
}

export function logout() {
  return axios.post('/user/logout')
}

export function register(params) {
  return axios.post('/user/register', params);
}

export const updateUserPassword = async (passwordInfo) => {
  try {
    const response = await axios.put('/user/profile/change_password', passwordInfo,{
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    return response;
  } catch (error) {
    throw new Error('更新密码失败');
  }
};

// 获取用户认证状态
export function getVerificationStatus() {
  return axios.get('/auth/verification_status', {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  });
}

// 提交实名认证申请
export function requestVerification(formData) {
  return axios.post('/auth/request_verification', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  });
}
