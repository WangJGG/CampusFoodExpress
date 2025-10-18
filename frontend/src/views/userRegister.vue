<template>
  <div class="container">
    <!-- 注册部分 -->
    <div class="login">
      <header name="注册">
        <h2>注册</h2>
      </header>

      <div class="login-body">
        <form @submit.prevent="onSubmit">
          <div class="user-type">
            <label>
              <input
                type="radio"
                value="user"
                v-model="state.role"
                checked
                disabled
              />
              用户注册
            </label>
          </div>

          <!-- 注册表单 -->
          <div class="form-group">
            <label for="username1">账号 (手机号)</label>
            <input
              v-model="state.username1"
              type="text"
              id="username1"
              placeholder="请输入账号"
              required
              @blur="validatePhoneNumber"
            />
            <p
              v-if="!state.isPhoneValid && state.username1"
              class="error-message"
            >
              手机号格式不正确，请输入 1 开头的 11 位数字。
            </p>
          </div>
          <div class="form-group">
            <label for="password1">密码</label>
            <input
              v-model="state.password1"
              type="password"
              id="password1"
              placeholder="请输入密码"
              required
            />
          </div>
          <div class="form-group">
            <label for="confirmPassword">重复密码</label>
            <input
              v-model="state.confirmPassword"
              type="password"
              id="confirmPassword"
              placeholder="请再次输入密码"
              required
            />
          </div>
          <div class="form-group">
            <label for="captcha">验证码</label>
            <div class="captcha-group">
              <input
                v-model="state.captcha"
                type="text"
                id="captcha"
                placeholder="请输入验证码"
                required
              />
              <img
                :src="state.captchaImage"
                alt="验证码"
                class="captcha-image"
                @click="refreshCaptcha"
              />
            </div>
            <p v-if="state.captchaError" class="error-message">
              验证码错误或已过期，请重试。
            </p>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn-submit">注册</button>
            <div class="link-login" @click="goToLogin">已有登录账号</div>
          </div>
        </form>
      </div>

      <!-- 使用须知复选框和链接 -->
      <div class="disclaimer">
        <label>
          <input type="checkbox" v-model="state.agreeToTerms" /> 我已阅读并同意
        </label>
        <span class="terms" @click="showModal = true">使用须知</span>
      </div>

      <!-- 使用自定义模态框显示消息 -->
      <div v-if="modalMessage" class="modal">
        <div class="modal-content">
          <h3>提示</h3>
          <p class="modal-text">{{ modalMessage }}</p>
          <button @click="closeModal">关闭</button>
        </div>
      </div>

      <!-- 使用须知模态框 -->
      <div v-if="showModal" class="modal">
        <div class="modal-content">
          <h3>使用须知</h3>
          <p>
            欢迎使用校园食运通！请仔细阅读以下条款：
            <br /><br />
            1.
            您需对账号和密码的安全负责，勿将其泄露给他人。如发现异常，请及时更改密码或联系我们。
            <br /><br />
            2.
            我们将严格保护您的个人信息，仅用于平台服务，未经您同意不会向第三方透露。
            <br /><br />
            3. 禁止发布违法、虚假或恶意内容，若违规我们有权限制您的使用。
            <br /><br />
            4. 我们尽力保障服务的稳定，但若因不可控因素中断，不承担相关责任。
            <br /><br />
            5. 使用条款可能会更新，您可随时查阅以了解最新内容。
            <br /><br />
            <span class="author">Author: 造火箭施工团队</span>
          </p>
          <button @click="showModal = false">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/* eslint-disable */
import { useRouter } from 'vue-router'; // 引入 Vue Router

const router = useRouter(); // 获取路由实例
import { reactive, ref, onMounted } from "vue";
import { register, getCaptcha } from "@/service/userRegister"; //sendVerificationCode
import { ElMessage } from 'element-plus'
const goToLogin = () => {
  router.push('/login'); // 跳转到 /register 页面
};
const state = reactive({
  username1: "",
  password1: "",
  confirmPassword: "",
  role: "user",
  agreeToTerms: false,
  isPhoneValid: true,
  captcha: "",
  captchaId: "",
  captchaImage: "",
  captchaError: false,
});

const showModal = ref(false);
const modalMessage = ref("");

// 添加 mounted 生命周期钩子
onMounted(async () => {
  await refreshCaptcha();
});

const validatePhoneNumber = () => {
  const phonePattern = /^1\d{10}$/;
  state.isPhoneValid = phonePattern.test(state.username1);
};

const refreshCaptcha = async () => {
  if (!state.isPhoneValid) {
    ElMessage.warning("请输入正确的手机号");
    return;
  }
  try {
    const response = await getCaptcha();
    if (response.status === 200) {
      state.captchaImage = response.data.image;
      state.captchaId = response.data.captcha_id;
    } else {
      ElMessage.error("获取验证码失败", response);
    }
  } catch (error) {
    ElMessage.error("获取验证码时出错:", error);
  }
};

const closeModal = () => {
  modalMessage.value = "";
};

const toggle = (mode) => {
  state.role = mode === "login" ? "user" : state.role;
};

