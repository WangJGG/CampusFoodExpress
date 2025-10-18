<template>
  <div class="report-handling" :back="'/admin'">
    <s-header :name="'举报处理'"></s-header>
    <a-button type="primary" @click="goTo('/admin')" style="margin-bottom: 10px">
      返回管理员主页
    </a-button>
    <div class="report-handling-box">
      <!-- 顶部的搜索框 -->
      <a-input
        placeholder="输入用户ID进行搜索"
        v-model="searchId"
        @input="searchReport"
        style="margin-bottom: 20px; width: 200px"
      />

      <!-- 未处理举报表格 -->
      <h3>未处理举报</h3>
      <a-table :columns="columns" :data="filteredReports" :pagination="false">
        <template #image="{ record }">
          <img
            :src="record.image_path || 'https://via.placeholder.com/100'"
            alt="举报图片"
            class="image-preview"
            @error="onImageError"
          />
        </template>
        <template #details="{ record }">
          {{ record.text }}
        </template>
        <template #time="{ record }">
          {{ formatDateTime(record.created_at) }}
        </template>
        <template #optional="{ record }">
          <a-space>
            <a-button type="primary" @click="openReplyModal(record)">处理</a-button>
          </a-space>
        </template>
      </a-table>

      <!-- 已处理举报表格 -->
      <h3 style="margin-top: 30px">已处理举报</h3>
      <a-table :columns="processedColumns" :data="processedReports" :pagination="false">
        <template #image="{ record }">
          <img
            :src="record.image_path || 'https://via.placeholder.com/100'"
            alt="举报图片"
            class="image-preview"
            @error="onImageError"
          />
        </template>
        <template #details="{ record }">
          {{ record.text }}
        </template>
        <template #time="{ record }">
          {{ formatDateTime(record.created_at) }}
        </template>
        <template #replyTime="{ record }">
          {{ formatDateTime(record.review_date) }}
        </template>
      </a-table>
    </div>

    <!-- 处理模态框 -->
    <a-modal
      v-model:visible="replyModalVisible"
      title="处理举报"
      @cancel="closeReplyModal"
      @ok="submitReply"
    >
      <a-form :model="replyForm">
        <a-form-item label="举报详细信息">
          <p>{{ replyForm.details }}</p>
        </a-form-item>
        <a-form-item field="reply" label="处理意见">
          <a-input v-model="replyForm.reply" placeholder="请输入处理意见" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import sHeader from '@/components/SimpleHeader.vue'
import { getAllReports, reviewReport } from '@/service/report'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

// 表格列定义（注意：接口返回的属性名保持不变）
const columns = [
  { title: "举报用户ID", dataIndex: "user_id" },
  { title: "举报图片", slotName: "image" },
  { title: "举报详细信息", slotName: "details" },
  { title: "举报时间", slotName: "time" },
  { title: "操作", slotName: "optional" }
]

const processedColumns = [
  { title: "举报用户ID", dataIndex: "user_id" },
  { title: "举报图片", slotName: "image" },
  { title: "举报详细信息", slotName: "details" },
  { title: "举报时间", slotName: "time" },
  { title: "处理时间", slotName: "replyTime" }
]

// 内部状态数据（保持本地变量名采用驼峰）
const reportsData = ref([])
const filteredReports = ref([])
const processedReports = ref([])
const searchId = ref('')
const replyForm = ref({ reportId: '', details: '', reply: '' })
const replyModalVisible = ref(false)

const router = useRouter()

// 全局函数声明

onMounted(function () {
  loadReports()
})

async function loadReports() {
  try {
    const response = await getAllReports()
    reportsData.value = response.data
    filteredReports.value = reportsData.value.filter(function (report) {
      return report.status === 'pending'
    })
    processedReports.value = reportsData.value.filter(function (report) {
      return report.status !== 'pending'
    })
  } catch (error) {
    ElMessage.error("加载举报数据失败")
  }
}

function searchReport() {
  if (searchId.value) {
    filteredReports.value = reportsData.value.filter(function (report) {
      return report.status === 'pending' && report.user_id.toString().includes(searchId.value)
    })
    processedReports.value = reportsData.value.filter(function (report) {
      return report.status !== 'pending' && report.user_id.toString().includes(searchId.value)
    })
  } else {
    filteredReports.value = reportsData.value.filter(function (report) {
      return report.status === 'pending'
    })
    processedReports.value = reportsData.value.filter(function (report) {
      return report.status !== 'pending'
    })
  }
}

function openReplyModal(report) {
  replyForm.value.reportId = report.id
  replyForm.value.details = report.text
  replyForm.value.reply = ''
  replyModalVisible.value = true
}

function closeReplyModal() {
  replyModalVisible.value = false
}

async function submitReply() {
  try {
    await reviewReport(replyForm.value.reportId, replyForm.value.reply)
    const index = reportsData.value.findIndex(function (report) {
      return report.id === replyForm.value.reportId
    })
    if (index !== -1) {
      reportsData.value[index].status = 'processed'
      reportsData.value[index].review_date = new Date() // 设置处理时间
    }
    filteredReports.value = reportsData.value.filter(function (report) {
      return report.status === 'pending'
    })
    processedReports.value = reportsData.value.filter(function (report) {
      return report.status !== 'pending'
    })
    replyModalVisible.value = false
    ElMessage.success("处理成功")
  } catch (error) {
    ElMessage.error("处理失败")
  }
}

function onImageError(event) {
  ElMessage.warning("图片加载失败，使用占位符替换")
  event.target.src = 'https://via.placeholder.com/100'
}

function formatDateTime(dateTime) {
  if (!dateTime) return ''
  const date = new Date(dateTime)
  return (
    date.getFullYear() +
    '-' +
    (date.getMonth() + 1) +
    '-' +
    date.getDate() +
    ' ' +
    date.getHours() +
    ':' +
    date.getMinutes()
  )
}

function goTo(path) {
  router.push(path)
}
</script>

<style lang="less" scoped>
@import '../common/style/mixin';

.report-handling {
  box-sizing: border-box;
  padding: 20px;

  .report-handling-box {
    font-size: 16px;
  }

  .image-preview {
    max-width: 100px;
    max-height: 100px;
    object-fit: cover;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 4px;
  }
}
</style>
