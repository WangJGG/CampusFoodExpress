<template>
  <div class="whole-page">
    <div class="header">
      <span class="app-name">个人主页</span>
    </div>
    <div class="user-info">
      <div class="info">
        <img :src="state.user.avatar" alt="User Avatar" />
        <div class="user-desc">
          <span>账号：{{ state.user.phone }}</span>
          <span>昵称：{{ state.user.nickname }}</span>
          <span class="name">个性签名：{{ state.user.bio }}</span>
          <span>账号类型：{{ state.user.role }}</span>
          <!-- 右侧添加 UserStatus 组件 -->
          <UserStatus class="user-status-component" />
        </div>
      </div>
    </div>
    <div class="function-list">
      <div class="function-item" @click="goTo('/userProfile')">
        <font-awesome-icon icon="user" class="function-icon" />
        <span>个人信息</span>
      </div>
      <div class="function-item" @click="goTo('/userPassword')">
        <font-awesome-icon icon="lock" class="function-icon" />
        <span>密码修改</span>
      </div>
      <div class="function-item" @click="goTo('/userAuthentication')">
        <font-awesome-icon icon="chart-bar" class="function-icon" />
        <span>学生认证</span>
      </div>
      <div class="function-item" @click="goTo('/userLikes')">
        <font-awesome-icon icon="gift" class="function-icon" />
        <span>我的收藏</span>
      </div>
      <!-- 新增的功能项 -->
      <div class="function-item" @click="goTo('/userComments')">
        <font-awesome-icon icon="comment" class="function-icon" />
        <span>我的评论</span>
      </div>
      <div class="function-item" @click="goTo('/restaurantTrack')">
        <font-awesome-icon icon="paw" class="function-icon" />
        <span>我的足迹</span>
      </div>
      <div class="function-item" @click="goTo('/userAccusation')">
        <font-awesome-icon icon="phone" class="function-icon" />
        <span>举报中心</span>
      </div>
    </div>
    <div class="logout-button">
      <a-button status="danger" @click="logout">退出登录</a-button>
    </div>
    <!-- 固定底部导航栏 -->
    <bottomTabBar v-model="active" />
  </div>
</template>


<script setup>
import { reactive, onMounted, ref } from "vue";
import { getUserInfo, userLogout } from "@/service/user";
import { useRouter } from "vue-router";
import { disconnectSocket } from "@/service/chatService";
import bottomTabBar from "@/components/bottomTabBar.vue";
const router = useRouter();
//userStatus
import UserStatus from "@/components/userStatus.vue";

const active = ref(4);

const state = reactive({
  user: {},
  loading: true,
});

onMounted(async () => {
  const response = await getUserInfo();
  state.user = response.data;
  state.loading = false;
});

const logout = async () => {
  const response = await userLogout();
  if (response.status === 200) {
    disconnectSocket(localStorage.getItem("token"));
    localStorage.removeItem("token");
    router.push("/login");
  } else {
    console.log(response);
  }
};

const goTo = (r, query) => {
  router.push({ path: r, query: query || {} });
};
</script>

<style lang="less" scoped>
@import "../common/style/mixin";

.user-header {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 10000;
  .fj();
  .wh(100%, 44px);
  line-height: 44px;
  padding: 0 10px;
  .boxSizing();
  color: #252525;
  background: #fff;
  border-bottom: 1px solid #dcdcdc;

  .user-name {
    font-size: 14px;
  }
}

.user-info {
  width: 94%;
  margin: 10px auto;
  height: 140px;
  background: #fdfbf2;
  box-shadow: 0 2px 5px #151312;
  border-radius: 6px;
  overflow: hidden;

  .info {
    position: relative;
    display: flex;
    width: 100%;
    height: 100%;
    padding: 25px 20px;
    .boxSizing();

    img {
      .wh(60px, 60px);
      border-radius: 50%;
      margin-top: 4px;
    }

    .user-desc {
      margin-left: 10px;
      position: relative;
      flex: 1;
      display: flex;
      flex-direction: column;
      line-height: 20px;
      font-size: 14px;
      color: #000;

      span {
        color: #000;
        font-size: 14px;
        padding: 2px 0;
      }

      .user-status-component {
        position: absolute;
        top: 0;
        right: 0;
        margin-right: 10px;
      }
    }
  }
}

.function-list {
  padding: 3%;
  background-color: #f8f8f8;
  margin-top: 20px;

  .function-item {
    display: flex;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #e0e0e0;
    cursor: pointer;

    &:last-child {
      border-bottom: none;
    }

    .function-icon {
      font-size: 24px;
      color: #f0d078;
      margin-right: 2%;
    }

    span {
      font-size: 14px;
      color: #333;
      flex: 1;
    }
  }
}

.logout-button {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  padding-bottom: 20px;
}
</style>