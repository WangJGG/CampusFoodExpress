<template>
  <div class="whole-page">
    <header class="header">
      <button class="back-button" @click="$router.push('/userPage')">
        <van-icon name="arrow-left" size="18px" />
      </button>
      <div class="title">
        <span class="app-name">我的评论</span>
      </div>
    </header>

    <div class="user-comments">
      <!-- 评论列表 -->
      <div class="comment-list">
        <div
          class="comment-item"
          v-for="(comment, index) in comments"
          :key="comment.id"
        >
          <!-- 餐馆图片和详情 -->
          <div class="comment-content" @click="goToDetail(comment.id)">
            <div class="restaurant-details">
              <h3 class="restaurant-name">{{ comment.restaurant_name }}</h3>
              <div class="rating">
                <span
                  v-for="star in 5"
                  :key="star"
                  class="star"
                  :class="{ filled: star <= comment.rating }"
                >
                  ★
                </span>
              </div>
              <p class="comment-date">{{ comment.created_at }}</p>
            </div>
          </div>
          <!-- 删除按钮 -->
          <button
            class="delete-button"
            @click.stop="deleteComment(comment, index)"
          >
            删除
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ElMessage, ElMessageBox } from "element-plus";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { getAllComments, deleteCommentById } from "../service/userComments";

const router = useRouter();
const comments = ref([]);

// 获取用户评论列表
const fetchUserComments = async () => {
  try {
    comments.value = await getAllComments();
    console.log(comments.value);
  } catch (error) {
    console.error("获取评论列表失败:", error.message);
    ElMessage.error("获取评论列表失败，请稍后重试。");
  }
};

// 删除评论
const deleteComment = async (comment, index) => {
  try {
    await ElMessageBox.confirm("确定要删除这条评论吗？", "删除确认", {
      confirmButtonText: "确认",
      cancelButtonText: "取消",
      type: "warning",
    });

    await deleteCommentById(comment.id);
    comments.value.splice(index, 1);
    ElMessage.success("评论删除成功！");
  } catch (error) {
    if (error !== "cancel") {
      console.error("删除评论失败:", error.message);
      ElMessage.error("删除评论失败，请稍后重试。");
    }
  }
};

// 跳转到评论详情页
const goToDetail = (commentId) => {
  router.push({ name: "detailComments", query: { id: commentId } });
};

// 页面加载时获取评论列表
onMounted(() => {
  fetchUserComments();
});
</script>

<style scoped>
.user-comments {
  padding: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* 返回按钮样式 */
.back-button {
  align-self: flex-start;
  margin-bottom: 20px;
}

.back-button-style {
  background-color: #fdc385;
  border-color: #fdc385;
  color: white;
  font-weight: bold;
  transition: background-color 0.3s ease;
  border-radius: 8px;
  padding: 10px 20px;
}

.back-button-style:hover {
  background-color: #f6a665;
  border-color: #f6a665;
}

/* 评论列表 */
.comment-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 100%;
  max-width: 600px;
}

/* 单个评论项 */
.comment-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #fff;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.comment-item:hover {
  transform: scale(1.02);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

/* 餐馆详情样式 */
.comment-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  cursor: pointer;
}

.restaurant-details {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.restaurant-name {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.rating {
  display: flex;
  gap: 2px;
}

.star {
  font-size: 20px;
  color: #ccc;
}

.star.filled {
  color: #ffd700;
}

.comment-date {
  font-size: 14px;
  color: #666;
}

/* 删除按钮样式 */
.delete-button {
  background-color: #f6a665;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.delete-button:hover {
  background-color: #f47c3c;
}
</style>
