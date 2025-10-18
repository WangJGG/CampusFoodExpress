<template>
  <div class="authentication-handling">
    <s-header :name="'实名认证管理'" :back="'/admin'" />
    <a-button
      type="primary"
      @click="$router.push('/admin')"
      style="margin-bottom: 10px"
    >
      返回管理员主页
    </a-button>
    <div class="authentication-handling-box">
      <!-- 顶部的搜索框 -->
      <a-input
        placeholder="输入用户ID进行搜索"
        v-model="searchId"
        @input="searchAuthentication"
        style="margin-bottom: 10px; width: 200px"
      />

      <!-- 未处理实名认证表格 -->
      <h3>未处理实名认证</h3>
      <a-table
        :columns="columns"
        :data="filteredAuthentications"
        :pagination="false"
      >
        <template #auth_image="{ record }">
          <img
            :src="record.auth_image"
            alt="校卡照片"
            style="max-width: 100px"
          />
        </template>
        <template #status="{ record }">
          <p>{{ record.status }}</p>
          <p v-if="record.status === 'pending'">未处理</p>
          <p v-else-if="record.status === 'authorized'">通过</p>
          <p v-else-if="record.status === 'unauthorized'">驳回</p>
        </template>
        <template #optional="{ record }">
          <a-space>
            <a-button type="primary" @click="openReplyModal(record)"
              >处理</a-button
            >
          </a-space>
        </template>
      </a-table>

      <!-- 已处理实名认证表格 -->
      <h3 style="margin-top: 30px">已处理实名认证</h3>
      <a-table
        :columns="processedColumns"
        :data="processedAuthentications"
        :pagination="false"
      >
        <template #auth_image="{ record }">
          <img
            :src="record.auth_image"
            alt="校卡照片"
            style="max-width: 100px"
          />
        </template>
        <template #status="{ record }">
          <p v-if="record.status === 'pending'">未处理</p>
          <p v-else-if="record.status === 'authorized'">通过</p>
          <p v-else-if="record.status === 'unauthorized'">驳回</p>
        </template>
      </a-table>
    </div>

    <!-- 处理模态框 -->
    <a-modal
      v-model:visible="replyModalVisible"
      title="处理实名认证"
      @cancel="replyModalVisible = false"
      @before-ok="submitAuthentication()"
    >
      <a-form :model="replyForm">
        <a-form-item label="用户ID">
          <p>{{ replyForm.user_id }}</p>
        </a-form-item>
        <a-form-item label="用户名">
          <p>{{ replyForm.nick_name }}</p>
        </a-form-item>
        <a-form-item label="真实姓名">
          <p>{{ replyForm.real_name }}</p>
        </a-form-item>
        <a-form-item label="电话号码">
          <p>{{ replyForm.phone }}</p>
        </a-form-item>
        <a-form-item label="学号">
          <p>{{ replyForm.id_number }}</p>
        </a-form-item>
        <a-form-item label="校卡照片">
          <img
            :src="replyForm.auth_image"
            alt="校卡照片"
            style="max-width: 100px"
          />
        </a-form-item>
        <a-form-item label="处理状态">
          <a-radio-group v-model="replyForm.status">
            <a-radio value="authorized">通过</a-radio>
            <a-radio value="unauthorized">驳回</a-radio>
          </a-radio-group>
        </a-form-item>
        <a-form-item label="请求日期">
          <p>{{ replyForm.request_date }}</p>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import sHeader from "@/components/SimpleHeader.vue";
import { get_authenticate, update_authenticate } from "@/service/auth";
import { ElMessage } from "element-plus";

const loading = ref(false);

const columns = [
  { title: "用户ID", dataIndex: "user_id" },
  { title: "用户名", dataIndex: "nick_name" },
  { title: "真实姓名", dataIndex: "real_name" },
  { title: "电话号码", dataIndex: "phone" },
  // { title: "学校", dataIndex: "school" },
  { title: "学号", dataIndex: "id_number" },
  { title: "校卡照片", slotName: "auth_image" },
  { title: "处理状态", dataIndex: "status" },
  { title: "请求日期", dataIndex: "request_date" },
  // { title: "审核日期", dataIndex: "review_date" },
  // { title: "审核人", dataIndex: "reviewed_by" },
  { title: "操作", slotName: "optional" },
];

