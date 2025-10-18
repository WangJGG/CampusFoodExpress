<template>
  <div>
    <!-- 返回按钮和标题 -->
    <div class="header">
      <button class="back-button" @click="goBack">
        <van-icon name="arrow-left" size="24px" />
      </button>
      <h2>选择好友加入群聊</h2>
      <button class="complete-btn" :class="{ active: selectedFriends.length >= 1 }" @click="createGroup"
        :disabled="selectedFriends.length < 1">
        完成
      </button>
    </div>

    <!-- 搜索框 -->
    <div class="search-bar">
      <input type="text" v-model="searchQuery" placeholder="搜索好友" class="search-input" />
    </div>

    <!-- 好友列表 -->
    <div class="friends-list">
      <!-- 当没有好友时显示提示信息 -->
      <div v-if="friends.length === 0" class="no-friends">
        您还没有亲友，快去添加吧！
      </div>

      <!-- 显示好友信息 -->
      <div v-for="friend in filteredFriends" :key="friend.id" class="friend-item">
        <input type="checkbox" :id="friend.id" class="friend-checkbox" v-model="selectedFriends" :value="friend.id"
          :disabled="isMemberAlready(friend.id)" />
        <img :src="friend.avatar" alt="avatar" class="friend-avatar" />
        <span class="friend-nickname">{{ friend.nickname }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from "vue";
import { useRouter, useRoute } from "vue-router"; // 引入 useRouter 以便实现页面跳转
import { addMember } from "../service/group"; // 引入创建群聊的服务
import { fetchFriends } from "../service/friend"; // 引入获取亲友数据的服务
import { ElMessage } from 'element-plus'

export default {
  setup() {
    const router = useRouter(); // 获取路由实例
    const friends = ref([]); // 存储好友列表
    const selectedFriends = ref([]); // 存储选中的好友ID
    const searchQuery = ref(""); // 存储搜索框的内容
    const state = ref({ loading: false }); // 控制加载状态
    const route = useRoute();
    const memberList = route.query.memberList
      ? JSON.parse(route.query.memberList)
      : [];

    const isMemberAlready = (friendId) => {
      // console.log(memberList[0]);
      // 检查 memberList 中的对象，看看是否有 user_id 和 friendId 相同的项
      return memberList.some((member) => member.user_id === friendId);
    };

    // 获取群聊和亲友数据
    const fetchGroupsAndFriends = async () => {
      state.value.loading = true;
      console.log("Fetching groups and friends...");
      try {
        const fetchedFriends = await fetchFriends(); // 获取亲友数据
        console.log("Fetched friends:", fetchedFriends);

        // 确保 fetchedFriends 是有效数组且不为空
        if (fetchedFriends && fetchedFriends.length > 0) {
          friends.value = [...fetchedFriends]; // 更新好友列表
        } else {
          friends.value = []; // 如果没有好友，设置为空数组
          console.log("No friends found");
        }
      } catch (error) {
        console.error("Error fetching friends:", error);
      } finally {
        state.value.loading = false;
      }
    };

    const handleAddMember = async () => {
      console.log("groupid: ", route.query.id);
      try {
        // 清空上次的消息
        if (selectedFriends.value.length === 0) {
          ElMessage.error("请至少选择一个好友");
          return;
        }

        // 遍历选中的好友ID，逐一调用 addMember
        const promises = selectedFriends.value.map((userId) => {
          return addMember(route.query.id, userId);
        });

        // 使用 Promise.all 并行处理所有成员添加
        const members = await Promise.all(promises);

        // 成功后弹出成功消息
        ElMessage.success(`成功添加了 ${members.length} 个成员。`);
        goBack();
      } catch (error) {
        // 错误时弹出错误消息
        ElMessage.error(error.message || "添加成员失败");
      }
    };

    // 返回上一页
    const goBack = () => {
      router.back(); // 使用 Vue Router 的 back 方法返回上一页
    };

    // 计算过滤后的好友列表
    const filteredFriends = computed(() => {
      if (!searchQuery.value) {
        return friends.value;
      }
      return friends.value.filter((friend) =>
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
      createGroup: handleAddMember,
      isMemberAlready,
      goBack,
      filteredFriends,
      loading: state.value.loading,
    };
  },
};
</script>

<style scoped>
/* 样式保持不变 */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background-color: #fff;
  border-bottom: 1px solid #ddd;
}

.back-button {
  background: none;
  border: none;
  color: #333;
  font-size: 14px;
  cursor: pointer;
}

.complete-btn {
  background-color: #ddd;
  color: #fff;
  padding: 10px 20px;
  border: none;
  cursor: not-allowed;
  border-radius: 20px;
  font-size: 16px;
}

.complete-btn.active {
  background-color: #ffa500;
  cursor: pointer;
}

.search-bar {
  padding: 10px;
  background-color: #f5f5f5;
}

.search-input {
  width: 100%;
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
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