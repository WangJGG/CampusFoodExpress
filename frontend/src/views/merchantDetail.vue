<template>
  <!-- 商家详情部分 -->
  <div class="whole-page">
    <!-- 返回按钮 -->
    <header class="header">
      <button class="back-button" @click="goBack">
        <van-icon name="arrow-left" size="18px" />
      </button>
      <h2 class="app-name">{{ restaurant.name }}</h2>
    </header>

    <!-- 商家信息 -->
    <div class="restaurant-info">

      <!-- 商家图片 -->
      <div class="restaurant-img-container">
        <img :src="restaurant.image" alt="餐馆图片" class="restaurant-img">
      </div>
      <div class="restaurant-details">
        <h3 class="restaurant-name">{{ restaurant.name }}</h3>
        <p class="restaurant-address">地址： {{ restaurant.address }}</p>

        <!-- 商家评分和月售 -->
        <div class="restaurant-stats">
          <p class="restaurant-rating">评分： {{ restaurant.rating }}</p>
          <p class="restaurant-sales">月售： {{ restaurant.sales }}</p>
        </div>

      </div>
      <!-- 收藏按钮 -->
      <button class="favorite-button" :class="{ 'favorited': isFavorited }" @click="toggleFavorite">
        {{ isFavorited ? '已收藏' : '收藏' }}
      </button>

      <!-- 商家二维码 -->
      <div class="qr-code-container">
        <h3 class="qr-code-title">扫描二维码点单</h3>
        <img :src="restaurant.qr_code" alt="商家二维码" class="qr-code-img" @touchstart="startPress" @touchend="endPress"
          ref="qrImage" />
      </div>
    </div>


    <!-- 评论列表 -->
    <div class="comment-section">
      <h3 class="section-title">用户评论</h3>
      <div v-if="comments.length > 0">
        <div class="comment" v-for="comment in comments" :key="comment.id">
          <div class="comment-header">
            <span class="username">{{ comment.username }}</span>
            <span class="rating">
              <i v-for="star in comment.rating" :key="star" class="star" :class="{ filled: star <= comment.rating }">★</i>
            </span>
          </div>
          <p class="comment-content">{{ comment.text }}</p>
          <div v-if="comment.images && comment.images.length > 0" class="comment-images">
            <img v-for="img in comment.images" :src="img" :key="img" class="comment-image" />
          </div>
          <p class="comment-time">{{ formatDate(comment.created_at) }}</p>
        </div>
      </div>
      <p v-else class="no-comments">暂无评论</p>
    </div>

    <!-- 悬赏订单弹窗 -->
    <div v-if="showRewardPrompt" class="reward-prompt-overlay">
      <div class="reward-prompt-modal">
        <p>是否需要创建悬赏订单？</p>
        <div class="button-group">
          <button @click="createRewardOrder" class="yes-button">是</button>
          <button @click="cancelRewardPrompt" class="no-button">否</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router';
import { reactive, onMounted, ref } from 'vue';
import { getRestaurantById } from '@/service/restaurantService';
import { addFavorite, deleteFavorite, checkFavorite } from '@/service/favoriteService';
import { getCommentsByRestaurant } from '@/service/comment';
import jsQR from 'jsqr';
import { ElMessage } from 'element-plus'

const router = useRouter();
const route = useRoute();

const restaurant = reactive({
  name: '',
  address: '',
  phone: '',
  qr_code: '',
  description: '',
  sales: '',
  image: '',
  rating: 0,
});

const isFavorited = ref(false); // 是否已收藏
const comments = ref([]); // 评论列表
const showRewardPrompt = ref(false); // 是否显示悬赏订单弹窗
let pressTimer = null; // 用于记录长按定时器

// 获取商家详细信息
const fetchRestaurantDetails = async () => {
  try {
    const id = route.query.id; // 从路由中获取餐馆的ID
    const response = await getRestaurantById(id); // 调用后端接口，获取餐馆信息
    const data = response.data; // 获取返回的数据
    
    // 将后端返回的数据赋值到 restaurant 对象中
    Object.assign(restaurant, data);
    console.log('Restaurant Data:', restaurant);
    // 检查是否已收藏
    const favoriteStatus = await checkFavorite(id);
    isFavorited.value = favoriteStatus.isFavorited;
  } catch (error) {
    console.error("Error loading restaurant details:", error);
    // 如果获取失败，可以选择跳转回主页
    // router.push('/');
  }
};

// 切换收藏状态
const toggleFavorite = async () => {
  try {
    const id = route.query.id;
    if (isFavorited.value) {
      // 取消收藏
      await deleteFavorite(id);
    } else {
      // 添加收藏
      await addFavorite(id);
    }
    isFavorited.value = !isFavorited.value; // 更新收藏状态
  } catch (error) {
    console.error('Error toggling favorite:', error);
  }
};

// 获取评论列表
const fetchComments = async () => {
  try {
    const id = route.query.id;
    const response = await getCommentsByRestaurant(id); // 调用后端接口
    comments.value = response.data; // 更新评论列表
    console.log('Comments:', response.data);
    console.log('Comments result:', comments.value.length);
  } catch (error) {
    console.error("Error loading comments:", error);
  }
};

const startPress = () => {
  // 开始长按时启动定时器，超过 1 秒触发二维码解析
  pressTimer = setTimeout(handleLongPress, 1000);
};

const endPress = () => {
  // 停止长按时清除定时器
  if (pressTimer) clearTimeout(pressTimer);
};

// 格式化日期
const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

const handleLongPress = async () => {
  // 扫描二维码内容
  const qrContent = await decodeQRCode();
  if (qrContent) {
    console.log('QR Code Content:', qrContent);
    navigateTo(qrContent);
  } else {
    ElMessage.error('无法识别二维码，请重试');
  }
};

