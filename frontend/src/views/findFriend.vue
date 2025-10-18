<template>
  <div class="whole-page">
    <!-- 搜索栏 -->
    <header class="header">
      <button class="back-button" @click="goBack">
        <van-icon name="arrow-left" size="18px" />
      </button>
    </header>
    <div class="search-bar">
      <div class="search-container">
        <input v-model="phoneNumber" class="search-input" type="text" placeholder="根据电话号码搜索你想要添加的好友"
          @keyup.enter="findUser" />
        <button class="search-button" @click="findUser">查找</button>
      </div>
    </div>

    <!-- 错误信息 -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <!-- 用户列表展示 -->
    <div class="friends-list">
      <!-- 显示查找到的用户 -->
      <div v-for="friend in filteredUsers" :key="friend.id" class="friend-item" @click="goToUserInfo(friend.id)">
        <img :src="friend.avatar" alt="头像" class="friend-avatar" />
        <span class="friend-nickname">{{ friend.nickname }}</span>
      </div>

      <!-- 如果没有找到匹配的好友，并且已进行过搜索 -->
      <div v-if="hasSearched && filteredUsers.length === 0 && !errorMessage" class="no-friends">
        您没有找到任何匹配的好友
      </div>
    </div>
  </div>
</template>

<script>
import { findUserByPhone } from '../service/friend';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    const phoneNumber = ref('');  // 用户输入的手机号
    const foundUser = ref(null); // 查找到的用户
    const errorMessage = ref('');  // 错误信息
    const selectedFriends = ref([]); // 存储选中的好友ID
    const hasSearched = ref(false); // 标记是否已经进行过搜索

    // 查找好友
    const findUser = async () => {
      hasSearched.value = true; // 标记为已进行搜索
      try {
        errorMessage.value = ''; // 清空错误信息
        const result = await findUserByPhone(phoneNumber.value);
        if (result && result.id) {
          console.log('result:', result);
          foundUser.value = result; // 更新用户数据
        } else {
          foundUser.value = null; // 没有匹配的好友
        }
      } catch (err) {
        // errorMessage.value = '查找失败：' + (err.response ? err.response.data.error : err.message);
        foundUser.value = null; // 出现错误时清空用户数据
      }
    };

    // 返回上一页
    const goBack = () => {
      router.back();
    };

    // 计算过滤后的用户列表（基于搜索框）
    const filteredUsers = computed(() => {
      if (!phoneNumber.value) {
        return [];  // 初始时，不显示任何用户
      }
      console.log('foundUser1:', foundUser.value);
      console.log('phoneNumber:', phoneNumber.value);
      if (foundUser.value && foundUser.value.phone.includes(phoneNumber.value)) {
        console.log('foundUser2:', foundUser.value);
        return [foundUser.value];
      }
      return [];
    });

    // 跳转到用户信息页面
    const goToUserInfo = (userId) => {
      router.push({ name: 'userInfo', query: { id: userId } });
    };

    return {
      phoneNumber,
      foundUser,
      errorMessage,
      selectedFriends,
      hasSearched,
      findUser,
      goBack,
      filteredUsers,
      goToUserInfo,
    };
  },
};
</script>


<style scoped>
/* 页面布局 */
.container {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  /* 灰色背景 */
  padding-top: 20px;
  /* 调整顶部空隙 */
}


/* 错误信息 */
.error-message {
  color: red;
  margin-top: 15px;
  font-size: 14px;
}

/* 好友列表样式 */
.friends-list {
  width: 90%;
  /* 设置为与搜索栏宽度一致 */
  display: flex;
  flex-direction: column;
  /* 列表纵向排列 */
  align-items: flex-start;
  padding: 16px 0;
  /* 不要加过多的内边距 */
}

/* 用户项样式 */
.friend-item {
  display: flex;
  align-items: center;
  background-color: #fff;
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 12px;
  width: 100%;
  /* 让每个用户项宽度和父容器一致 */
  box-sizing: border-box;
  cursor: pointer;
  /* 增加手型光标，表明可点击 */
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