<template>
  <div class="whole-page">
    <header class="header">
      <button class="back-button" @click="$router.push('/userPage')">
        <van-icon name="arrow-left" size="18px" />
      </button>
      <div class="title">
        <span class="app-name">我的收藏</span>
      </div>
    </header>
    <div class="user-likes">
      <!-- 收藏列表 -->
      <div class="restaurant-list">
        <div
          class="restaurant-item"
          v-for="(restaurant, index) in restaurants"
          :key="index"
        >
          <img :src="restaurant.image" class="restaurant-img" alt="饭店图片" />
          <div class="restaurant-details" @click="goToRestaurant(restaurant)">
            <h3 class="restaurant-name">{{ restaurant.name }}</h3>
            <p class="restaurant-location">{{ restaurant.address }}</p>
            <p class="restaurant-rating">
              <span class="highlight">{{ restaurant.rating }}</span> 评分 - 月售
              {{ restaurant.sales }}
            </p>
          </div>
          <button
            class="unlike-button"
            @click.stop="removeFromFavorites(restaurant)"
          >
            取消收藏
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ElMessage } from 'element-plus'
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { getUserFavorites, removeFavorite } from "../service/userLikes";

const router = useRouter();
const restaurants = ref([]);

// 获取用户收藏列表
const fetchUserFavorites = async () => {
  try {
    const data = await getUserFavorites();
    restaurants.value = data;
  } catch (error) {
    console.error("获取收藏列表失败:", error.message);
    ElMessage.error("获取收藏列表失败，请稍后重试。");
  }
};

// 取消收藏逻辑
const removeFromFavorites = async (restaurant) => {
  try {
    await removeFavorite(restaurant.id);
    restaurants.value = restaurants.value.filter((r) => r.id !== restaurant.id);
    ElMessage.success("取消收藏成功！");
  } catch (error) {
    console.error("取消收藏失败:", error.message);
    ElMessage.error("取消收藏失败，请稍后重试。");
  }
};

onMounted(() => {
  fetchUserFavorites();
});

// 跳转到餐馆详情页
const goToRestaurant = (restaurant) => {
  router.push({ name: "merchantDetail", query: { id: restaurant.id } });
};
</script>

<style scoped>
.user-likes {
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

/* 餐厅列表 */
.restaurant-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 20px;
  width: 100%;
  max-width: 600px;
}

.restaurant-item {
  display: flex;
  background-color: rgba(255, 255, 255, 1);
  padding: 15px;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease;
}

.restaurant-item:hover {
  transform: scale(1.02);
}

.restaurant-img {
  width: 80px;
  height: 80px;
  border-radius: 5px;
  object-fit: cover;
}

.restaurant-details {
  margin-left: 15px;
  flex: 1;
}

.restaurant-name {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.restaurant-location,
.restaurant-rating {
  margin: 5px 0;
  color: #555;
}

.highlight {
  font-weight: bold;
  color: #ffd700;
}

.unlike-button {
  background-color: #f6a665;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
  align-self: center;
  margin-top: 10px;
}

.unlike-button:hover {
  background-color: #f47c3c;
}
</style>
