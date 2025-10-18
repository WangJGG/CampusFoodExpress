import axios from '../utils/axios';
// 注册 API 函数
export async function register(params) {
    try {
      const response = await axios.post('/user/register', params);
      if (response.status === 201 && response.data) {
        return response; // 返回后端的响应数据
      } else {
        throw new Error('注册失败：服务器未返回正确的数据');
      }
    } catch (error) {
      console.error('注册请求出错:', error.message);
      throw error;
    }
  }
  
  // 发送验证码 API 函数
  export async function sendVerificationCode(phone) {
    try {
      const response = await axios.post('/user/send_code', { phone });
      if (response.status === 200) {
        return response; // 返回验证码发送状态
      } else {
        throw new Error('验证码发送失败');
      }
    } catch (error) {
      console.error('验证码发送请求出错:', error.message);
      throw error;
    }
  }
  
  export const getCaptcha = async () => {
    try {
      const response = await axios.get("/user/captcha");
      return response; // 返回图形验证码的相关信息
    } catch (error) {
      console.error("获取图形验证码失败：", error);
      throw error;
    }
  };