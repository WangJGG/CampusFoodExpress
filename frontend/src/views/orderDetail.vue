<template>
  <div class="order-detail">
    <header class="header">
      <button class="back-button" @click="goBack">
        <van-icon name="arrow-left" size="18px" />
      </button>
      <h1>订单详情</h1>
    </header>

    <div class="order-content">
      <div v-if="order.loading">加载中...</div>
      <div v-else>
        <!-- 订单信息 -->
        <div class="info-box">
          <h2>
            <span class="icon-container"><font-awesome-icon :icon="['fas', 'receipt']"
                :style="{ color: '#FF7043' }" /></span>
            订单标题： {{ order.data.user.nickname }} 发布的订单
          </h2>
          <p>
            <span class="icon-container"><font-awesome-icon :icon="['fas', 'calendar-alt']"
                :style="{ color: '#FF7043' }" /></span>
            <strong>发布时间： </strong>{{ order.data.order_date }}
          </p>
          <p>
            <span class="icon-container"><font-awesome-icon :icon="['fas', 'check-circle']"
                :style="{ color: '#FF7043' }" /></span>
            <strong>订单状态：</strong>{{ order.data.status }}
          </p>
          <p>
            <span class="icon-container"><font-awesome-icon :icon="['fas', 'dollar-sign']"
                :style="{ color: '#FF7043' }" /></span>
            <strong>订单报酬： </strong>{{ order.data.delivery_fee }}元
          </p>
          <p>
            <span class="icon-container"><font-awesome-icon :icon="['fas', 'map-marker-alt']"
                :style="{ color: '#FF7043' }" /></span>
            <strong>取餐时间： </strong>预计{{
              order.data.expected_pickup_time
            }}取餐
          </p>
          <p>
            <span class="icon-container"><font-awesome-icon :icon="['fas', 'clock']"
                :style="{ color: '#FF7043' }" /></span>
            <strong>送达时间： </strong>预计{{
              order.data.desired_delivery_time
            }}送达
          </p>
          <p>
            <span class="icon-container"><font-awesome-icon :icon="['fas', 'list-ul']"
                :style="{ color: '#FF7043' }" /></span>
            <strong>详细要求： </strong>{{ order.data.remarks }}
          </p>
        </div>

        <!-- 发布者信息 -->
        <div class="info-box">
          <h3>
            <span class="icon-container"><font-awesome-icon :icon="['fas', 'user']"
                :style="{ color: '#FF7043' }" /></span>
            订单发布者
          </h3>
          <p>
            <span class="icon-container"><font-awesome-icon :icon="['fas', 'user-circle']"
                :style="{ color: '#FF7043' }" /></span>
            <strong>姓名： </strong>{{ order.data.user.nickname }}
          </p>
          <p>
            <span class="icon-container"><font-awesome-icon :icon="['fas', 'phone']"
                :style="{ color: '#FF7043' }" /></span>
            <strong>联系方式： </strong>{{ order.data.user.phone }}
          </p>
        </div>

        <!-- 商家信息 -->
        <div class="info-box">
          <h3>
            <span class="icon-container"><font-awesome-icon :icon="['fas', 'store']"
                :style="{ color: '#FF7043' }" /></span>
            订单来源商家
          </h3>
          <p>
            <span class="icon-container"><font-awesome-icon :icon="['fas', 'store-alt']"
                :style="{ color: '#FF7043' }" /></span>
            <strong>商家名称： </strong>{{ order.data.restaurant.name }}
          </p>
          <p>
            <span class="icon-container"><font-awesome-icon :icon="['fas', 'map-marker-alt']"
                :style="{ color: '#FF7043' }" /></span>
            <strong>地址：</strong>{{ order.data.restaurant.address }}
          </p>
          <p>
            <span class="icon-container"><font-awesome-icon :icon="['fas', 'phone-square-alt']"
                :style="{ color: '#FF7043' }" /></span>
            <strong>电话： </strong>{{ order.data.restaurant.phone }}
          </p>
          <p>
            <span class="icon-container"><font-awesome-icon :icon="['fas', 'clock']"
                :style="{ color: '#FF7043' }" /></span>
            <strong>描述：</strong>{{ order.data.restaurant.description }}
          </p>
        </div>

        <!-- 按钮区域 -->
        <div class="action-buttons">
          <div v-if="
            order.data.status === 'Created' &&
            order.data.user_id != state.user.id
          ">
            <button class="action-button" @click="handleAcceptOrder">
              接受悬赏
            </button>
          </div>
          <div v-if="
            order.data.status === 'Shipped' &&
            order.data.delivery_person_id === state.user.id
          ">
            <button class="action-button" @click="handleCompleteOrder">
              完成悬赏
            </button>
            <button class="action-button cancel" @click="handleCancelOrder">
              放弃悬赏
            </button>
          </div>
          <div v-if="
            order.data.status != 'Completed' &&
            order.data.user_id === state.user.id &&
            order.data.status != 'Deleted'
          ">
            <button class="action-button cancel" @click="handleDeleteOrder">
              取消悬赏
            </button>
          </div>
          <div v-if="
            order.data.status === 'Completed' &&
            order.data.user_id == state.user.id &&
            !order.data.is_commented
          ">
            <button class="action-button" @click="MerchantRate(order.data.id)">
              评价
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/* eslint-disable */
import { onMounted, reactive, computed } from "vue"; // 确保导入 computed
import { useRouter, useRoute } from "vue-router";
import {
  getOrderById,
  acceptOrder,
  cancelOrder,
  deleteOrder,
  completeOrder,
} from "@/service/order";
import { getUserInfo } from "@/service/user";
import { addFriend, deleteFriend, checkFriend } from "@/service/friends";
// import { getLocal } from '@/common/js/utils';
import { ElMessage } from "element-plus";

