<template>
  <div class="whole-page">
    <!-- 返回按钮 -->
    <div class="header">
      <span class="app-name">消息列表</span>
      <!-- + 按钮，右上角 -->
      <button class="add-button" @click="goTocreategroup">
        <van-icon name="plus" size="24px" />
      </button>
      <!-- 放大镜按钮，右上角 -->
      <button class="search-button" @click="goToFindFriend">
        <van-icon name="search" size="24px" />
      </button>
    </div>

    <div class="notification-section">
      <van-cell-group>
        <!-- System Notification -->
        <van-cell title="系统消息" :label="state.latestSystemMessage?.title || '暂无消息'"
          :value="state.latestSystemMessage?.time || '--:--'" icon="notes-o" clickable
          @click="readSystemNotification(state.latestSystemMessage?.id)"></van-cell>

        <!-- Order Notification -->
        <van-cell title="订单消息" :label="state.latestOrderMessage?.title || '暂无消息'"
          :value="state.latestOrderMessage?.time || '--:--'" icon="notes-o" clickable
          @click="readOrderNotification(state.latestOrderMessage?.id)"></van-cell>

        <!-- Unread Notifications -->
        <van-cell title="未读系统消息" label="总计未读消息数量" :value="`${state.unreadSysCount} 条`" icon="envelop-o"></van-cell>

        <!-- Unread Notifications -->
        <van-cell title="未读订单消息" label="总计未读消息数量" :value="`${state.unreadOrderCount} 条`" icon="envelop-o"></van-cell>
      </van-cell-group>
    </div>

    <!-- 中间栏切换群聊和亲友列表 -->
    <div class="tab-bar">
      <div class="tab-item" :class="{ active: viewMode.mode === 'groups' }" @click="setViewMode('groups')">
        群聊
      </div>
      <div class="tab-item" :class="{ active: viewMode.mode === 'friends' }" @click="setViewMode('friends')">
        亲友
      </div>
    </div>

    <!-- 群聊列表展示 -->
    <div v-if="viewMode.mode === 'groups'" class="group-chats">
      <div v-if="groups.length > 0 && !groups[0].message">
        <div v-for="group in groups" :key="group.id" class="group-item" @click="readGroupNotification(group)">
          <!-- 头像和未读消息 -->
          <div class="group-avatar-container">
            <img v-if="group.image" :src="group.image" alt="Group" class="group-avatar" />
            <div v-if="group.unread_count > 0" class="group-unread">
              {{ formatUnreadCount(group.unread_count) }}
            </div>
          </div>
          <div class="group-info">
            <h4>{{ group.name }}</h4>
            <p>{{ group.last_message ? truncateMessage(group.last_message.content) : '暂无消息' }}</p>
          </div>
          <!-- 时间放置在右上角 -->
          <div class="group-time">
            {{ group.last_message ? formatTimestamp(group.last_message.timestamp) : '--:--' }}
          </div>
        </div>
      </div>
      <div v-else>
        <div class="no-content">
          <van-icon name="question-o" size="36px" color="#ff9f00" />
          <p class="no-content-text">{{ groups[0]?.message || '暂无群聊' }}</p>
        </div>
      </div>
    </div>

    <!-- 亲友列表展示 -->
    <div v-if="viewMode.mode === 'friends'" class="friends-list">
      <div v-if="friends.length > 0 && !friends[0].message">
        <div v-for="friend in friends" :key="friend.id" class="friend-item" @click="readFriendNotification(friend)">
          <!-- 头像和未读消息 -->
          <div class="friend-avatar-container">
            <img :src="friend.avatar" alt="avatar" class="friend-avatar" />
            <div v-if="friend.unread_count > 0" class="friend-unread">
              {{ formatUnreadCount(friend.unread_count) }}
            </div>
          </div>
          <div class="friend-info">
            <h4 class="friend-nickname">{{ friend.nickname }}</h4>
            <p class="friend-message">{{ friend.last_message ? truncateMessage(friend.last_message.content) : '暂无消息' }}
            </p>
          </div>
          <!-- 时间 -->
          <span class="friend-time">{{ friend.last_message ? formatTimestamp(friend.last_message.timestamp) : '--:--'
            }}</span>
        </div>
      </div>
      <div v-else>
        <div class="no-content">
          <van-icon name="question-o" size="36px" color="#ff9f00" />
          <p class="no-content-text">{{ friends[0]?.message || '暂无亲友' }}</p>
        </div>
      </div>
    </div>

    <!-- 固定底部导航栏 -->
    <bottomTabBar v-model="active" />
  </div>
</template>

