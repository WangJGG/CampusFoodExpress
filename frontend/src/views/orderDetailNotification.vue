<template>
  <div class="order-notification-page">
    <!-- 页面标题 -->
    <div class="header">
      <button class="back-button" @click="goBack">
        <van-icon name="arrow-left" size="18px" />
      </button>
      <h1>订单通知</h1>
    </div>

    <!-- 订单消息列表 -->
    <div class="order-list">
      <div v-for="(notification, index) in notifications" :key="index" class="order-item"
        @click="goToOrderDetail(notification.order_id)">
        <!-- 通知时间 -->
        <p class="order-time">{{ formatDate(notification.created_at) }}</p>
        <!-- 通知内容 -->
        <div class="order-content">
          <h3 class="order-title">{{ notification.title }}</h3>
          <p class="order-desc" v-html="notification.content"></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getAllOrderNotifications } from '../service/orderNotification'; // 引入订单通知API
import { Icon as VanIcon } from 'vant';

export default {
  components: {
    VanIcon,
  },
  setup() {
    const router = useRouter();
    const notifications = ref([]); // 存储通知列表

    // 获取所有订单通知
    const fetchNotifications = async () => {
      try {
        const response = await getAllOrderNotifications(); // 调用 API 获取所有通知
        notifications.value = response; // 更新通知列表
        console.log('获取订单通知成功:', notifications);
      } catch (error) {
        console.error('获取订单通知失败:', error);
      }
    };

    // 格式化时间
    const formatDate = (dateStr) => {
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      const date = new Date(dateStr);
      return date.toLocaleString('zh-CN', options);
    };

    // 跳转到订单详情
    const goToOrderDetail = (id) => {
      router.push(`/orderDetail?id=${id}`);
    };

    // 返回上一页
    const goBack = () => {
      router.back();
    };

    // 页面加载时获取数据
    onMounted(() => {
      fetchNotifications();
    });

    return {
      notifications,
      formatDate,
      goToOrderDetail,
      goBack,
    };
  },
};
</script>

<style scoped>
.order-notification-page {
  background-color: #f5f5f5;
  font-family: Arial, sans-serif;
  padding: 0 16px;
}

/* 页面标题 */
.header {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  background-color: #fff;
  padding: 16px;
  border-bottom: 1px solid #ddd;
  text-align: center;
}

.header h1 {
  margin: 0;
  font-size: 18px;
  color: #333;
  font-weight: bold;
}


.back-button:hover {
  color: #007aff;
}

/* 通知列表 */
.order-list {
  margin-top: 16px;
}

/* 每条通知的容器 */
.order-item {
  background-color: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
}

.order-item:hover {
  transform: translateY(-5px);
}

/* 通知时间 */
.order-time {
  font-size: 12px;
  color: #888;
  margin-bottom: 8px;
}

/* 通知标题 */
.order-title {
  font-size: 16px;
  color: #333;
  margin: 0 0 8px;
  font-weight: bold;
}

/* 通知描述 */
.order-desc {
  font-size: 14px;
  color: #555;
  line-height: 1.5;
}
</style>