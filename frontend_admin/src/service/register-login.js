import axios from '../utils/axios';

// 登录 API 函数
export async function login(params) {
    try {
        // 始终使用管理员登录接口
        const router = 'admin/login';
    
        // 新建一个对象 tmpparams，包含 username 和 password 字段
        const tmpparams = {
          phone: params.loginName, // 假设用户名字段名为 loginName
          password: params.password,
        };

        const response = await axios.post(router, tmpparams);
        
        if (response.status === 200 && response.data) {
          return response; // 返回后端的响应数据
        } else {
          throw new Error('登录失败：服务器未返回正确的数据');
        }
    } catch (error) {
        console.error('登录请求出错:', error.message);
        throw error;
    }
}