<script setup>
/* eslint-disable */
import { reactive, onMounted, ref, onBeforeUnmount } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import {
  registerGroupUnreadHandler,
  registerPrivateUnreadHandler,
  markGroupMessagesAsRead,
  markPrivateMessagesAsRead,
} from '../service/Notifications'; // 确保路径正确
import{
  connectSocket,
  registerPrivateMessageHandler,
  registerGroupMessageHandler,
} from '../service/chatService'; // 确保路径正确
import {
  getLatestNotification,
  getUnreadNotificationsCount,
  updateAllNotificationStatus,
} from '../service/sysNotification'; // System notification API
import {
  getLatestOrderNotification,
  updateAllOrderNotificationsStatus,
  getUnreadOrderNotificationsCount,
} from '../service/orderNotification'; // Order notification API
import { fetchGroupChats } from '../service/group'; // 群聊数据获取
import { fetchFriends } from '../service/friend'; // 亲友数据获取
import bottomTabBar from '@/components/bottomTabBar.vue';


// import { v4 as uuidv4 } from 'uuid'; // 确保已安装: npm install uuid

const router = useRouter();
const route = useRoute();
const token = localStorage.getItem('token');

// 辅助函数：截断过长的消息并添加省略号 
const truncateMessage = (message, maxLength = 10) => { 
  if (message.length > maxLength) {
    return message.substring(0, maxLength) + '...';
  }
  return message;
};

// 辅助函数：处理未读消息数量的显示
const formatUnreadCount = (unreadCount) => {
  if (unreadCount > 99) {
    return '99+';
  }
  return unreadCount;
};

const state = reactive({
  latestSystemMessage: null,
  latestOrderMessage: null,
  unreadSysCount: 0,
  unreadOrderCount: 0,
  loading: false, // 添加加载状态
});

const groups = reactive([]);  // 群聊数组
const friends = reactive([]); // 亲友数组
const active = ref(3); // 用于 van-tabbar 的 v-model
const viewMode = reactive({
  mode: 'groups', // 默认显示群聊
});

// 切换当前显示模式
const setViewMode = (mode) => {
  if (viewMode.mode !== mode) {
    viewMode.mode = mode;
    console.log(`Switched to ${mode}`);
    fetchGroupsAndFriends(); // 每次切换时都获取最新的群聊和亲友数据
  }
};

// 跳转到查找亲友页面
const goToFindFriend = () => {
  router.push({ name: 'findFriend' }); // 跳转到findFriend路由
};

// 更新系统未读消息数量
const updateGroupUnreadCount = (data) => {
  console.log('Group unread message count:', data);
  state.unreadSysCount = data.unread_count || 0; // 更新系统未读消息数
};

// 更新通知未读消息数量
const updatePrivateUnreadCount = (data) => {
  console.log('Private unread message count:', data);
  state.unreadOrderCount = data.unread_count || 0; // 更新通知未读消息数
};

// 获取群聊与亲友数据
const fetchGroupsAndFriends = async () => {
  state.loading = true;
  console.log('Fetching groups and friends...');
  try {
    const fetchedGroups = await fetchGroupChats();
    const fetchedFriends = await fetchFriends();
    console.log('Groups:', fetchedGroups);

    // 确保 fetchedGroups 是有效数组且不为空
    if (fetchedGroups && fetchedGroups.groups.length > 0) {
      // 清空 groups 数组并将 fetchedGroups 中的每个项推入
      groups.length = 0; // 清空 groups 数组
      // 初始化每个群组的 unread_count
      const initializedGroups = fetchedGroups.groups.map(group => ({
        ...group,
        unread_count: group.unread_count || 0, // 假设后端有提供 unread_count
      }));
      groups.push(...initializedGroups);
      // console.log('Groups:', groups);
      // console.log('GroupsMessages:', groups[0].last_message);
    } else {
      console.log('No groups found');
    }

    // 处理亲友数据
    if (fetchedFriends && Array.isArray(fetchedFriends) && fetchedFriends.length > 0) {
      // 清空 friends 数组并推入新的数据
      friends.length = 0;
      // 初始化每个亲友的 unread_count
      const initializedFriends = fetchedFriends.map(friend => ({
        ...friend,
        unread_count: friend.unread_count || 0, // 假设后端有提供 unread_count
      }));
      friends.push(...initializedFriends);
      // console.log("friends:", friends);
      // console.log("friendsMessages:", friends[0]);
    } else {
      console.log('No friends found');
    }

  } catch (error) {
    console.error('Error fetching groups and friends:', error);
  } finally {
    state.loading = false;
  }
};

