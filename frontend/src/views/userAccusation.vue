<template>
  <div class="whole-page">
    <header class="header">
      <button class="back-button" @click="$router.push('/userPage')">
        <van-icon name="arrow-left" size="18px" />
      </button>
      <div class="title">
        <span class="app-name">举报中心</span>
      </div>
    </header>

    <div class="user-accusation">
      <div class="accusation-box">
        <!-- 举报表单 -->
        <a-form
          :model="accusation"
          :rules="rules"
          ref="accusationForm"
          layout="vertical"
        >
          <a-form-item field="complaint" label="举报内容">
            <a-textarea
              v-model="accusation.complaint"
              placeholder="✏️ 描述你的举报内容..."
              required
            />
          </a-form-item>

          <a-form-item label="上传证据">
            <div class="upload-button" @click="triggerFileInput">
              <input
                type="file"
                id="image-upload"
                accept="image/*"
                @change="handleFileUpload"
                hidden
              />
              <div v-if="previewImage.url" class="image-preview">
                <img
                  :src="previewImage.url"
                  alt="预览图"
                  class="preview-image"
                />
              </div>
              <div v-else class="image-preview">
                <img
                  src="https://th.bing.com/th/id/R.fa7714d7995851ec441f1140e979edff?rik=SL2j5GY9V%2bUvkw&riu=http%3a%2f%2ficon.chrafz.com%2fuploads%2fallimg%2f160919%2f1-1609191FU20-L.png&ehk=PlqPcLD1bVPXVB%2fCq8bf7ytoRic3tR%2fu4nKsrxdz0QM%3d&risl=&pid=ImgRaw&r=0"
                  alt="上传图片"
                  class="preview-image"
                />
              </div>
            </div>
          </a-form-item>

          <a-form-item>
            <a-button
              type="primary"
              class="submit-button"
              @click="submitAccusation"
              >提交举报</a-button
            >
          </a-form-item>
        </a-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ElMessage } from 'element-plus'
import { reactive } from "vue";
import { submitReport } from "@/service/userAccusation";

const accusation = reactive({
  complaint: "",
  evidenceFile: null,
});

const previewImage = reactive({
  url: null,
});

const rules = {
  complaint: [{ required: true, message: "请填写举报内容", trigger: "blur" }],
};
const MAX_FILE_SIZE = 16 * 1024 * 1024;
// 触发文件上传输入框
const triggerFileInput = () => {
  document.getElementById("image-upload").click();
};

// 处理文件上传
const handleFileUpload = (event) => {
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
    accusation.evidenceFile = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImage.url = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

// 提交举报请求
const submitAccusation = async () => {
  try {
    if (!accusation.complaint) {
      ElMessage.warning("举报内容不能为空！");
      return;
    }

    const formData = new FormData();
    formData.append("text", accusation.complaint);
    if (accusation.evidenceFile) {
      formData.append("image", accusation.evidenceFile);
    }

    const response = await submitReport(formData);
    if (response && response.message) {
      ElMessage.success(response.message);
      resetForm();
    } else {
      ElMessage.error("举报提交失败");
    }
  } catch (error) {
    ElMessage.error("举报提交失败，请稍后重试。");
    console.error("举报提交失败:", error.message);
  }
};

// 清空表单
const resetForm = () => {
  accusation.complaint = "";
  accusation.evidenceFile = null;
  document.getElementById("image-upload").value = "";
  previewImage.url = null;
};
</script>

<style lang="less" scoped>
.user-accusation {
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

  .accusation-box {
    width: 100%;
    max-width: 500px;
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .ant-form-item {
    margin-bottom: 16px;
  }

  .ant-input,
  .ant-textarea {
    border-radius: 8px;
    padding: 10px;
  }

  .upload-area {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
  }

  .upload-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
  }

  .upload-text {
    font-size: 14px;
  }

  .image-preview {
    margin-top: 10px;
    text-align: center;
  }

  .preview-image {
    width: 120px;
    height: 120px;
    object-fit: cover;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .submit-button {
    width: 100%;
    background: #fdc385;
    border-color: #fdc385;
    color: white;
    font-weight: bold;
    transition: background 0.3s ease;
  }

  .submit-button:hover {
    background: #f6a665;
    border-color: #f6a665;
  }

  .back-button-style {
    width: 100%;
    background: #fdc385;
    border-color: #fdc385;
    color: white;
    font-weight: bold;
    transition: background 0.3s ease;
  }

  .back-button-style:hover {
    background: #f6a665;
    border-color: #f6a665;
  }
}
</style>