const processedColumns = [
  { title: "用户ID", dataIndex: "user_id" },
  { title: "用户名", dataIndex: "nick_name" },
  { title: "真实姓名", dataIndex: "real_name" },
  { title: "电话号码", dataIndex: "phone" },
  // { title: "学校", dataIndex: "school" },
  { title: "学号", dataIndex: "id_number" },
  { title: "校卡照片", slotName: "auth_image" },
  { title: "处理状态", dataIndex: "status" },
  { title: "请求日期", dataIndex: "request_date" },
  { title: "审核日期", dataIndex: "review_date" },
  { title: "审核人", dataIndex: "reviewed_by" },
];

const authenticationsData = ref([]);
const filteredAuthentications = ref([]);
const processedAuthentications = ref([]);
const searchId = ref("");
const replyForm = ref({
  id: "",
  user_id: "",
  nick_name: "",
  real_name: "",
  phone: "",
  id_number: "",
  auth_image: "",
  status: "",
  request_date: "",
  review_date: "",
  reviewed_by: "",
});
const replyModalVisible = ref(false);

onMounted(async function () {
  const data = await get_authenticate();
  // 这里 data.data 为后端返回的认证列表
  authenticationsData.value = data.data;
  filteredAuthentications.value = data.data.filter(function (auth) {
    return auth.status === "pending";
  });
  processedAuthentications.value = data.data.filter(function (auth) {
    return auth.status !== "pending";
  });
});

function searchAuthentication() {
  if (searchId.value) {
    filteredAuthentications.value = authenticationsData.value.filter(function (
      auth
    ) {
      return (
        auth.status === "pending" &&
        auth.user_id.toString().includes(searchId.value)
      );
    });
    processedAuthentications.value = authenticationsData.value.filter(function (
      auth
    ) {
      return (
        auth.status !== "pending" &&
        auth.user_id.toString().includes(searchId.value)
      );
    });
  } else {
    filteredAuthentications.value = authenticationsData.value.filter(function (
      auth
    ) {
      return auth.status === "pending";
    });
    processedAuthentications.value = authenticationsData.value.filter(function (
      auth
    ) {
      return auth.status !== "pending";
    });
  }
}

function openReplyModal(auth) {
  replyForm.value = { ...auth };
  replyModalVisible.value = true;
}

async function submitAuthentication() {
  if (
    replyForm.value.status !== "authorized" &&
    replyForm.value.status !== "unauthorized"
  ) {
    ElMessage.error("请选择通过或驳回");
    return;
  }

  const index = authenticationsData.value.findIndex(function (auth) {
    return auth.id === replyForm.value.id;
  });
  if (index === -1) {
    ElMessage.error("未找到该认证请求");
    return;
  }
  try {
    loading.value = true;
    const response = await update_authenticate(replyForm.value);
    if (response.status === 200) {
      // 更新本地数据
      const newStatus = replyForm.value.status;
      if (newStatus === "authorized" || newStatus === "unauthorized") {
        authenticationsData.value[index].status = newStatus;
      } else {
        console.error("无效的状态:", newStatus);
        return;
      }
      filteredAuthentications.value = authenticationsData.value.filter(
        function (auth) {
          return auth.status === "pending";
        }
      );
      processedAuthentications.value = authenticationsData.value.filter(
        function (auth) {
          return auth.status !== "pending";
        }
      );
      replyModalVisible.value = false;
      ElMessage.success("认证处理成功");
      await refreshData();
    } else {
      ElMessage.error("更新失败，状态码：" + response.status);
    }
  } catch (error) {
    console.error("更新认证时发生错误:", error);
    ElMessage.error("更新认证时发生错误");
  } finally {
    loading.value = false;
    replyModalVisible.value = false;
  }
}

async function refreshData() {
  try {
    const data = await get_authenticate();
    authenticationsData.value = data.data;
    filteredAuthentications.value = data.data.filter(function (auth) {
      return auth.status === "pending";
    });
    processedAuthentications.value = data.data.filter(function (auth) {
      return auth.status !== "pending";
    });
  } catch (error) {
    console.error("刷新数据时发生错误:", error);
    ElMessage.error("刷新数据时发生错误");
  } finally {
    loading.value = false; // 确保加载状态关闭
  }
}
</script>

<style lang="less" scoped>
@import "../common/style/mixin";

.authentication-handling {
  box-sizing: border-box;
  padding: 20px;

  .authentication-handling-box {
    font-size: 16px;
  }
}
</style>
