<template>
  <div class="user-box">
    <s-header :name="'我的'" />
    <div class="user-info">
      <div class="info">
        <img :src="state.user.avatar" alt="User Avatar" class="profile-img" />
        <div class="user-desc">
          <span class="account-number">{{ state.user.phone }}</span>
          <span class="account-type">{{ state.user.role }}</span>
        </div>
      </div>
    </div>
    <div class="function-list">
      <div class="function-item" @click="goTo('/userAcount')">
        <font-awesome-icon icon="user" class="function-icon" />
        <span>用户账号</span>
      </div>
      <div class="function-item" @click="goTo('/restaurantAcount')">
        <font-awesome-icon icon="user-tie" class="function-icon" />
        <span>商家账号</span>
      </div>
      <div class="function-item" @click="goTo('/realNameAuthentication')">
        <font-awesome-icon icon="chart-bar" class="function-icon" />
        <span>实名审批</span>
      </div>
      <div class="function-item" @click="goTo('/reportHandlinig')">
        <font-awesome-icon icon="circle-exclamation" class="function-icon" />
        <span>举报处理</span>
      </div>
      <div class="function-item" @click="goTo('/comment')">
        <font-awesome-icon icon="comment" class="function-icon" />
        <span>查看评论</span>
      </div>
    </div>
    <div class="logout-button">
      <a-button status="danger" @click="logout">退出登录</a-button>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from "vue";
import sHeader from "@/components/SimpleHeader.vue";
import { getAdminInfo, adminLogout } from "@/service/admin";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";

const router = useRouter();
const state = reactive({
  user: {},
  loading: false,
});

function fetchAdminInfo() {
  getAdminInfo()
    .then((response) => {
      state.user = response.data;
      state.loading = true;
    })
    .catch(() => {
      ElMessage.error("获取管理员信息失败");
    });
}

onMounted(() => {
  fetchAdminInfo();
});

function goTo(routePath, query = {}) {
  router.push({ path: routePath, query });
}

async function logout() {
  try {
    const response = await adminLogout();
    if (response.status === 200) {
      localStorage.removeItem("token");
      router.push("/login");
    } else {
      ElMessage.error("退出登录失败");
    }
  } catch (error) {
    ElMessage.error("退出登录失败");
  }
}
</script>

<style lang="less" scoped>
@import "../common/style/mixin";

.user-box {
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
    width: 90%;
    margin: 20px auto;
    height: 160px;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.2);
    border-radius: 16px;
    transition: transform 0.3s ease;
    overflow: hidden;

    &:hover {
      transform: translateY(-2px);
    }

    .info {
      display: flex;
      align-items: center;
      height: 100%;
      padding: 0 30px;
      gap: 24px;

      .profile-img {
        .wh(80px, 80px);
        border-radius: 50%;
        border: 3px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;

        &:hover {
          transform: scale(1.05);
        }
      }

      .user-desc {
        display: flex;
        flex-direction: column;
        gap: 12px;

        .account-number {
          font-size: 18px;
          font-weight: 500;
          color: #e0e7ff;
          letter-spacing: 0.5px;
          text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .account-type {
          background: rgba(255, 255, 255, 0.1);
          padding: 6px 12px;
          border-radius: 20px;
          font-size: 14px;
          color: #c4b5fd;
          font-weight: 600;
          backdrop-filter: blur(4px);
          width: fit-content;
        }
      }
    }
  }

  .function-list {
    width: 90%;
    margin: 20px auto; // 保持原有居中布局
    padding: 24px 30px; // 调整内边距更规范
    background: linear-gradient(
      135deg,
      #f0f4ff 0%,
      #f8f8f8 100%
    ); // 添加渐变背景
    border-radius: 16px; // 增加圆角
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.1); // 添加柔和阴影
    transition: transform 0.3s ease; // 添加过渡动画

    &:hover {
      transform: translateY(-2px); // 悬停上浮效果
    }

    .function-item {
      display: flex;
      align-items: center;
      padding: 12px 0; // 调整内边距
      border-bottom: 1px solid rgba(224, 224, 224, 0.5); // 半透明分割线
      cursor: pointer;
      transition: all 0.2s ease; // 添加过渡

      &:hover {
        background: rgba(255, 255, 255, 0.3); // 悬停背景效果
        padding-left: 8px; // 悬停位移效果
      }

      &:last-child {
        border-bottom: none;
      }

      .function-icon {
        font-size: 28px; // 放大图标
        color: #6366f1; // 使用主题紫色
        margin-right: 20px; // 固定间距
        transition: transform 0.3s ease;

        &:hover {
          transform: scale(1.1); // 图标悬停缩放
        }
      }

      span {
        font-size: 16px; // 放大文字
        color: #4b5563; // 深灰色文字
        letter-spacing: 0.3px; // 增加字间距
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05); // 文字阴影
      }
    }
  }

  .logout-button {
    display: flex;
    justify-content: center;
    margin-top: 20px;
    padding-bottom: 20px;
  }
}
</style>
