<template>
  <div class="whole-page">
    <!-- 上方淡黄色区域 -->
    <div class="header"></div>

    <!-- 按钮区域 -->
    <div class="button-container">
      <button
        :class="['tab-button', currentTab === 'orders' ? 'active' : '']"
        @click="switchTab('orders')"
      >
        我的订单
      </button>
      <button
        :class="['tab-button', currentTab === 'rewards' ? 'active' : '']"
        @click="switchTab('rewards')"
      >
        悬赏大厅
      </button>
      <button
        :class="['tab-button', currentTab === 'myDeliveries' ? 'active' : '']"
        @click="switchTab('myDeliveries')"
      >
        我的接单
      </button>
    </div>

    <!-- 中间内容区域，增加 content-container 居中背景样式 -->
    <div class="content-container">
      <div v-if="currentTab === 'orders'">
        <div v-if="orders.length > 0">
          <!-- 我的订单页面 -->
          <div
            v-for="order in orders"
            :key="order.id"
            class="order-card"
            @click="showOrderDetail(order.id)"
          >
            <div class="order-header">
              <span>{{ order.status }}</span>
              <span>{{ formatDate(order.order_date) }}</span>
            </div>
            <div class="order-details">
              <p>用户ID：{{ order.user_id }}</p>
              <p>餐馆名称：{{ order.restaurant_name || "未知餐馆" }}</p>
              <p>配送员ID：{{ order.delivery_person_id || "未指定" }}</p>
              <p>配送费用：¥{{ order.delivery_fee }}</p>
              <p>送货地址：{{ order.address }}</p>
              <p>备注：{{ order.remarks || "无" }}</p>
              <p>
                完成日期：{{ formatDate(order.completion_date) || "未完成" }}
              </p>
            </div>
          </div>
        </div>
        <div v-else class="empty-state">
          <p>您还没有发布订单哦~</p>
        </div>
      </div>

      <div v-if="currentTab === 'rewards'">
        <!-- 悬赏大厅页面 -->
        <div v-if="rewards.length > 0">
          <div v-for="reward in rewards" :key="reward.id" class="order-card" @click="showOrderDetail(reward.id)">
            <div class="order-details">
              <p>餐厅名称: {{ reward.restaurant.name }}</p>
              <p>餐厅地点: {{ reward.restaurant.address }}</p>
              <p>送达地点: {{ reward.address }}</p>
              <p>费用: ¥{{ reward.delivery_fee }}</p>
              <p>备注: {{ reward.remarks || "无" }}</p>
            </div>
          </div>
        </div>
        <div v-else class="empty-state">
          <p>悬赏大厅暂无订单</p>
        </div>

        <!-- 悬赏大厅浮动按钮 -->
        <button class="floating-button" @click="goTo('/rewardPublish')">
          +
        </button>
      </div>

      <div v-if="currentTab === 'myDeliveries'">
        <!-- 我的接单页面 -->
        <div
          v-for="delivery in myDeliveries"
          :key="delivery.id"
          class="order-card"
          @click="showOrderDetail(delivery.id)"
        >
          <div class="order-header">
            <span>{{ delivery.status }}</span>
            <span>{{ formatDate(delivery.order_date) }}</span>
          </div>
          <div class="order-details">
            <p>订单编号：{{ delivery.id }}</p>
            <p>配送费用：¥{{ delivery.delivery_fee }}</p>
            <p>送货地址：{{ delivery.address }}</p>
            <p>备注：{{ delivery.remarks || "无" }}</p>
            <p>
              完成日期：{{ formatDate(delivery.completion_date) || "未完成" }}
            </p>
          </div>
        </div>
        <div v-if="myDeliveries.length === 0" class="empty-state">
          <p>您的配送订单空空如也~~</p>
        </div>
      </div>
    </div>

    <!-- 固定底部导航栏 -->
    <bottomTabBar v-model="active" />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { getRestaurantById } from "@/service/restaurantService.js";
import {
  getOrdersByUser,
  getInitiatedOrders,
  getOrdersByDeliveryPerson,
} from "@/service/order.js";
import { ElMessage } from "element-plus";
import bottomTabBar from '@/components/bottomTabBar.vue';

const router = useRouter();

// 当前选中的标签页
const currentTab = ref("orders");
const active = ref(2);

// 从API获取的订单数据和悬赏数据
const orders = ref([]);
const rewards = ref([]);
const myDeliveries = ref([]);

// 页面加载时调用获取订单
onMounted(() => {
  ElMessage.success({ message: "欢迎来到订单大厅", duration: 1000 });
  fetchOrders();
  fetchRewards(); // 页面加载时获取悬赏订单
  fetchMyDeliveries();
});

// 获取用户的订单数据
const fetchOrders = async () => {
  try {
    const response = await getOrdersByUser();
    orders.value = response.data; // 从API返回的数据赋值给orders

    // 遍历每个订单，获取对应的餐馆信息
    for (const order of orders.value) {
      const restaurant = await getRestaurantById(order.restaurant_id); // 获取餐馆信息
      order.restaurant_name = restaurant.data.name; // 存储餐馆名称
    }
  } catch (error) {
    console.error("获取订单失败：", error);
    ElMessage.error("获取订单失败，请稍后重试。");
  }
};

// 获取悬赏大厅订单
const fetchRewards = async () => {
  try {
    const response = await getInitiatedOrders();
    rewards.value = response.data; // 设置订单数据
  } catch (error) {
    console.error("获取悬赏订单失败：", error);
    ElMessage.error("无法加载悬赏大厅，请稍后重试。");
  }
};

// 获取我的接单
const fetchMyDeliveries = async () => {
  try {
    const response = await getOrdersByDeliveryPerson();
    myDeliveries.value = response.data;
  } catch (error) {
    console.error("获取接单失败：", error);
    ElMessage.error("获取接单失败，请稍后重试。");
  }
};