// 获取系统和订单通知
const fetchNotifications = async () => {
  try {
    const [latestSystemMessage, latestOrderMessage, unreadSysCount, unreadOrderCount] = await Promise.all([
      getLatestNotification(),
      getLatestOrderNotification(),
      getUnreadNotificationsCount(),
      getUnreadOrderNotificationsCount(),
    ]);

    if (latestSystemMessage) {
      state.latestSystemMessage = {
        id: latestSystemMessage.id || 'N/A',
        title: latestSystemMessage.title || '暂无标题',
        time: formatTimestamp(latestSystemMessage.created_at) || '--:--',
      };
    }
    if (latestOrderMessage) {
      state.latestOrderMessage = {
        id: latestOrderMessage.id || 'N/A',
        title: latestOrderMessage.title || '暂无标题',
        time: formatTimestamp(latestOrderMessage.created_at) || '--:--',
      };
    }
    state.unreadSysCount = unreadSysCount || 0;
    state.unreadOrderCount = unreadOrderCount || 0;
  } catch (error) {
    console.error('Error fetching notifications:', error);
  }
};

// 更新系统消息为已读并跳转

const readSystemNotification = async () => {
  if (!state.latestSystemMessage) {
    console.log('系统消息为空');
    return;
  }
  try {
    // 更新所有系统消息为已读状态
    await updateAllNotificationStatus();
    // 跳转到系统消息详情页面
    goTo('/sysNotificationDetail');
  } catch (error) {
    console.error('Error reading system notification:', error);
  }
};


// 更新订单消息为已读并跳转
const readOrderNotification = async (id) => {
  if (!state.latestOrderMessage) {
    console.log('订单消息为空');
    return;
  }
  try {
    // 如果 id 存在，则更新所有订单消息的已读状态
    if (id) {
      await updateAllOrderNotificationsStatus();
    }
    // 跳转到订单详情页面
    goTo('/orderNotificationDetail');
  } catch (error) {
    console.error('Error reading order notification:', error);
  }
};


// 点击群聊消息，跳转到聊天页面并标记已读
const readGroupNotification = async (group) => {
  console.log('Reading group notification:', group.id);
  try {

    console.log('markGroupMessagesAsRead:', group.id);
    markGroupMessagesAsRead(token, group.id); // 标记群聊消息为已读
    // 重置该群组的 unread_count
    const targetGroup = groups.find(g => g.id === group.id);
    if (targetGroup) {
      targetGroup.unread_count = 0;
    }
    router.push({ path: '/chatPage', query: { type: 'group', id: group.id } }); // 跳转到群聊聊天页面
  } catch (error) {
    console.error('Error marking group notification as read:', error);
  }
};

// 点击亲友消息，跳转到聊天页面并标记已读
const readFriendNotification = async (friend) => {
  console.log('Reading friend notification:', friend);
  try {
    markPrivateMessagesAsRead(token, friend.id); // 标记私聊消息为已读
    // 重置该亲友的 unread_count
    const targetFriend = friends.find(f => f.id === friend.id);
    if (targetFriend) {
      targetFriend.unread_count = 0;
    }
    router.push({ path: '/chatPage', query: { type: 'friend', id: friend.id } }); // 跳转到亲友聊天页面
  } catch (error) {
    console.error('Error marking friend notification as read:', error);
  }
};

// 处理私聊消息
const handlePrivateMessage = (message) => {
  // 假设 message 包含 sender_id, content, timestamp
  // console.log('Private message:', message, message.sender_id, message.content, message.timestamp);
  if (message && message.sender_id && message.content && message.timestamp) {
    // 找到对应的亲友
    const friend = friends.find(f => f.id === message.sender_id);
    if (friend) {
      friend.last_message = message;
      console.log('friendMessage:', friend.last_message);
      //更新未读计数
      friend.unread_count = (friend.unread_count || 0) + 1;
      // state.unreadOrderCount = (state.unreadOrderCount || 0) + 1; // 也更新总未读订单消息数
    }
  }
};

// 处理群聊消息
const handleGroupMessage = (message) => {
  // 假设 message 包含 group_id, content, timestamp
  if (message && message.group_id && message.content && message.timestamp) {
    // 找到对应的群组
    const group = groups.find(g => g.id === message.group_id);
    if (group) {
      group.last_message = message;
      //更新未读计数
      group.unread_count = (group.unread_count || 0) + 1;
      // state.unreadSysCount = (state.unreadSysCount || 0) + 1; // 也更新总未读系统消息数
    }
  }
};

// 辅助函数：格式化时间为 YYYY-MM-DD HH:MM
const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp);
  const year = date.getFullYear();
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');
  const hours = date.getHours().toString().padStart(2, '0');
  const minutes = date.getMinutes().toString().padStart(2, '0');
  return `${year}-${month}-${day} ${hours}:${minutes}`;
};


