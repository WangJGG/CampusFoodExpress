/*
import axios from 'axios'
import { showToast, showFailToast } from 'vant'
import { setLocal } from '@/common/js/utils'
import router from '../router'

console.log('import.meta.env', import.meta.env)

axios.defaults.baseURL = import.meta.env.MODE == 'development' ? '//backend-api-01.newbee.ltd/api/v1' : '//backend-api-01.newbee.ltd/api/v1'
axios.defaults.withCredentials = true
axios.defaults.headers['X-Requested-With'] = 'XMLHttpRequest'
axios.defaults.headers['token'] = localStorage.getItem('token') || ''
axios.defaults.headers.post['Content-Type'] = 'application/json'

axios.interceptors.response.use(res => {
  if (typeof res.data !== 'object') {
  showFailToast('服务端异常！')
    return Promise.reject(res)
  }
  if (res.data.resultCode != 200) {
    if (res.data.message) showFailToast(res.data.message)
    if (res.data.resultCode == 416) {
      router.push({ path: '/login' })
    }
    if (res.data.data && window.location.hash == '#/login') {
      setLocal('token', res.data.data)
      axios.defaults.headers['token'] = res.data.data
    }
    return Promise.reject(res.data)
  }

  return res.data
})

export default axios
*/


import axios from 'axios';
import router from '../router';
// 创建 axios 实例
const instance = axios.create({
  baseURL: 'http://127.0.0.1:5000/api', // 替换为后端 API 地址
  //baseURL: 'http://100.78.9.135:5000/api', // 测试临时使用
  timeout: 5000,
  withCredentials: true,
});

// 响应拦截器（可选，根据实际情况添加）
instance.interceptors.response.use(
  (response) => {
    // 正常响应直接返回
    return response;
  },
  (error) => {
    console.error('请求出错:', error);
    console.error(error.response);
    /* 对于422缺少参数和401未授权的请求，将路由重新push到login，不抛出错误 */
    // 检查是否返回 401 Unauthorized
    if (error.response && error.response.status === 401) {
      console.warn('未授权访问，跳转到登录页面');
      // 跳转到登录页面
      router.push('/login'); 
      // return {data: {resultCode: 401, message: '未授权访问'}};
    }
    if (error.response && error.response.status === 422) {
      console.warn('缺少参数');
      // 跳转到登录页面
      router.push('/login'); 
      // return {data: {resultCode: 422, message: '缺少参数'}};
    }
    //仍然抛出错误
    return Promise.reject(error);
    //return {data: {resultCode: 500, message: '请求出错'}};
  }
);


// 请求拦截器（可选，为所有请求添加 token（如果有的话）
instance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default instance;
