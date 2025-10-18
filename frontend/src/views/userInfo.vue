<template>
  <div class="user-info">
    <header class="header">
      <button class="back-button" @click="router.back()">
        <van-icon name="arrow-left" size="18px" />
      </button>
      <span class="app-name">用户详情</span>
    </header>

    <div class="user-info-container">
      <!-- 用户信息盒子 -->
      <div class="user-info-box">
        <div class="user-avatar">
          <img :src="user.avatar" alt="头像" class="avatar-img" />
        </div>
        <div class="status-box">
          <div class="status" v-if="status.isActive">
            {{ statusList[status.statusId] }}
          </div>
          <div class="status" v-else>暂无状态</div>
          <!-- <div class="content">{{ status.content }}</div> -->
        </div>
      </div>

      <!-- 用户详情部分 -->
      <div class="user-details">
        <p><strong>昵称:</strong> {{ user.nickname }}</p>
        <p><strong>账号:</strong> {{ user.phone }}</p>
        <p><strong>签名:</strong> {{ user.bio }}</p>
        <p><strong>认证状态:</strong> {{ user.auth_status }}</p>
        <p>
          <strong>账号状态:</strong> {{ user.is_forbidden ? "已封禁" : "正常" }}
        </p>
      </div>
    </div>

    <!-- 好友操作按钮 -->
    <div class="friend-action">
      <a-button v-if="isFriend" type="danger" @click="deleteFriendHandler" class="action-button delete-button">
        删除好友
      </a-button>
      <a-button v-else type="primary" @click="addFriendHandler" class="action-button add-button">
        添加好友
      </a-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { getUserDetails, addFriend, deleteFriend } from "@/service/friends";

// 路由参数和用户数据
const route = useRoute();
const router = useRouter();
const userId = route.query.id;
const user = ref({});
const isFriend = ref(false); // 是否是好友
const status = ref({
  isActive: false,
  statusId: null,
  content: "",
});

// 状态列表
const statusList = ["😋在干饭", "😢饿饿", "🥣等饭吃"];

// 获取用户信息和状态
onMounted(async () => {
  try {
    const response = await getUserDetails(userId);
    user.value = response.data; // 用户信息
    isFriend.value = response.data.is_friend; // 好友关系
    const userStatus = response.data.status;

    // 设置状态信息
    if (userStatus && userStatus.is_active) {
      status.value.isActive = true;
      status.value.statusId = userStatus.status_id;
      status.value.content = userStatus.content;
    }
  } catch (error) {
    console.error("获取用户信息失败", error);
  }
});

// 添加好友逻辑
const addFriendHandler = async () => {
  try {
    await addFriend(userId);
    isFriend.value = true;
    alert("好友添加成功");
  } catch (error) {
    console.error("添加好友失败", error);
    alert("添加好友失败，请稍后重试");
  }
};

// 删除好友逻辑
const deleteFriendHandler = async () => {
  try {
    await deleteFriend(userId);
    isFriend.value = false;
    router.push({
      path: "/friends",
      query: {
        type: 'private',
      },
    })
    alert("好友删除成功");
  } catch (error) {
    console.error("删除好友失败", error);
    alert("删除好友失败，请稍后重试");
  }
};
</script>

<style scoped>
.user-info {
  box-sizing: border-box;
  padding: 20px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  position: relative; /* 为子元素的绝对定位提供参考 */
}

/* .back-button {
  margin-bottom: 10px;
  background: #ffd700;
  border-color: #ffd700;
  color: white;
  font-weight: bold;
  transition: background 0.3s ease;
} */

/* .back-button:hover {
  background: #f6a665;
  border-color: #f6a665;
} */

.user-info-box {
  display: flex;
  flex-direction: column;
  /* 改为垂直排列 */
  align-items: center;
  /* 垂直居中 */
  gap: 20px;
}

.user-avatar {
  margin-bottom: 20px;
  /* 调整头像与状态盒子的间距 */
}

.avatar-img {
  max-width: 100px;
  max-height: 100px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.status-box {
  display: flex;
  flex-direction: column;
  /* 垂直排列状态和内容 */
  align-items: center;
  /* 居中对齐 */
  gap: 10px;
  padding: 15px;
}

.status,
.content {
  padding: 10px 20px;
  background-color: #ffd700;
  border-radius: 20px;
  color: white;
  font-weight: bold;
  max-width: 300px;
  text-align: center;
  word-wrap: break-word;
  box-sizing: border-box;
  max-height: 100px;
  /* 设置最大高度 */
  overflow-y: auto;
  /* 添加垂直滚动条 */
  scrollbar-width: thin;
  /* 针对现代浏览器，设置滚动条宽度 */
  scrollbar-color: rgba(0, 0, 0, 0.3) transparent;
  /* 滚动条颜色 */
}

/* .status {
  background-color: #f47c3c;
} */

.content {
  background-color: #fee200;
}

.user-details {
  text-align: center;
  /* 居中显示用户详细信息 */
  margin-top: 20px;
}

.user-details p {
  margin-bottom: 10px;
  font-size: 16px;
  color: #333;
}

.friend-action {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.action-button {
  width: 100%;
  max-width: 200px;
  border-radius: 8px;
  font-weight: bold;
  padding: 10px;
}

.add-button {
  background: #ffd700;
  border-color: #ffd700;
  color: white;
  transition: background 0.3s ease;
}

.add-button:hover {
  background: #f6a665;
  border-color: #f6a665;
}

.delete-button {
  background: #f6a665;
  border-color: #f6a665;
  color: white;
  transition: background 0.3s ease;
}

.delete-button:hover {
  background: #ffd700;
  border-color: #ffd700;
}

.user-info-container {
  box-sizing: border-box;
  padding: 20px;
  background: linear-gradient(to bottom,
      rgba(246, 211, 101, 0.8),
      rgba(255, 215, 0, 0.5));
  /* 背景样式 */
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  /* 垂直排列 */
  gap: 20px;
  align-items: center;
  /* 居中内容 */
}
</style>