onMounted(() => {
  if (token) {
    registerGroupUnreadHandler(updateGroupUnreadCount);  // 注册群聊未读消息处理器
    registerPrivateUnreadHandler(updatePrivateUnreadCount); // 注册私聊未读消息处理器

    const { type } = route.query || {};  // 确保 query 存在
    if (type === "private") {
      viewMode.mode = 'friends';
    }

    // 连接WebSocket
    connectSocket(token);

    // 注册消息事件监听器
    registerPrivateMessageHandler(handlePrivateMessage);
    registerGroupMessageHandler(handleGroupMessage);

    fetchNotifications();
    fetchGroupsAndFriends();
  } else {
    console.error('No token found. Please log in.');
  }
});


// 跳转函数
const goTo = (path) => {
  router.push(path);
};

// 跳转到创建群组页面
const goTocreategroup = () => {
  router.push({ name: 'creategroup' });
};
</script>

<style scoped>
.header h2 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.back-button {
  position: absolute;
  top: 50%;
  left: 16px;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #333;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.back-button:hover {
  color: #007aff;
}

/* + 按钮样式 */
.add-button {
  position: absolute;
  top: 50%;
  right: 16px;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 24px;
  color: #FFA500;
}

.add-button:hover {
  color: #ff8c00;
}

/* 搜索按钮的位置 */
.search-button {
  position: absolute;
  top: 10px;
  left: 16px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 24px;
  color: #f4a261;
  width: 50px;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.search-button:hover {
  color: #f47011;
}

/* 群聊和亲友列表的公共样式 */
.group-chats,
.friends-list {
  margin: 0;
  padding: 0;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 群聊项样式 */
.group-item,
.friend-item {
  display: flex;
  align-items: center;
  padding: 10px;
  margin-bottom: 10px;
  background-color: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  position: relative;
  /* 为未读消息和时间提供定位空间 */
}

/* 群聊项与好友项头像 */
.group-avatar,
.friend-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 15px;
}

/* 头像容器样式 */
.group-avatar-container,
.friend-avatar-container {
  position: relative;
  /* 为未读消息提供定位空间 */
  display: inline-block;
  /* 使容器能够包含绝对定位的元素 */
}

/* 未读消息的通用样式 */
.group-unread,
.friend-unread {
  position: absolute;
  top: -5px;
  /* 根据需要调整 */
  right: -5px;
  /* 根据需要调整 */
  background-color: #ff4500;
  color: #fff;
  border-radius: 50%;
  width: 20px;
  /* 根据需要调整 */
  height: 20px;
  /* 根据需要调整 */
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 12px;
}


/* 头像容器样式 */
.group-avatar-container,
.friend-avatar-container {
  position: relative;
  /* 为未读消息提供定位空间 */
  display: inline-block;
  /* 使容器能够包含绝对定位的元素 */
}

/* 未读消息的通用样式 */
.group-unread,
.friend-unread {
  position: absolute;
  top: -5px;
  /* 根据需要调整 */
  right: -5px;
  /* 根据需要调整 */
  background-color: #ff4500;
  color: #fff;
  border-radius: 50%;
  width: 20px;
  /* 根据需要调整 */
  height: 20px;
  /* 根据需要调整 */
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 12px;
}


.group-info h4,
.friend-info h4 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.group-info p,
.friend-info p {
  font-size: 14px;
  color: #666;
  margin: 5px 0;
}

.group-info span,
.friend-info span {
  font-size: 12px;
  color: #999;
}

/* 统一时间和未读消息的样式 */
.friend-time,
.group-time {
  position: absolute;
  top: 5px;
  /* 距离顶部 5px */
  right: 10px;
  /* 距离右边 10px */
  font-size: 12px;
  color: #aaa;
}

.friend-unread,
.group-unread {
  position: absolute;
  bottom: 5px;
  /* 距离底部 5px */
  left: 10px;
  /* 距离左边 10px */
  background-color: #ff4500;
  color: #fff;
  border-radius: 12px;
  padding: 2px 6px;
  font-size: 12px;
  font-weight: bold;
}

/* 右下角的未读消息标记 */
.group-item p,
.friend-item p {
  font-size: 14px;
  color: #999;
  text-align: center;
}

/* 没有群聊或亲友时的文本 */
.no-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background-color: #f8f8f8;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.no-content .van-icon {
  margin-bottom: 10px;
}

.no-content-text {
  font-size: 16px;
  color: #888;
  font-weight: 500;
}

/* 中间栏样式 */
.tab-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #fff;
  border-top: 1px solid #ddd;
  border-bottom: 1px solid #ddd;
  margin: 0;
  width: 100%;
}

/* 每个选项的样式 */
.tab-item {
  flex: 1;
  padding: 14px 0;
  font-size: 16px;
  font-weight: 500;
  color: #666;
  cursor: pointer;
  text-align: center;
  transition: background-color 0.3s ease;
}

.tab-item.active {
  background-color: #FFA500;
  color: #fff;
  font-weight: 600;
}

.tab-item:hover {
  background-color: #f4a261;
  color: #fff;
}
</style>