const router = useRouter();
const route = useRoute();

const order = reactive({
  data: {},
  loading: true,
});
const isFriend = reactive({ value: false });
const userId = parseInt(localStorage.getItem("user_id"), 10); // 获得当前的userId

const state = reactive({
  user: {},
  loading: true,
});

const MerchantRate = (orderId) => {
  try {
    // 处理后端响应，例如跳转到新页面
    router.push({ path: "/merchantRate", query: { id: orderId } });
  } catch (error) {
    console.error("请求失败:", error);
  }
};

// 获取订单详细信息
const fetchOrderDetails = async () => {
  try {
    const id = route.query.id;
    if (!id) {
      throw new Error("订单ID不能为空");
    }
    const response = await getOrderById(id);
    order.data = response.data;
    order.loading = false;
    console.log(order.data.user_id);
  } catch (error) {
    console.error("Error loading order details:", error);
    ElMessage.error("获取订单详情失败，稍后再试");
  }
};

// 更新订单状态为“已接受”
const handleAcceptOrder = async () => {
  try {
    console.log(state.user.auth_status);
    if (state.user.auth_status === "unauthorized") {
      ElMessage.warning("请先进行实名认证！");
      return;
    }
    if (state.user.auth_status === "pending") {
      ElMessage.warning("您的实名认证还在审核中，请耐心等待");
      return;
    }

    const deliveryPersonId = state.user.id; // 获取当前用户ID，即配送员ID
    const orderId = order.data.id; // 获取当前订单的ID

    // 调用 acceptOrder 函数，发送订单ID和配送员ID
    console.log(orderId, deliveryPersonId);
    const response = await acceptOrder(orderId, deliveryPersonId);

    // 判断后端响应
    if (response.data.message === "Order accepted successfully") {
      order.data.status = "Shipped"; // 更新订单状态
      order.data.delivery_person_id = deliveryPersonId; // 设置配送员ID
      const res = await checkFriend(order.data.user_id); // 检查订单发起者(user_id)和当前页面的用户(deliveryPersonId)是否为好友
      isFriend.value = res.data.isFriend;
      if (!isFriend.value) {
        addFriend(order.data.user_id); // 将订单发起者(user_id)和当前页面的用户(deliveryPersonId)建立好友关系
      }
      ElMessage.success("成功接受悬赏！");
    } else {
      ElMessage.error("接受悬赏失败");
    }
  } catch (error) {
    console.error("Error accepting order:", error);
    ElMessage.error("接受悬赏失败，请稍后再试");
  }
};