// 日期格式化函数
const formatDate = (dateString) => {
  if (!dateString) return null;
  const date = new Date(dateString);
  return date.toLocaleDateString() + " " + date.toLocaleTimeString();
};

// 显示订单详情
const showOrderDetail = (orderId) => {
  router.push({ path: "/orderDetail", query: { id: orderId } });
};

// 切换标签页逻辑
const switchTab = (tab) => {
  currentTab.value = tab;
};

// 页面跳转
const goTo = (path) => {
  router.push(path);
};
</script>

<style scoped>
/* 按钮容器样式 */
.button-container {
  display: flex;
  justify-content: space-between;
  /* 确保按钮均匀对齐边界 */
  padding: 0;
  /* 去除多余内边距 */
  margin: 10px auto;
  /* 上下间距10px */
  max-width: 500px;
  /* 设置与白色区域相同的最大宽度 */
}

/* 按钮样式 */
.tab-button {
  flex: 1;
  /* 按钮均分容器宽度 */
  text-align: center;
  /* 按钮文字居中对齐 */
  max-width: 150px;
  /* 限制每个按钮的最大宽度 */
  padding: 8px 12px;
  /* 调整内边距 */
  font-size: 16px;
  /* 调整字体大小 */
  border: 2px solid rgba(255, 223, 0, 0.6);
  background-color: rgba(255, 255, 255, 0.6);
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin: 0 15px;
  /* 按钮之间设置一定的间隔 */
}

.tab-button.active {
  background-color: #fff;
  border-color: #ffd700;
  font-weight: bold;
  box-shadow: 0 0 5px rgba(255, 223, 0, 0.8);
}

.tab-button:hover {
  opacity: 0.8;
}

.tab-button:not(.active) {
  opacity: 0.5;
}

/* 中间内容容器样式 */
/* 中间内容容器样式，动态调整高度以适应内容 */
.content-container {
  max-width: 500px;
  /* 限制内容区域的最大宽度 */
  background-color: #fff;
  border-radius: 8px;
  padding: 10px;
  margin: 0 auto;
  /* 居中内容区域 */
  margin-top: 20px;
  /* 增大按钮与内容区域的距离 */
  padding-bottom: 50px;
  /* 确保内容在底部有足够的填充，不会被导航栏遮挡 */
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  min-height: 70px;
  /* 设置一个合理的最小高度，避免内容较少时显得空旷 */
  flex-grow: 1;
  /* 让容器根据内容动态调整高度 */
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  /* 内容从顶部开始排列 */
}

/* 订单卡片 */
.order-card {
  background: #fff;
  border: 1px solid #ddd;
  margin-bottom: 15px;
  border-radius: 12px;
  padding: 15px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.order-card:hover {
  transform: scale(1.02);
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.15);
  /* 加强阴影 */
}

.order-header {
  display: flex;
  justify-content: space-between;
  font-size: 16px;
  margin-bottom: 10px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #444;
}

.order-details {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  word-wrap: break-word;
  text-align: justify;
}

/* 悬赏大厅卡片 */
.reward-card {
  background: #fff;
  border: 1px solid #ddd;
  margin-bottom: 10px;
  border-radius: 5px;
  padding: 10px;
}

.reward-details {
  font-size: 14px;
  margin-bottom: 10px;
}

.details-button {
  padding: 5px 10px;
  background-color: #f9e8a0;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

/* 悬浮按钮 */
.floating-button {
  position: fixed;
  bottom: 80px;
  /* 增加 bottom 值，以确保按钮在导航栏上方 */
  right: 20px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: #f9e8a0;
  border: none;
  font-size: 36px;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.floating-button:hover {
  background-color: #00ffa2;
  transform: scale(1.1);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

/* 修改底部导航栏样式，确保它始终在页面底部 */
.van-tabbar {
  position: fixed;
  /* 固定导航栏在页面底部 */
  bottom: 0;
  width: 100%;
  background-color: white;
  z-index: 1000;
  /* 确保导航栏位于最上层 */
  box-shadow: 0 -1px 5px rgba(0, 0, 0, 0.1);
  /* 为导航栏添加轻微阴影 */
}

/* 订单为空时的样式 */
.empty-state {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 30px;
  /* 缩小内边距 */
  text-align: center;
  font-size: 18px;
  /* 字体大小适中 */
  color: #777;
  /* 柔和的灰色字体 */
  background: #fdfdfd;
  /* 明亮的背景色 */
  border: 1px solid #eee;
  /* 浅灰色边框 */
  border-radius: 12px;
  /* 圆角边框 */
  margin: 20px auto;
  /* 上下间距，水平居中 */
  max-width: 300px;
  /* 设置框的最大宽度 */
  height: auto;
  /* 设置为自动高度，移除过长的高度 */
  max-height: 400px;
  /* 设置最大高度为 400px */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  /* 轻微阴影 */
}

/* 暂无订单图标样式 */
.empty-state::before {
  content: "📭";
  /* 添加信封图标 */
  font-size: 36px;
  /* 图标大小 */
  margin-bottom: 10px;
  /* 图标与文字之间的间距 */
  color: #ffd700;
  /* 符合整体设计的暖黄色 */
}

/* 响应式布局：小屏幕优化 */
@media screen and (max-width: 368px) {
  .header {
    height: 50px;
    /* 小屏幕上进一步减少高度 */
  }

  .button-container {
    gap: 8px;
    /* 缩小按钮间距 */
  }

  .tab-button {
    font-size: 12px;
    /* 缩小按钮字体 */
    padding: 6px 10px;  /* 缩小按钮内边距 */
  }
}
</style>
