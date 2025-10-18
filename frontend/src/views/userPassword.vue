<template>
  <div class="whole-page">
    <header class="header">
      <button class="back-button" @click="$router.push('/userPage')">
        <van-icon name="arrow-left" size="18px" />
      </button>
      <div class="title">
        <span class="app-name">修改密码</span>
      </div>
    </header>

    <div class="user-password">
      <div class="user-password-box">
        <!-- 密码修改表单 -->
        <a-form
          :model="password_info"
          :rules="rules"
          ref="passwordForm"
          layout="vertical"
        >
          <a-form-item field="old_password" label="旧密码">
            <a-input-password
              v-model="password_info.old_password"
              placeholder="请输入旧密码"
              required
            />
          </a-form-item>

          <a-form-item field="new_password" label="新密码">
            <a-input-password
              v-model="password_info.new_password"
              placeholder="请输入新密码"
              required
            />
          </a-form-item>

          <a-form-item field="confirm_password" label="确认密码">
            <a-input-password
              v-model="password_info.confirm_password"
              placeholder="请再次输入新密码"
              required
            />
          </a-form-item>

          <a-form-item>
            <a-button
              type="primary"
              class="save-button"
              @click="checkPasswordsAndSubmit"
            >
              保存修改
            </a-button>
          </a-form-item>
        </a-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ElMessage } from 'element-plus'
import { reactive } from "vue";
import { updateUserPassword } from "@/service/user";
import { useRouter } from "vue-router";

const rules = {
  old_password: [{ required: true, message: "请输入旧密码", trigger: "blur" }],
  new_password: [{ required: true, message: "请输入新密码", trigger: "blur" }],
  confirm_password: [
    { required: true, message: "请确认新密码", trigger: "blur" },
  ],
};

const password_info = reactive({
  old_password: "",
  new_password: "",
  confirm_password: "",
});

const router = useRouter();

const checkPasswordsAndSubmit = async () => {
  if (
    !password_info.old_password ||
    !password_info.new_password ||
    !password_info.confirm_password
  ) {
    ElMessage.warning("请填写所有必填项");
    return;
  }

  if (password_info.new_password !== password_info.confirm_password) {
    ElMessage.error("新密码与确认密码不一致，请重新输入");
    return;
  }

  if (password_info.old_password === password_info.new_password) {
    ElMessage.warning("新密码不能与旧密码相同");
    return;
  }

  try {
    const response = await updateUserPassword({
      old_password: password_info.old_password,
      new_password: password_info.new_password,
    });

    if (response.status === 200) {
      ElMessage.success("密码修改成功，请重新登录");
      router.push("/login");
    } else {
      ElMessage.error("密码更新失败");
    }
  } catch (error) {
    ElMessage.error("原密码输入错误！");
    console.error("更新密码失败", error);
  }
};
</script>

<style lang="less" scoped>
.user-password {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
  border-radius: 15px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);

  .button-container {
    margin-bottom: 20px;
    width: 100%;
    display: flex;
    justify-content: flex-start;
  }

  .user-password-box {
    width: 100%;
    max-width: 400px;
    background-color: #ffffff;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  a-button {
    background: #fdc385;
    border-color: #fdc385;
    color: #ffffff;
    font-weight: bold;
    transition: all 0.3s ease;

    &:hover {
      background: #f6a665;
      border-color: #f6a665;
    }
  }

  .save-button {
    width: 100%;
    background: #fdc385;
    border-color: #fdc385;
    color: white;
    font-weight: bold;
    transition: background 0.3s ease;
  }

  .save-button:hover {
    background: #f6a665;
    border-color: #f6a665;
  }

  .ant-form-item-label {
    font-size: 14px;
    font-weight: 600;
    color: #555;
  }

  .ant-input-password {
    border-radius: 8px;
    border: 2px solid #fda085;
    padding: 10px;
    transition: all 0.3s ease;
  }

  .ant-input-password:focus {
    border-color: #f6d365;
    box-shadow: 0 0 0 2px rgba(253, 160, 133, 0.2);
  }

  .ant-form-item {
    margin-bottom: 16px;
  }

  .ant-form-item-control-input {
    padding: 4px;
  }
}
</style>