// 放弃订单的悬赏
const handleCancelOrder = async () => {
  try {
    const response = await cancelOrder(order.data.id); // 重置订单状态为“Created”并清空user_id
    if (response.data.message === "Order rejected successfully") {
      order.data.status = "Created"; // 更新前端状态
      order.data.delivery_person_id = null; // 清空user_id
      if (!isFriend.value) {
        deleteFriend(order.data.user_id); // 将订单发起者(user_id)和当前页面的用户(deliveryPersonId)删除好友关系
      }
      ElMessage.success("成功放弃悬赏！");
    } else {
      ElMessage.error("放弃悬赏失败");
    }
  } catch (error) {
    console.error("Error canceling order:", error);
    ElMessage.error("放弃悬赏失败，请稍后再试");
  }
};

// 取消订单的悬赏
const handleDeleteOrder = async () => {
  try {
    const response = await deleteOrder(order.data.id); // 重置订单状态为“Created”并清空user_id
    if (response.data.message === "Order deleted successfully") {
      // 判断状态 created不执行删除好友，当 order.data.status === 'Shipped' 时，再执行下面的 deleteFriend 操作
      if (order.data.status === "Shipped") {
        console.log("user_id:", order.data.delivery_person_id);
        if (!isFriend.value) {
          const deleteResponse = await deleteFriend(
            order.data.delivery_person_id
          ); // 删除好友关系
          console.log(deleteResponse);
        }
        order.data.delivery_person_id = null; // 清空user_id
      }

      order.data.status = "Deleted"; // 更新前端状态
      ElMessage.success("成功取消悬赏！");
    } else {
      ElMessage.error("取消悬赏失败");
    }
  } catch (error) {
    console.error("Error canceling order:", error);
    ElMessage.error("取消悬赏失败，请稍后再试");
  }
};

// 完成订单的悬赏
const handleCompleteOrder = async () => {
  try {
    const response = await completeOrder(order.data.id); // 重置订单状态为“Created”并清空user_id
    if (response.data.message === "Order completed successfully") {
      order.data.status = "Completed"; // 更新前端状态
      order.data.delivery_person_id = null; // 清空user_id
      if (!isFriend.value) {
        deleteFriend(order.data.user_id); // 将订单发起者(user_id)和当前页面的用户(deliveryPersonId)删除好友关系
      }
      ElMessage.success("成功完成悬赏！");
    } else {
      ElMessage.error("完成悬赏失败");
    }
  } catch (error) {
    console.error("Error canceling order:", error);
    ElMessage.error("完成悬赏失败，请稍后再试");
  }
};

// 添加联系函数
const contactPerson = async (type) => {
  try {
    const orderData = order.data;

    // 根据传入的 type 来决定是 userId 还是 deliveryPersonId
    const id =
      type === "customer" ? orderData.user_id : orderData.delivery_person_id;
    console.log(id);

    // 跳转到聊天页面
    router.push({ path: "/chatPage", query: { type: "friend", id } });
  } catch (error) {
    console.error("获取订单信息失败:", error);
    ElMessage.error("联系失败，请稍后重试");
  }
};

// 页面加载时调用
onMounted(async () => {
  fetchOrderDetails();
  const response = await getUserInfo();
  state.user = response.data;
  state.loading = false;
});

