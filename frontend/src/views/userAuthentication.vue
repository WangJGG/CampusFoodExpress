<template>
  <div class="whole-page">
    <header class="header">
      <button class="back-button" @click="$router.push('/userPage')">
        <van-icon name="arrow-left" size="18px" />
      </button>
      <div class="title">
        <span class="app-name">实名认证</span>
      </div>
    </header>

    <div class="user-authentication">
      <!-- 动态渲染不同状态的内容 -->
      <div v-if="status === 'authorized'" class="status-box">
        <p>您的实名认证已通过。</p>
      </div>

      <div v-else-if="status === 'pending'" class="status-box">
        <p>实名认证申请正在审核中，请耐心等待。</p>
      </div>

      <div v-else-if="status === 'unauthorized'" class="authentication-box">
        <a-form
          :model="authForm"
          :rules="rules"
          ref="formRef"
          layout="vertical"
        >
          <!-- 真实姓名 -->
          <a-form-item field="real_name" label="真实姓名">
            <a-input
              v-model="authForm.real_name"
              placeholder="请输入真实姓名"
            />
          </a-form-item>

          <!-- 学号 -->
          <a-form-item field="id_number" label="学号">
            <a-input v-model="authForm.id_number" placeholder="请输入学号" />
          </a-form-item>

          <!-- 上传照片 -->
          <a-form-item field="img" label="校园卡/学生证照片">
            <input type="file" @change="onFileChange" class="file-input" />
            <img
              v-if="previewImg"
              :src="previewImg"
              alt="图片预览"
              class="preview-image"
            />
          </a-form-item>

          <!-- 提交实名认证按钮 -->
          <a-form-item>
            <a-button
              type="primary"
              class="submit-button"
              @click="submitVerification"
              >实名认证</a-button
            >
          </a-form-item>
        </a-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ElMessage } from 'element-plus'
import { reactive, ref, onMounted } from "vue";
import { getVerificationStatus, requestVerification } from "@/service/user";

const status = ref("");
const previewImg = ref(null);
const formRef = ref(null);

const authForm = reactive({
  real_name: "",
  id_number: "",
  img: null,
});

const rules = {
  real_name: [{ required: true, message: "请输入真实姓名", trigger: "blur" }],
  id_number: [{ required: true, message: "请输入学号", trigger: "blur" }],
  img: [
    { required: true, message: "请上传校园卡或学生证照片", trigger: "change" },
  ],
};
const MAX_FILE_SIZE = 16 * 1024 * 1024;
onMounted(async () => {
  try {
    const response = await getVerificationStatus();
    if (response.status === 200) {
      status.value = response.data.status;
    }
  } catch (error) {
    console.error("获取用户认证状态失败", error);
  }
});

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
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImg.value = e.target.result;
    };
    reader.readAsDataURL(file);

    authForm.img = file;
  }
};

const submitVerification = async () => {
  try {
    await formRef.value.validate();
    if (!authForm.real_name || !authForm.id_number || !authForm.img) {
      ElMessage.warning("请填写完整信息！");
      return;
    }

    const formData = new FormData();
    formData.append("real_name", authForm.real_name);
    formData.append("id_number", authForm.id_number);
    formData.append("img", authForm.img);

    const response = await requestVerification(formData);

    if (response.status === 201) {
      ElMessage.success("实名认证申请已提交，请等待审核");
      status.value = "pending";
    } else {
      ElMessage.error("提交失败，请稍后重试");
    }
  } catch (error) {
    ElMessage.error("实名认证提交失败");
    console.error("实名认证提交失败", error);
  }
};
</script>

<style scoped>
.user-authentication {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
  border-radius: 15px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.button-container {
  margin-bottom: 20px;
  width: 100%;
  display: flex;
  justify-content: flex-start;
}

.status-box {
  max-width: 400px;
  width: 100%;
  padding: 20px;
  background: #ffffff;
  border-radius: 8px;
  text-align: center;
  font-size: 16px;
  color: #333333;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.authentication-box {
  max-width: 400px;
  width: 100%;
  padding: 20px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.preview-image {
  width: 120px;
  height: 120px;
  border-radius: 8px;
  margin-top: 10px;
  object-fit: cover;
  border: 2px solid #fda085;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.file-input {
  margin-top: 10px;
}

.submit-button {
  width: 100%;
  background: #fdc385;
  border-color: #fdc385;
  color: #ffffff;
  font-weight: bold;
  transition: all 0.3s ease;
}

.submit-button:hover {
  background: #f6a665;
  border-color: #f6a665;
}
</style>
