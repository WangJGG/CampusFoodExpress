<template>
  <div class="container">
    <!-- 标头 -->
    <header class="app-header">
      <h1>校园食运通 - 管理员登录</h1>
    </header>

    <div class="login">
      <!-- 登录界面 -->
      <div class="login-body">
        <form @submit.prevent="onSubmit">
          <!-- 登录表单 -->
          <div class="form-group">
            <label for="username">账号 (手机号)</label>
            <input
              v-model="state.username"
              type="text"
              id="username"
              placeholder="请输入账号"
              required
            />
          </div>
          <div class="form-group">
            <label for="password">密码</label>
            <input
              v-model="state.password"
              type="password"
              id="password"
              placeholder="请输入密码"
              required
            />
          </div>
          <div class="form-actions">
            <button type="submit" class="btn-submit">登录</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from "vue";
import { useRouter } from "vue-router";
import { login } from "@/service/register-login"; // 后端登录接口
import { ElMessage } from "element-plus";

const router = useRouter();

const state = reactive({
  username: "",
  password: "",
  role: "admin", // 强制角色为管理员
});

async function onSubmit() {
  if (!state.username || !state.password) {
    ElMessage.error("请填写账号和密码");
    return;
  }

  try {
    // 调用后端登录接口
    const response = await login({
      loginName: state.username,
      password: state.password,
      role: state.role,
    });

    if (response.data.token && response.data.role === "admin") {
      // 登录成功
      localStorage.setItem("token", response.data.token);
      router.push("/admin"); // 跳转到管理员页面
    } else {
      ElMessage.error("登录失败：账号或密码不匹配");
    }
  } catch (error) {
    ElMessage.error("登录失败：账号或密码不匹配");
  }
}
</script>

<style scoped>
/* 保持现有的样式，或根据需要进行调整 */
.container {
  position: relative;
  width: 100%;
  height: 100vh;
  background-image: url("../static/images/img_bg_2.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.app-header {
  text-align: center;
  margin-top: 20px;
}

.app-header h1 {
  font-size: 36px;
  color: white;
  font-weight: bold;
}

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
  justify-content: center;
}

.form-group {
  margin-bottom: 15px;
  width: 100%;
}

.form-group input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.form-actions {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
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
}

.btn-submit:hover {
  background-color: #f47c3c;
}
</style>
