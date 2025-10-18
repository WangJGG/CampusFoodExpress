<template>
  <div class="whole-page">
    <!-- 返回按钮和标题 -->
    <div class="header">
      <button class="back-button" @click="goBack">
        <van-icon name="arrow-left" size="18px" />
      </button>
      <div class="title">
        <span class="app-name">选择好友创建群聊</span>
      </div>
    </div>
    <div class="search-bar">
      <div class="search-container">
        <input type="text" v-model="searchQuery" placeholder="搜索好友" class="search-input" />
        <button class="search-button">搜索</button>
      </div>
    </div>

    <button class="complete-btn" :class="{ active: selectedFriends.length >= 1 }" @click="createGroup">
      确认
    </button>

    <!-- 好友列表 -->
    <div class="friends-list">
      <!-- 当没有好友时显示提示信息 -->
      <div v-if="friends.length === 0" class="no-friends">
        您还没有亲友，快去添加吧！
      </div>

      <!-- 显示好友信息 -->
      <div v-for="friend in filteredFriends" :key="friend.id" class="friend-item">
        <input type="checkbox" :id="friend.id" class="friend-checkbox" v-model="selectedFriends" :value="friend.id" />
        <img :src="friend.avatar" alt="avatar" class="friend-avatar" />
        <span class="friend-nickname">{{ friend.nickname }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router'; // 引入 useRouter 以便实现页面跳转
import { createGroup } from '../service/group';  // 引入创建群聊的服务
import { fetchFriends } from '../service/friend'; // 引入获取亲友数据的服务
import { ElMessage } from 'element-plus'

export default {
  setup() {
    const router = useRouter();  // 获取路由实例
    const friends = ref([]);  // 存储好友列表
    const selectedFriends = ref([]);  // 存储选中的好友ID
    const searchQuery = ref('');  // 存储搜索框的内容
    const state = ref({ loading: false }); // 控制加载状态

    // 获取群聊和亲友数据
    const fetchGroupsAndFriends = async () => {
      state.value.loading = true;
      console.log('Fetching groups and friends...');
      try {
        const fetchedFriends = await fetchFriends(); // 获取亲友数据
        console.log('Fetched friends:', fetchedFriends);

        // 确保 fetchedFriends 是有效数组且不为空
        if (fetchedFriends && fetchedFriends.length > 0) {
          friends.value = [...fetchedFriends];  // 更新好友列表
        } else {
          friends.value = []; // 如果没有好友，设置为空数组
          console.log('No friends found');
        }
      } catch (error) {
        console.error('Error fetching friends:', error);
      } finally {
        state.value.loading = false;
      }
    };

    // 创建群聊
    const handleCreateGroup = async () => {
      try {
        console.log(selectedFriends.value[0]);
        if(selectedFriends.value.length==1){
          router.push({ path: '/chatPage', query: { type: 'friend', id: selectedFriends.value[0] } }); // 跳转到亲友聊天页面
          ElMessage.warning('双人的干饭小群已经有了哦😋');
          return;
        }
        const { group, owner } = await createGroup(selectedFriends.value);
        console.log('人员列表:', selectedFriends.value, '人数：', selectedFriends.value.length);
        console.log('群聊创建成功:', group);
        console.log('群主信息:', owner);
        ElMessage.success('群聊创建成功!');
        // 跳转到新创建的群聊页面

        router.push({ path: '/friends' }); // 跳转到群聊聊天页面
      } catch (error) {
        console.error('创建群聊失败:', error.message);
        ElMessage.error(error.message);
      }
    };

    // 返回上一页
    const goBack = () => {
      router.back();  // 使用 Vue Router 的 back 方法返回上一页
    };

    // 计算过滤后的好友列表
    const filteredFriends = computed(() => {
      if (!searchQuery.value) {
        return friends.value;
      }
      return friends.value.filter(friend =>
        friend.nickname.includes(searchQuery.value)
      );
    });

    // 初始化时加载好友数据
    onMounted(() => {
      fetchGroupsAndFriends(); // 获取群聊和亲友数据
    });

    return {
      friends,
      selectedFriends,
      searchQuery,
      createGroup: handleCreateGroup,
      goBack,
      filteredFriends,
      loading: state.value.loading,
    };
  }
};
</script>

<style scoped>
/* 完成按钮样式 */
.complete-btn {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  background-color: #ddd;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.3s;
}

.complete-btn.active {
  background-color: #FFA500;
  cursor: pointer;
}

.complete-btn:disabled {
  background-color: #b0b0b0;
  cursor: not-allowed;
}

.friends-list {
  padding: 16px;
}

.friend-item {
  display: block;
  background-color: #fff;
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.friend-checkbox {
  width: 24px;
  height: 24px;
}

.friend-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.friend-nickname {
  font-size: 14px;
}

.no-friends {
  text-align: center;
  font-size: 16px;
  color: #999;
  padding: 20px;
  background-color: #f0f0f0;
  border-radius: 8px;
}
</style>