const onSubmit = async () => {
  if (!state.agreeToTerms) {
    ElMessage.warning("请先阅读并同意使用须知");
    return;
  }

  if (state.password1 !== state.confirmPassword) {
    ElMessage.warning("两次输入的密码不一致，请重新输入");
    return;
  }

  if (!state.isPhoneValid) {
    ElMessage.warning("手机号格式不正确，请输入 1 开头的 11 位数字");
    return;
  }

  if (!state.captcha || !state.captchaId) {
    ElMessage.warning("请输入验证码");
    return;
  }

  try {
    const response = await register({
      phone: state.username1,
      password: state.password1,
      captcha: state.captcha,
      captcha_id: state.captchaId,
    });

    if (response.status === 201) {
      ElMessage.success("注册成功");
      state.username1 = ""; // clear the input
      state.password1 = ""; 
      state.confirmPassword = ""; 
      state.captcha = ""; 
      state.captchaError = false; 
      router.push('/login');

    } else if (response.status === 400 && error.response.data !== 'Phone number already registered') {
      ElMessage.warning('注册失败：该手机号已注册，不能重复注册');
      router.push('/login');
      // console.log(response.data.error)
    } else if (response.status === 400) {
      ElMessage.error('注册失败：验证码输入错误');
    } else {
      ElMessage.error('注册失败：发生未知错误');
    }
    refreshCaptcha(); // 刷新验证码
  } catch (error) {
    refreshCaptcha(); // 刷新验证码
    if (error.response) {
      const { status } = error.response;

      if (status === 400 && error.response.data.error === 'Phone number already registered') {
        console.log(error.response.data.error)
        ElMessage.warning('注册失败：该手机号已注册，不能重复注册');
        router.push('/login');
      } else if (status === 400) {
        ElMessage.error('注册失败：验证码输入错误');
      } else {
        ElMessage.error('注册失败：发生未知错误');
      }
    } else {
      ElMessage.error('注册出错:', error);
      modalMessage.value = '注册失败，请重试';
    }
  }
};
</script>

<style scoped>
.captcha-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.captcha-image {
  width: 100px;
  height: 40px;
  cursor: pointer;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* 设置背景图片和容器样式 */
.container {
  position: relative;
  width: 100%;
  height: 100vh;
  /* 背景图片铺满整个视口 */
  background-image: url("../static/images/img_bg_2.jpg");
  /* 替换为你的背景图片路径 */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* 添加伪元素实现半透明和变暗效果 */
.container::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  /* 50% 透明度的黑色遮罩 */
  z-index: -1;
  /* 让遮罩层在内容下方 */
}

/* 顶部标头样式 */
.app-header {
  text-align: center;
  margin-top: 20px;
}

.app-header h1 {
  font-size: 36px;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  font-weight: bold;
}

/* 全局样式 */
.login {
  margin-top: 20px;
  width: 400px;
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  /* 水平居中 */
  justify-content: center;
  /* 垂直居中 */
}

/* 标题样式 */
header h2 {
  font-size: 24px;
  color: #f47c3c;
  margin-bottom: 20px;
}

/* 用户类型选择框样式 */
.user-type {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 15px;
}

.user-type label {
  display: flex;
  align-items: center;
  font-size: 16px;
  color: #333;
  font-weight: 500;
  cursor: pointer;
}

.user-type input[type="radio"] {
  margin-right: 10px;
  accent-color: #f47c3c;
}

/* 表单组样式 */
.form-group {
  margin-bottom: 15px;
  width: 100%;
  /* 设置表单组宽度为 100% */
  max-width: 500px;
  /* 可选：限制最大宽度 */
  margin: 0 auto;
  /* 居中显示 */
  text-align: left;
}

/* 输入框样式 */
.form-group input {
  width: 100%;
  /* 输入框填满整个表单组的宽度 */
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  /* 确保 padding 不影响宽度 */
  background-color: #f0f4ff;
  /* 根据图片设置的背景色，可自行调整 */
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

.phone-group {
  display: flex;
  align-items: center;
}

.phone-group input {
  flex: 1;
}

.phone-group .btn-send-code {
  margin-left: 10px;
  background-color: #fee200;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.phone-group .btn-send-code:hover {
  background-color: #f47c3c;
}

/* 将 form-actions 居中 */
.form-actions {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  /* 居中对齐按钮 */
}

.btn-submit {
  background-color: #fee200;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  width: 80%;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.btn-submit:hover {
  background-color: #f47c3c;
}

/* 链接样式 */
.link-register,
.link-login {
  margin-top: 10px;
  color: #f47c3c;
  cursor: pointer;
  font-size: 14px;
  text-decoration: underline;
}

/* 使用须知复选框样式 */
.disclaimer {
  margin-top: 20px;
  font-size: 14px;
  text-align: center;
}

.terms {
  color: #f47c3c;
  text-decoration: underline;
  cursor: pointer;
}

/* 模态框样式 */

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: #fff;
  padding: 30px;
  border-radius: 10px;
  width: 80%;
  max-width: 600px;
  max-height: 70vh;
  /* 限制模态框高度 */
  overflow-y: auto;
  /* 超出时显示滚动条 */
  text-align: left;
}

.modal-content h3 {
  margin-bottom: 15px;
  font-size: 24px;
  /* 调整标题字体大小 */
  color: #f47c3c;
  text-align: center;
}

.modal-content p {
  font-size: 18px;
  /* 增大文字大小 */
  color: #333;
  line-height: 1.6;
}

.modal-content button {
  background-color: #f47c3c;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 20px;
  display: block;
  margin-left: auto;
  margin-right: auto;
}
</style>

