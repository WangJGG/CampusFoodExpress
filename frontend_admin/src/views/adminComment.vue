<template>
  <div class="comment-management" :back="'/admin'">
    <s-header :name="'评论管理'" />
    <a-button type="primary" @click="goTo('/admin')" style="margin-bottom: 10px">
      返回管理员主页
    </a-button>
    <div class="comment-management-box">
      <!-- 顶部的搜索框 -->
      <a-input
        placeholder="输入用户ID进行搜索"
        v-model="searchId"
        @input="searchComments"
        style="margin-bottom: 20px; width: 200px"
      />

      <!-- 评论表格 -->
      <h3>所有评论</h3>
      <a-table :columns="columns" :data="filteredComments" :pagination="false">
        <template #images="{ record }">
          <div class="image-container">
            <img
              v-for="(image, index) in record.images"
              :key="index"
              :src="image"
              alt="评论图片"
              class="image-preview"
              @error="onImageError"
            />
          </div>
        </template>
        <template #text="{ record }">
          {{ record.text }}
        </template>
        <template #created_at="{ record }">
          {{ formatDateTime(record.created_at) }}
        </template>
        <template #optional="{ record }">
          <a-space>
            <a-button status="danger" @click="confirmDelete(record.id)">删除</a-button>
          </a-space>
        </template>
      </a-table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import sHeader from '@/components/SimpleHeader.vue';
import { getAllComments, deleteComment } from '@/service/comment';
import { ElMessage } from 'element-plus';

const router = useRouter();

const columns = [
  { title: "评论ID", dataIndex: "id" },
  { title: "用户ID", dataIndex: "user_id" },
  { title: "餐厅ID", dataIndex: "restaurant_id" },
  { title: "评论内容", slotName: "text" },
  { title: "评分", dataIndex: "rating" },
  { title: "评论时间", slotName: "created_at" },
  { title: "评论图片", slotName: "images" },
  { title: "操作", slotName: "optional" }
];

const commentsData = ref([]);
const filteredComments = ref([]);
const searchId = ref('');

onMounted(function () {
  loadComments();
});

function loadComments() {
  getAllComments()
    .then(function (response) {
      commentsData.value = response.data;
      filteredComments.value = commentsData.value; // 初始显示全部评论
    })
    .catch(function (error) {
      ElMessage.error("加载评论数据失败：" + (error.response?.data?.error || error.message));
    });
}

function searchComments() {
  if (searchId.value) {
    filteredComments.value = commentsData.value.filter(function (comment) {
      return comment.user_id.toString().includes(searchId.value);
    });
  } else {
    filteredComments.value = commentsData.value;
  }
}

function confirmDelete(commentId) {
  deleteComment(commentId)
    .then(function () {
      commentsData.value = commentsData.value.filter(function (comment) {
        return comment.id !== commentId;
      });
      filteredComments.value = commentsData.value;
      ElMessage.success("评论ID " + commentId + " 删除成功");
    })
    .catch(function (error) {
      ElMessage.error("评论ID " + commentId + " 删除失败：" + (error.response?.data?.error || error.message));
    });
}

function onImageError(event) {
  event.target.src = 'https://via.placeholder.com/100';
}

function formatDateTime(dateTime) {
  if (!dateTime) return '';
  var date = new Date(dateTime);
  return date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate() + " " + date.getHours() + ":" + date.getMinutes();
}

function goTo(path) {
  router.push(path);
}
</script>

<style lang="less" scoped>
@import '../common/style/mixin';

.comment-management {
  box-sizing: border-box;
  padding: 20px;

  .comment-management-box {
    font-size: 16px;
  }

  .image-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
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