const buttons = computed(() => {
  const btns = [];

  // 判断当前用户是否可接受悬赏
  if (order.data.status === "Created" && order.data.user_id !== state.user.id) {
    btns.push({ text: "接受悬赏", action: acceptOrder });
  }

  // 判断当前用户是否为配送员，显示完成或放弃悬赏按钮
  if (
    order.data.status === "Shipped" &&
    order.data.delivery_person_id === state.user.id
  ) {
    btns.push({ text: "完成悬赏", action: completeOrder });
    btns.push({ text: "放弃悬赏", action: cancelOrder, type: "cancel" });
  }

  // 判断订单发布者是否可取消订单
  if (
    order.data.status !== "Completed" &&
    order.data.user_id === state.user.id
  ) {
    btns.push({ text: "取消悬赏", action: deleteOrder, type: "cancel" });
  }

  // 判断是否可评价订单
  if (
    order.data.status === "Completed" &&
    (order.data.user_id === state.user.id ||
      order.data.delivery_person_id === state.user.id)
  ) {
    btns.push({ text: "评价", action: () => MerchantRate(order.data.id) });
  }

  // 判断是否显示联系按钮
  if (order.data.status === "Shipped") {
    if (userId === order.data.user_id) {
      btns.push({
        text: "联系配送员",
        action: () => contactPerson("delivery"),
      });
    }
    if (userId === order.data.delivery_person_id) {
      btns.push({ text: "联系客户", action: () => contactPerson("customer") });
    }
  }

  return btns;
});

const goBack = () => {
  router.back();
};
</script>

<style scoped>
/* 页面整体 */
.order-detail {
  font-family: Arial, sans-serif;
  background-color: #f8f4ec;
  min-height: 100vh;
  color: #333;
}

/* 顶部导航栏 */
.header {
  background: linear-gradient(to bottom, #f9e8a0, #f8f4ec);
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}

.header h1 {
  font-size: 25px;
  font-weight: bold;
  color: #333;
}

/* 内容区域 */
.order-content {
  padding: 20px;
}

/* 信息框 */
.info-box {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* 标题样式 */
.info-box h2,
.info-box h3 {
  font-size: 20px;
  color: #333;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}

/* 文字和图标对齐样式 */
.info-box p {
  font-size: 16px;
  color: #666;
  line-height: 1.6;
  margin: 10px 0;
  display: flex;
  align-items: center;
  /* 使图标和文字垂直对齐 */
}

/* 图标容器样式，确保图标对齐一致 */
.icon-container {
  width: 26px;
  /* 适当减小图标容器的宽度 */
  height: 26px;
  /* 适当减小图标容器的高度 */
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
  /* 减少图标与文字之间的间距 */
}

.order-info p strong,
.publisher-info p strong,
.merchant-info p strong {
  margin-right: 6px;
  color: #333;
  font-weight: bold;
}

/* 统一图标大小和颜色 */
.icon-container svg {
  font-size: 20px;
  /* 增大图标的大小 */
  color: #ff7043 !important;
  /* 确保颜色应用到图标 */
}

/* 边距和间距的改进 */
.info-box {
  padding-top: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.info-box:last-child {
  border-bottom: none;
}

/* 按钮区域 */
.action-buttons {
  display: flex;
  justify-content: space-evenly;
  gap: 15px;
  margin-top: 20px;
  flex-wrap: wrap;
  /* 小屏幕下允许按钮换行 */
}

.action-button {
  flex: 1;
  max-width: 130px;
  /* 最大宽度限制 */
  min-width: 80px;
  /* 最小宽度限制 */
  background: linear-gradient(to right, #5cab5f, #72c876);
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 25px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.action-button:hover {
  background: linear-gradient(to right, #4da551, #57a859);
  /* 悬停时加深背景 */
  transform: scale(1.05);
  /* 增加轻微缩放效果 */
}

.action-button.cancel {
  background: linear-gradient(to right, #f74b17, #f93c02);
  /* 单独设置取消按钮为红色渐变 */
}

.action-button.cancel:hover {
  background: linear-gradient(to right, #e64a19, #ff5722);
  /* 红色按钮悬停效果 */
}

@media screen and (max-width: 600px) {
  .action-buttons {
    justify-content: center;
    /* 按钮居中 */
    gap: 10px;
    /* 减小间距 */
    margin-top: 15px;
    /* 调整间距 */
  }

  .action-button {
    width: 45%;
    /* 小屏幕下按钮宽度为容器宽度的45%，这样按钮不会太小 */
    max-width: 250px;
    /* 设置一个适应的最大宽度 */
    min-width: 120px;
    /* 最小宽度设置，确保按钮不至于太小 */
  }
}
</style>
