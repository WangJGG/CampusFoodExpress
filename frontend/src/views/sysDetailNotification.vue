<template>
  <div class="notification-page">
    <!-- 页面标题 -->
    <div class="header">
      <!-- 返回按钮 -->
      <button class="back-button" @click="goBack">
        <van-icon name="arrow-left" size="18px" />
      </button>
      <h1>系统通知</h1>
    </div>

    <!-- 系统消息列表 -->
    <div class="notifications">
      <div v-for="(notification, index) in notifications" :key="index" class="notification-item">
        <!-- 消息时间 -->
        <p class="notification-time">{{ formatDate(notification.created_at) }}</p>
        <!-- 消息内容 -->
        <div class="notification-content">
          <h3 class="notification-title">{{ notification.title }}</h3>
          <p class="notification-desc" v-html="notification.content"></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { getAllNotifications } from '../service/sysNotification';
import { useRouter } from 'vue-router';
import { Icon as VanIcon } from 'vant';

export default {
  components: {
    VanIcon,
  },
  setup() {
    const router = useRouter();
    const notifications = ref([]); // 存储系统消息

    // 获取系统消息
    const fetchNotifications = async () => {
      try {
        const response = await getAllNotifications(); // 调用 API 获取所有通知
        notifications.value = response; // 更新消息列表
      } catch (error) {
        console.error('获取系统消息失败:', error);
      }
    };

    // 格式化时间
    const formatDate = (dateStr) => {
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      const date = new Date(dateStr);
      return date.toLocaleString('zh-CN', options);
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
      goBack,
    };
  },
};
</script>

<style scoped>
/* 整体布局 */
.notification-page {
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

/* 消息列表 */
.notifications {
  margin-top: 16px;
}

/* 每条消息的容器 */
.notification-item {
  background-color: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
}

/* 消息时间 */
.notification-time {
  font-size: 12px;
  color: #888;
  margin-bottom: 8px;
}

/* 消息标题 */
.notification-title {
  font-size: 16px;
  color: #333;
  margin: 0 0 8px;
  font-weight: bold;
}

/* 消息内容 */
.notification-desc {
  font-size: 14px;
  color: #555;
  line-height: 1.5;
}
</style>