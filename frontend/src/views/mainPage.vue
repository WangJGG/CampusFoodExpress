<template>
  <div class="whole-page">
    <!-- 搜索栏，包含 "校园食运通" 和 搜索框内的按钮 -->
    <header class="header">
      <span class="app-name">校园食运通</span>
    </header>
    <div class="search-bar">
      <div class="search-container">
        <input
          type="text"
          class="search-input"
          v-model="searchQuery"
          placeholder="输入关键词搜索..."
        />
        <button class="search-button" @click="searchResturants">搜索</button>
      </div>
    </div>

    <!-- 轮播图 -->
    <van-swipe class="carousel" autoplay="3000">
      <van-swipe-item
        v-for="(item, index) in state.carouselImages"
        :key="index"
      >
        <div class="carousel-item">
          <img :src="item" alt="轮播图" />
        </div>
      </van-swipe-item>
    </van-swipe>

    <!-- 饭店信息列表 -->
    <div class="restaurant-list">
      <div
        class="restaurant-item"
        v-for="(restaurant, index) in display.restaurants"
        :key="index"
        @click="goToRestaurantDetail(restaurant.id)"
      >
        <!-- 商家图片 -->
        <img :src="restaurant.image" class="restaurant-img" alt="饭店图片" />
        <div class="restaurant-details">
          <h3 class="restaurant-name">{{ restaurant.name }}</h3>
          <p class="restaurant-address">{{ restaurant.address }}</p>
          <p class="restaurant-rating">
            <span class="highlight">{{ restaurant.sales }}</span> 评分 - 月售
            {{ restaurant.sales }}
          </p>
        </div>
      </div>
    </div>

    <!-- 固定底部导航栏 -->
    <bottomTabBar v-model="active" />
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { getAllRestaurants } from "@/service/restaurantService";
import bottomTabBar from '@/components/bottomTabBar.vue';
import { ElMessage } from 'element-plus'

const router = useRouter();
const active = ref(0);  // 传入BottomTabBar组件中
const searchQuery = ref("");

const state = reactive({
  carouselImages: ["./images/image1.jpg", "./images/image2.jpg"],
  restaurants: [],
});

const display = reactive({
  carouselImages: ["./images/image1.jpg", "./images/image2.jpg"],
  restaurants: [],
});

const select = reactive({
  carouselImages: ["./images/image1.jpg", "./images/image2.jpg"],
  restaurants: [],
});

// 获取所有商家信息
const fetchRestaurants = async () => {
  try {
    const restaurants = await getAllRestaurants();
    // 筛选掉 status 为 'forbided' 的餐馆
    const filteredRestaurants = restaurants.filter(
      (restaurant) => restaurant.status !== "forbided"
    );
    state.restaurants = filteredRestaurants;
  } catch (error) {
    console.error("Error loading restaurants:", error);
  }
  display.restaurants = state.restaurants;
};

// 页面加载时调用
onMounted(() => {
  fetchRestaurants();
});

// 页面跳转
// const goTo = (path) => {
//   router.push(path);
// };

// 根据商家 ID 跳转到商家详情页面
const goToRestaurantDetail = (restaurantId) => {
  router.push({
    path: "/merchantDetail",
    query: {
      id: restaurantId, // 传递商家 ID
    },
  });
};

const searchResturants = async () => {
  const query = searchQuery.value.trim().toLowerCase(); // 将查询转换为小写以实现大小写不敏感匹配

  if (query === "") {
    display.restaurants = state.restaurants;
    return;
  }

  try {
    // 清空之前的搜索结果
    select.restaurants = [];

    for (const restaurant of state.restaurants) {
      // 使用 includes() 方法进行部分匹配，并且也转换为小写以确保大小写不敏感
      if (restaurant.name.toLowerCase().includes(query)) {
        select.restaurants.push(restaurant);
      }
    }

    // 更新显示的餐厅列表
    display.restaurants = select.restaurants;

    // 如果没有找到任何匹配项，可以给用户提示
    if (select.restaurants.length === 0) {
      display.restaurants = state.restaurants;
      ElMessage.error( "我们好像没有收录您搜索的商家哦~" );
    }
  } catch (error) {
    console.error("搜索标记数据失败:", error);
  }
};
</script>

<style scoped>
/* 轮播图样式 */
.carousel {
  margin-top: 20px;
  /* 确保轮播图与搜索栏错开 */
  width: 100%;
  max-height: 300px;
  /* 限制轮播图最大高度 */
}

.carousel-item {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  /* 使图片垂直居中 */
}

.carousel img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  /* 确保图片自适应缩放 */
  object-position: center;
  /* 图片居中显示 */
  max-height: 300px;
  /* 限制最大高度 */
}

.search-bar {
  display: flex;
  align-items: center;
  /* 垂直居中 */
  gap: 10px;
  /* 子元素之间的间距 */
}

.search-input {
  width: 100%;
  border: none;
  /* 移除边框 */
  outline: none;
  /* 移除焦点时的边框效果 */
  padding: 10px;
  font-size: 16px;
  border-radius: 20px;
  /* 确保圆角边框一致 */
  background-color: transparent;
  /* 确保背景与容器一致 */
}

.search-container {
  background-color: #fff8dc;
  /* 确保容器背景色一致 */
  border-radius: 20px;
  padding: 5px;
  /* 避免内边距过多导致视觉错位 */
  border: 1px solid #ccc;
  /* 设置单一边框 */
  box-sizing: border-box;
  /* 确保边框和内边距包含在宽度中 */
}

/* 饭店信息列表样式 */
.restaurant-list {
  padding: 20px;
  padding-bottom: 80px;
  /* 增加底部内边距，避免内容被底部导航栏挡住 */
  display: flex;
  flex-direction: column;
  gap: 15px;
  /* 增加列表项之间的间距 */
}

.restaurant-item {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #f0f0f0;
  background-size: cover;
}

.restaurant-img {
  width: 80px;
  height: 80px;
  margin-right: 15px;
  object-fit: cover;
  /* 确保图片自适应 */
}

.restaurant-details {
  flex: 1;
  /* 确保餐馆信息占据剩余空间 */
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.restaurant-name {
  margin: 0;
  font-size: 18px;
  color: #000;
  /* 饭店名称黑色 */
  font-weight: bold;
}

.restaurant-address {
  margin: 5px 0;
  font-size: 14px;
  color: #666;
}

.restaurant-rating {
  margin: 5px 0;
  font-size: 16px;
}

.highlight {
  color: #ffd700;
  /* 使用黄色突出显示评分 */
  font-weight: bold;
}

/* 底部导航栏样式 */
.van-tabbar {
  position: fixed;
  bottom: 0;
  width: 100%;
  background-color: white;
}



</style>
