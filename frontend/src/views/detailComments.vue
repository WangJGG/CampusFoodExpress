<template>
  <div class="detail-comments">
    <header class="header">
      <button class="back-button" @click="goBack">
        <van-icon name="arrow-left" size="18px" />
      </button>
      <div class="title">
        <span class="app-name">评论详情</span>
      </div>
    </header>

    <!-- 检查 comment 是否存在 -->
    <div v-if="comment">
      <!-- 顶部区域 -->
      <div class="header-card">
        <div class="header">
          <h2 class="restaurant-name">{{ comment.restaurant_name }}</h2>
          <!-- 商家评分 -->
          <div class="merchant-rating">
            <span v-for="star in 5" :key="star" class="star" :class="{ filled: star <= comment.rating }">★</span>
          </div>
        </div>
      

      <!-- 评论内容区域 -->
      <div class="merchant-info">
        <p class="comment-text">{{ comment.text }}</p>
        <div class="images">
          <img v-for="(image, index) in limitedImages" :key="index" :src="image" class="comment-img" alt="评论图片" />
          <button v-if="comment.images.length > 3" class="more-button" @click="showAllImages">
            +{{ comment.images.length - 3 }}
          </button>
        </div>
      </div>

      <!-- 商家信息区域 -->
      <div class="merchant-info" @click="goToRestaurantDetail(comment.restaurant_id)">
        <img :src="comment.restaurant_image" class="merchant-img" alt="商家图片" />
        <div class="merchant-details">
          <h4 class="merchant-name">{{ comment.restaurant_name }}</h4>
          <p class="merchant-rating-number">
            评分：{{ comment.restaurant_rating.toFixed(1) }}
          </p>
        </div>
      </div>
    </div>
  </div>

    <!-- 加载失败或评论为空时的提示 -->
    <div v-else>
      <p class="error-text">加载评论详情失败，请稍后重试。</p>
    </div>

    <!-- 图片弹窗 -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <button class="close-button" @click="closeModal">关闭</button>
        <img v-for="(image, index) in comment.images" :key="index" :src="image" class="modal-img" alt="评论图片" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { getComments } from "../service/userComments";
import { ElMessage } from 'element-plus'

const route = useRoute();
const router = useRouter();
const comment = ref(null);
const showModal = ref(false);

// 获取评论详情
const fetchCommentDetail = async () => {
  const commentId = route.query.id;
  try {
    const data = await getComments(commentId);
    comment.value = data;
    console.log("评论详情:", data);
  } catch (error) {
    console.error("获取评论详情失败:", error.message);
    ElMessage.error("加载评论详情失败，请稍后重试。");
  }
};

// 返回上一页
const goBack = () => {
  router.back();
};

// 跳转到商家详情页面
const goToRestaurantDetail = (restaurantId) => {
  router.push({
    path: "/merchantDetail",
    query: {
      id: restaurantId,
    },
  });
};

// 显示所有图片
const showAllImages = () => {
  showModal.value = true;
};

// 关闭图片弹窗
const closeModal = () => {
  showModal.value = false;
};

// 限制最多显示 3 张图片
const limitedImages = computed(() => comment.value?.images.slice(0, 3) || []);

// 页面加载时获取评论详情
onMounted(() => {
  fetchCommentDetail();
});
</script>

<style scoped>
.detail-comments {
  padding: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: linear-gradient(to bottom,
      rgba(246, 211, 101, 0.8),
      rgba(255, 215, 0, 0.5));
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  color: #333;
}

.floating-header {
  position: fixed;
  top: 10px;
  left: 10px;
  z-index: 1000;
  background-color: rgba(255, 255, 255, 0.95);
  padding: 8px 15px;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.back-button {
  align-self: flex-start;
  margin-bottom: 20px;
}

.back-button:hover {
  color: #ff4d4f;
}

.save-button {
  width: 100%;
  background: #fdc385;
  border-color: #fdc385;
  color: white;
  font-weight: bold;
  transition: background 0.3s ease;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-bottom: 20px;
}

.restaurant-name {
  font-size: 22px;
  font-weight: bold;
  color: #333;
}

.merchant-rating {
  display: flex;
  gap: 5px;
}

.star {
  font-size: 20px;
  color: #ccc;
}

.star.filled {
  color: #ffd700;
}

.comment-text {
  font-size: 16px;
  line-height: 1.6;
  margin: 20px 0;
  text-align: justify;
  white-space: pre-line; /* 支持换行符显示 */
  word-wrap: break-word; /* 自动换行，防止长文本超出边界 */
  display: block; /* 确保文本独占一行 */
}

.images {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  display: block; /* 图片区域设为块级元素，独占一行 */
  margin-top: 10px; /* 图片与文本之间的间距 */
}

.comment-img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 10px;
  transition: transform 0.3s ease;
}

.comment-img:hover {
  transform: scale(1.05);
}

.more-button {
  background-color: #ff7b54;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.more-button:hover {
  background-color: #ff4d4f;
}

.merchant-info {
  display: block;
  /* display: flex; */
  align-items: center;
  margin-top: 20px;
  padding: 15px;
  border-radius: 15px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.merchant-info:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
}

.merchant-img {
  width: 70px;
  height: 70px;
  border-radius: 10px;
  object-fit: cover;
}

.merchant-details {
  margin-left: 15px;
  flex: 1;
}

.merchant-name {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.merchant-rating-number {
  font-size: 14px;
  color: #666;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1001;
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 15px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  max-width: 80%;
  max-height: 80%;
  overflow-y: auto;
}

.close-button {
  align-self: flex-end;
  background-color: #ff4d4f;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.close-button:hover {
  background-color: #d9363e;
}

.modal-img {
  width: 100%;
  max-width: 400px;
  height: auto;
  border-radius: 10px;
  object-fit: cover;
}

/* 通用卡片样式 */
.header-card,
.images-card {
  background: #ffffff;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease, transform 0.3s ease;
  width: 400px; /* 或者设置一个更大的值 */
}

.content-card{
  background: #ffffff;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease, transform 0.3s ease;
  width: 400px; /* 或者设置一个更大的值 */
  display: flex;
  align-items: center;
  margin-top: 20px;
  padding: 15px;
  cursor: pointer;
}

.header-card:hover,
.content-card:hover,
.images-card:hover {
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
  transform: translateY(-5px);
}

/* 顶部区域样式 */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-direction: column;
  /* 商家名和评分垂直排列 */
  background-color: transparent;
  /* 去除任何默认背景 */
}

.restaurant-name {
  font-size: 22px;
  font-weight: bold;
  color: #333333;
}

.merchant-rating {
  display: flex;
  gap: 5px;
}

.star {
  font-size: 20px;
  color: #e0e0e0;
}

.star.filled {
  color: #ffd700;
}

/* 评论内容样式 */
.comment-text {
  font-size: 16px;
  line-height: 1.6;
  text-align: justify;
  color: #555555;
}

/* 图片区域样式 */
.images {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.comment-img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 10px;
  transition: transform 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.comment-img:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

/* 显示更多图片按钮样式 */
.more-button {
  background-color: #ff7b54;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.more-button:hover {
  background-color: #ff4d4f;
  transform: scale(1.05);
}
</style>