const decodeQRCode = async () => {
  try {
    const imgElement = document.querySelector('.qr-code-img');
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.width = imgElement.width;
    canvas.height = imgElement.height;
    context.drawImage(imgElement, 0, 0, imgElement.width, imgElement.height);

    const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
    const qrCode = jsQR(imageData.data, canvas.width, canvas.height);

    return qrCode ? qrCode.data : null;
  } catch (error) {
    console.error('二维码解析失败:', error);
    return null;
  }
};

// 模拟返回后的弹窗逻辑
// const simulateReturnAfterOrder = () => {
//   setTimeout(() => {
//     showRewardPrompt.value = true; // 模拟返回后显示弹窗
//   }, 10000); // 假设返回时间为2秒
// };

// 创建悬赏订单
const createRewardOrder = () => {
  router.push('/rewardPublish'); // 跳转到悬赏订单发布页面
};

/* eslint-disable no-undef */
const navigateTo = (content) => {
  // 判断是否为 HTTP 链接
  if (content.startsWith('http') || content.startsWith('https') || content.startsWith('www')) {
    // 如果是 URL，使用 plus.runtime.openURL 在系统默认浏览器中打开
    if (typeof window.plus !== 'undefined') {  // 检查 H5+ 环境
      console.log('H5+ API is supported, opening in default browser');
      plus.runtime.openURL(content);  // 不传递回调函数以确保在默认浏览器中打开
    } else {
      console.error('H5+ API is not supported');
      // 如果不在H5+环境中，使用window.open并在新标签页中打开
      window.open(content, '_system');  // _system 是Cordova等框架中用于指定系统浏览器的标识符
    }
  } else if (content.startsWith('weixin://')) {
    // 微信小程序链接的处理保持不变
    if (typeof window.plus !== 'undefined') {  // 检查 H5+ 环境
      ElMessage.error('微信跳转功能暂时无法实现，请截图微信扫码点单');
      // 注意：目前5+ API并不直接支持weixin://协议的处理
      // console.log('Trying to open WeChat URL:', content);
      // plus.runtime.openURL(content, function () {
      //   console.log('WeChat URL launched');
      // }, function (e) {
      //   console.error('无法打开微信: ' + e.message);
      // });
    } else {
      ElMessage.error('当前环境不支持微信跳转，请手动打开微信');
    }
  } else {
    // 其他内容提示，假设它是一个普通的 URL 但没有 http
    // 强制加上 http://，并尝试在默认浏览器中打开
    const url = 'http://' + content;
    if (typeof window.plus !== 'undefined') {
      plus.runtime.openURL(url);
    } else {
      window.open(url, '_system');
    }
  }
};

/* eslint-enable no-undef */

// 关闭弹窗
const cancelRewardPrompt = () => {
  showRewardPrompt.value = false;
};

// 返回主页
const goBack = () => {
  router.back();
};

// 页面加载时调用
onMounted(async () => {
  await fetchRestaurantDetails();
  await fetchComments();
  // simulateReturnAfterOrder(); // 模拟返回后的弹窗显示
});
</script>


<style scoped>
/* 商家信息样式 */
.restaurant-info {
  padding: 20px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-top: 15px;
}

.restaurant-details {
  display: flex;
  flex-direction: column;
  /* 信息垂直排列 */
  gap: 15px;
}

.restaurant-name {
  font-size: 22px;
  font-weight: bold;
  color: #333;
}

.restaurant-address {
  font-size: 16px;
  color: #666;
}

/* 商家评分和月售部分 */
.restaurant-stats {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.restaurant-rating,
.restaurant-sales {
  font-size: 16px;
  color: #666;
}

.favorite-button {
  padding: 10px 20px;
  font-size: 16px;
  color: white;
  background-color: #ff9800;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.favorite-button.favorited {
  background-color: #ffd700;
}

.favorite-button:hover {
  background-color: #e57373;
}

/* 商家图片样式 */
.restaurant-img-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 12px;
  overflow: hidden;
  padding: 10px;
  background-color: #f5f5f5;
  /* 背景色 */
}

.restaurant-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 12px;
}

/* 二维码样式 */
.qr-code-container {
  margin-top: 30px;
  text-align: center;
}

.qr-code-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
}

.qr-code-img {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

/* 收藏按钮样式 */
.favorite-button {
  display: inline-block;
  padding: 10px 20px;
  margin-top: 15px;
  font-size: 16px;
  color: white;
  background-color: #ff9800;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: bold;
}

.favorite-button.favorited {
  background-color: #ffd700;
}

.favorite-button:hover {
  background-color: #e57373;
}

.comment-section {
  margin-top: 30px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 15px;
}

.comment {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ddd;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.username {
  font-weight: bold;
  font-size: 16px;
  color: #333;
}

.rating {
  font-size: 14px;
  color: #FFD700;
}

.star {
  font-size: 14px;
  margin-right: 2px;
}

.star.filled {
  color: #FFD700;
}

.comment-content {
  font-size: 14px;
  color: #555;
  margin-bottom: 5px;
}

.comment-images {
  display: flex;
  gap: 10px;
  margin-bottom: 5px;
}

.comment-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.comment-time {
  font-size: 12px;
  color: #999;
}

.no-comments {
  font-size: 14px;
  color: #999;
  text-align: center;
}

/* 弹窗样式 */
.reward-prompt-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.reward-prompt-modal {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.reward-prompt-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s ease-in-out;
}

.button-group {
  margin-top: 10px;
}

.yes-button,
.no-button {
  margin: 0 10px;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}

.yes-button {
  background-color: #4caf50;
  color: white;
}

.no-button {
  background-color: #f44336;
  color: white;
}
</style>