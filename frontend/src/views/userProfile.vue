<template>
  <div class="whole-page">
    <header class="header">
      <button class="back-button" @click="$router.push('/userPage')">
        <van-icon name="arrow-left" size="18px" />
      </button>
      <div class="title">
        <span class="app-name">用户个人信息管理</span>
        <!-- 标题部分 -->
      </div>
    </header>

    <div class="user-profile">
      <div class="back-button"></div>
      <div class="user-profile-box">
        <!-- 个人信息编辑表单 -->
        <a-form
          :model="userInfo"
          :rules="rules"
          ref="userForm"
          layout="vertical"
        >
          <a-form-item field="avatar" label="头像">
            <input type="file" @change="onFileChange" class="file-input" />
            <img
              v-if="previewAvatar.url"
              :src="previewAvatar.url"
              alt="头像预览"
              class="avatar-preview"
            />
            <img
              v-else-if="userInfo.avatar"
              :src="userInfo.avatar"
              alt="当前头像"
              class="avatar-preview"
            />
          </a-form-item>

          <a-form-item field="nickname" label="昵称">
            <a-input v-model="userInfo.nickname" />
          </a-form-item>

          <a-form-item field="bio" label="个性签名">
            <a-input v-model="userInfo.bio" />
          </a-form-item>

          <a-form-item>
            <a-button type="primary" class="save-button" @click="updateUserInfo"
              >保存修改</a-button
            >
          </a-form-item>
        </a-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ElMessage } from 'element-plus'
import { reactive, onMounted } from "vue";
import { getUserInfo, EditUserInfo } from "@/service/user";
import { useRouter } from "vue-router";
const MAX_FILE_SIZE = 16 * 1024 * 1024;
const rules = {
  avatar: [{ required: true, message: "请上传头像", trigger: "change" }],
  nickname: [{ required: true, message: "请输入昵称", trigger: "blur" }],
  bio: [{ required: true, message: "请输入个性签名", trigger: "blur" }],
};

const userInfo = reactive({
  avatar: null,
  nickname: "",
  bio: "",
});

const previewAvatar = reactive({ url: null });

const onFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    const allowedTypes = ["image/png", "image/jpg", "image/jpeg", "image/gif"];
    if (!allowedTypes.includes(file.type)) {
      ElMessage.error("只能上传 png, jpg, jpeg, gif 格式的图片文件！");
      event.target.value = "";
      return;
    }
    if (file && file.size > MAX_FILE_SIZE) {
      ElMessage.warning("文件大小不能超过 16MB");
      event.target.value = ""; // 清空文件选择
    }
    userInfo.avatar = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      previewAvatar.url = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const router = useRouter();

onMounted(async () => {
  try {
    const response = await getUserInfo();
    if (response.status === 200) {
      userInfo.avatar = response.data.avatar;
      userInfo.nickname = response.data.nickname;
      userInfo.bio = response.data.bio;
    }
  } catch (error) {
    console.error("获取用户信息失败", error);
  }
});

const updateUserInfo = async () => {
  try {
    if (!userInfo.nickname || !userInfo.bio) {
      ElMessage.warning("昵称或个性签名不能为空！");
      return;
    }
    const response = await EditUserInfo(userInfo);
    if (response.status === 200) {
      ElMessage.success("用户信息更新成功！");
      router.push("/userPage");
    } else {
      ElMessage.error("更新失败，请稍后重试");
    }
  } catch (error) {
    ElMessage.error("更新用户信息失败");
    console.error("更新用户信息失败", error);
  }
};
</script>

<style lang="less" scoped>
.user-profile {
  padding: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);

  .back-button {
    align-self: flex-start;
    margin-bottom: 20px;
  }

  .user-profile-box {
    width: 100%;
    max-width: 500px;
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .avatar-preview {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid #ffd700;
    margin-top: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
  }

  .avatar-preview:hover {
    transform: scale(1.1);
  }

  .file-input {
    margin-top: 10px;
  }

  .ant-form-item {
    margin-bottom: 16px;
  }

  .ant-input {
    border-radius: 8px;
    padding: 10px;
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
}
</style>
