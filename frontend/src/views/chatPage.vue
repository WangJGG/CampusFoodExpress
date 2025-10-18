<template>
  <div class="chat-container">
    <!-- 群聊名称显示 -->
    <div class="chat-header">
      <!-- 左上角返回按钮 -->
      <button class="back-button" @click="handleBack">
        <van-icon name="arrow-left" size="18px" />
      </button>
      <h2 class="group-name">{{ this.groupName }}</h2>
      <!-- 右上角三个点图标 -->
      <button class="options-button" @click="handleDetail">
        ⋯
        <!-- Unicode: U+22EF -->
      </button>
    </div>

    <!-- 消息列表 -->
    <div class="messages" ref="messagesContainer" @scroll="handleScroll">
      <!-- 加载更多提示 -->
      <div v-if="isLoadingMore" class="loading-more">
        <span>加载更多...</span>
      </div>

      <!-- 消息项 -->
      <div v-for="(msg, index) in messages" :key="msg.id">
        <!-- 时间标识 -->
        <div v-if="showTimestamp(index)" class="timestamp">
          {{ formatTimestamp(msg.timestamp) }}
        </div>

        <!-- 消息气泡 -->
        <div
          :class="[
            'message',
            Number(msg.sender_id) === this.currentUserId ? 'sent' : 'received',
          ]"
        >
          <!-- 头像 -->
          <template v-if="msg.sender_id !== currentUserId">
            <!-- 头像显示在左边 -->
            <img
              :src="userAvatars[msg.sender_id] || defaultAvatar"
              alt="Avatar"
              class="avatar left-avatar"
            />
          </template>

          <!-- 消息内容 -->
          <div class="message-content">
            <template v-if="msg.content_type === 'link'">
              <!-- 渲染链接卡片消息 -->
              <div class="message-card" @click="navigateToLink(msg.content)">
                <div class="card-title">分享给您一个订单</div>
                <div class="card-link">点击查看详情</div>
              </div>
            </template>
            <template v-else-if="msg.content_type === 'text'">
              <!-- 普通文本消息 -->
              {{ msg.content }}
            </template>
            <template v-else>
              <div class="unsupported-message">不支持的消息类型</div>
            </template>
            <!-- <div class="message-time">
              {{ formatTime(msg.timestamp) }}
            </div> -->
          </div>

          <template v-if="msg.sender_id === currentUserId">
            <!-- 头像显示在右边 -->
            <img
              :src="userAvatars[msg.sender_id] || defaultAvatar"
              alt="Avatar"
              class="avatar right-avatar"
            />
          </template>
        </div>
      </div>
    </div>

    <!-- 输入框 -->
    <div class="input-container">
      <input
        type="text"
        v-model="newMessage"
        @keyup.enter="handleSendMessage"
        placeholder="输入消息..."
      />
      <button
        @click="handleSendMessage"
        :disabled="newMessage.trim() === ''"
        class="send-button"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="send-icon"
          viewBox="0 0 24 24"
          fill="#fff"
        >
          <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
        </svg>
      </button>
      <!-- 新增 "+" 按钮 -->
      <button @click="handleShowOrders" class="add-button">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="add-icon"
          viewBox="0 0 24 24"
          fill="#fff"
        >
          <path d="M19 13H13V19H11V13H5V11H11V5H13V11H19V13Z" />
        </svg>
      </button>
    </div>

    <!-- 订单列表 -->
    <div
      v-if="showOrderList"
      class="order-modal-overlay"
      @click="closeOrderList"
    >
      <div class="order-modal" @click.stop>
        <div class="order-modal-header">
          <!-- 左侧返回按钮 -->
          <button class="modal-back-button" @click="closeOrderList">‹</button>
          <h2>选择订单分享</h2>
        </div>
        <!-- 订单信息显示 -->
        <div class="order-modal-content">
          <div
            v-for="order in orders"
            :key="order.id"
            class="order-item"
            @click="handleOrderClick(order)"
          >
            <div class="order-info">
              <p class="restaurant-name">{{ order.restaurantName }}</p>
              <p class="order-address">{{ order.address }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 分享确认弹窗 -->
    <div v-if="showShareModal" class="share-modal-overlay">
      <div class="share-modal">
        <p class="modal-title">是否分享此订单</p>
        <div class="modal-buttons">
          <button @click="cancelShare" class="no-button">否</button>
          <button @click="shareOrder" class="yes-button">是</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  connectSocket,
  registerPrivateMessageHandler,
  registerGroupMessageHandler,
  sendPrivateMessage,
  sendGroupMessage,
  getMessageHistory,
} from "@/service/chatService.js"; // 根据实际路径调整

import { getGroup } from "@/service/group.js"; // 引入 getGroup 方法
import { getUserDetails } from "@/service/friends.js";
import { getRestaurantById } from "@/service/restaurantService.js";

import { getOrdersByUser } from "@/service/order.js";
import { getInfoById } from "@/service/user.js";
import { useRouter } from "vue-router";
import { v4 as uuidv4 } from "uuid"; // 确保已安装: npm install uuid
import { ElMessage } from "element-plus";

export default {
  name: "ChatPage",
  data() {
    return {
      messages: [], // 消息列表
      newMessage: "", // 新消息输入
      currentUserId: parseInt(localStorage.getItem("user_id"), 10) || null, // 当前用户ID (转为整数)
      chatType: "private", // 'private' 或 'group' 或 'temp'
      chatTargetId: null, // 对方用户ID或群组ID
      groupName: "", // 群组名称
      userAvatars: {}, // 存储每个用户的头像
      defaultAvatar: "https://via.placeholder.com/40", // 默认头像
      isLoadingMore: false, // 是否正在加载更多消息
      hasMoreMessages: true, // 是否还有更多历史消息
      page: 1, // 当前页码
      perPage: 20, // 每页消息数量
      showOrderList: false, // 控制订单列表显示
      showShareModal: false, // 控制分享弹窗显示
      orders: [], // 用户的订单列表
      selectedOrder: null, // 被选择的订单
      router: useRouter(),
    };
  },

  methods: {
    async getUserAvatar(userId) {
      if (this.userAvatars[userId]) return; // 如果头像已缓存，则无需重新请求
      try {
        const response = await getInfoById(userId);
        console.log(response.data.avatar);
        this.userAvatars[userId] = response.data.avatar; // 缓存头像
      } catch (error) {
        console.error("获取头像失败:", error);
      }
    },

    /**
     * 格式化时间为 HH:MM
     */
    formatTime(timestamp) {
      const date = new Date(timestamp);
      const hours = date.getHours().toString().padStart(2, "0");
      const minutes = date.getMinutes().toString().padStart(2, "0");
      return `${hours}:${minutes}`;
    },

    /**
     * // 实现返回逻辑，例如导航到上一页
     */
    handleBack() {
      this.router.push({
        path: "/friends",
        query: {
          type: this.chatType,
        },
      });
    },

    /**
     * 跳转到群组详情
     */
    handleDetail() {
      if (this.chatType === "private") {
        this.router.push({
          path: "/userInfo",
          query: {
            id: this.chatTargetId, // 将目标 ID 传递为查询参数
          },
        });
      } else {
        this.router.push({
          path: "/groupDetail",
          query: {
            id: this.chatTargetId, // 将目标 ID 传递为查询参数
          },
        });
      }
    },

    /**
     * 格式化时间为 YYYY-MM-DD HH:MM
     */
    formatTimestamp(timestamp) {
      const date = new Date(timestamp);
      const year = date.getFullYear();
      const month = (date.getMonth() + 1).toString().padStart(2, "0");
      const day = date.getDate().toString().padStart(2, "0");
      const hours = date.getHours().toString().padStart(2, "0");
      const minutes = date.getMinutes().toString().padStart(2, "0");
      return `${year}-${month}-${day} ${hours}:${minutes}`;
    },

    /**
     * 判断是否需要显示时间标识
     */
    showTimestamp(index) {
      if (index === 0) return true;
      const currentMsgTime = new Date(this.messages[index].timestamp).getTime();
      const previousMsgTime = new Date(
        this.messages[index - 1].timestamp
      ).getTime();
      return currentMsgTime - previousMsgTime > 2.5 * 60 * 1000; // 2.5分钟
    },

    /**
     * 处理发送消息
     */
    async handleSendMessage() {
      if (this.newMessage.trim() === "") return;

      const token = localStorage.getItem("token");
      const userId = parseInt(localStorage.getItem("user_id"), 10); // 确保 userId 为整数
      if (!token || !userId) {
        this.$router.push("/login");
        return;
      }

      try {
        if (this.chatType === "private") {
          // 发送私聊消息
          await sendPrivateMessage(
            token,
            parseInt(this.chatTargetId, 10),
            this.newMessage,
            "text"
          );
        } else if (this.chatType === "group") {
          // 发送群聊消息
          await sendGroupMessage(
            token,
            parseInt(this.chatTargetId, 10),
            this.newMessage,
            "text"
          );
        }

        // 添加到消息列表
        const message = {
          id: uuidv4(), // 使用 UUID 生成唯一ID
          sender_id: userId,
          receiver_id:
            this.chatType === "private"
              ? parseInt(this.chatTargetId, 10)
              : null,
          group_id:
            this.chatType === "group" ? parseInt(this.chatTargetId, 10) : null,
          content: this.newMessage,
          content_type: "text",
          timestamp: new Date().toISOString(),
        };
        this.addMessage(message);
        this.newMessage = "";
      } catch (error) {
        console.error("发送消息失败:", error);
        ElMessage.error("发送消息失败，请稍后再试。");
      }
    },

    /**
     * 添加消息到消息列表，并处理时间标识
     */
    addMessage(message) {
      this.messages.push(message);
      if (!this.isLoadingMore) {
        this.$nextTick(this.scrollToBottom);
      }
    },

    /**
     * 滚动到消息底部
     */
    scrollToBottom() {
      const container = this.$refs.messagesContainer;
      if (!container) {
        console.error("messagesContainer is not yet available.");
        return;
      }
      container.scrollTop = container.scrollHeight;
    },

    /**
     * 处理接收到的私聊消息
     */
    handlePrivateMessage(message) {
      if (
        this.chatType === "private" &&
        (message.sender_id === this.chatTargetId ||
          message.receiver_id === this.currentUserId)
      ) {
        this.addMessage(message);
        console.log(
          `收到来自用户 ${message.sender_id} 的消息: ${message.content}`
        );
      }
    },

    /**
     * 处理接收到的群聊消息
     */
    handleGroupMessage(message, isGroup) {
      if (
        isGroup &&
        this.chatType === "group" &&
        message.group_id === parseInt(this.chatTargetId, 10)
      ) {
        // 不显示自己发送的群消息
        if (message.sender_id !== parseInt(this.currentUserId, 10)) {
          this.addMessage(message);
          console.log(
            `收到群组 ${message.group_id} 的消息: ${message.content}`
          );
        }
      }
    },

    /**
     * 加载消息历史
     */
    async loadMessageHistory() {
      if (!this.hasMoreMessages || this.isLoadingMore) return;

      this.isLoadingMore = true;
      try {
        const data = await getMessageHistory(
          this.chatType === "private" ? this.chatTargetId : null,
          this.chatType === "group" ? this.chatTargetId : null,
          this.page,
          this.perPage
        );

        if (data.messages.length < this.perPage) {
          this.hasMoreMessages = false;
        }

        // 假设后端返回的消息按时间降序排列
        this.messages = [...data.messages.reverse(), ...this.messages];
        this.page += 1;

        // 加载每个消息的发送者头像
        data.messages.forEach((msg) => {
          if (msg.sender_id !== this.currentUserId) {
            this.getUserAvatar(msg.sender_id); // 获取发送者头像
          }
        });

        // 如果是第一次加载，滚动到底部
        if (this.page === 2) {
          this.$nextTick(this.scrollToBottom);
        }
      } catch (error) {
        console.error("加载消息历史失败:", error);
      } finally {
        this.isLoadingMore = false;
      }
    },

    /**
     * 处理滚动事件，判断是否需要加载更多消息
     */
    handleScroll() {
      const container = this.$refs.messagesContainer;
      if (!container) {
        console.error("messagesContainer is not yet available.");
        return;
      }

      if (
        container.scrollTop === 0 &&
        this.hasMoreMessages &&
        !this.isLoadingMore
      ) {
        this.loadMessageHistory();
      }
    },

    /**
     * 初始化聊天
     * @param {string} type - 'private' 或 'group'
     * @param {string} targetId - 对方用户ID或群组ID
     */
    async initializeChat(type, targetId) {
      if (type === "friend") {
        type = "private"; // 将 'friend' 类型转换为 'private'
      }

      if (type !== "private" && type !== "group") {
        console.error("Invalid chat type:", type);
        return;
      }

      this.chatType = type;
      this.chatTargetId = parseInt(targetId, 10); // 确保转为整数
      this.messages = [];
      this.page = 1;
      this.hasMoreMessages = true;

      if (type === "group") {
        try {
          const group = await getGroup(targetId);
          this.groupName = group.data.group.name || "群聊";
        } catch (error) {
          console.error("获取群组信息失败:", error);
          this.groupName = "群聊";
        }
      } else {
        // 如果是私聊，可以设置为对方的名称（假设有获取用户信息的方法）
        try {
          const friendData = await getUserDetails(targetId);
          this.groupName = friendData.data.nickname || "好友"; // 访问响应数据中的 nickname
        } catch (error) {
          console.error("获取好友信息失败:", error);
          this.groupName = "好友";
        }
      }

      this.loadMessageHistory();
    },

    /**
     * 显示订单列表
     */
    async handleShowOrders() {
      try {
        const response = await getOrdersByUser();
        const orders = response.data;
        for (const order of orders) {
          const restaurantResponse = await getRestaurantById(
            order.restaurant_id
          );
          order.restaurantName = restaurantResponse.data.name; // 添加商家名称
        }
        this.orders = orders.map((order) => ({
          id: order.id,
          restaurantName: order.restaurantName,
          address: order.address,
        }));
        this.showOrderList = true;
      } catch (error) {
        console.error("获取订单失败：", error);
      }
    },

    /**
     * 点击订单后触发
     * @param order - 用户选择的订单
     */
    handleOrderClick(order) {
      this.selectedOrder = order;
      this.showOrderList = false;
      this.showShareModal = true;
    },

    /**
     * 确认分享订单
     */
    shareOrder() {
      const orderLink = `/orderDetail?id=${this.selectedOrder.id}`; // 生成订单链接
      const token = localStorage.getItem("token");
      const message = {
        id: uuidv4(), // 临时生成唯一 ID，用于前端显示
        sender_id: this.currentUserId, // 当前用户 ID
        content: orderLink, // 消息内容直接为链接
        content_type: "link", // 消息类型为 link
        timestamp: new Date().toISOString(), // 当前时间
        group_id: this.chatType === "group" ? this.chatTargetId : null, // 群聊 ID（如果是群聊）
        receiver_id: this.chatType === "private" ? this.chatTargetId : null, // 私聊接收者 ID（如果是私聊）
      };

      // 调用方法发送消息（私聊或群聊）
      if (this.chatType === "private") {
        sendPrivateMessage(token, this.chatTargetId, orderLink, "link");
      } else {
        sendGroupMessage(token, this.chatTargetId, orderLink, "link");
      }

      // 将消息添加到本地消息列表
      this.addMessage(message);
      this.showShareModal = false; // 关闭分享弹窗
    },

    /**
     * 关闭订单列表显示
     */
    closeOrderList() {
      this.showOrderList = false;
    },

    /**
     * 取消分享
     */
    cancelShare() {
      this.showShareModal = false;
      this.showOrderList = true;
    },

    navigateToLink(link) {
      if (!link) {
        console.error("无效的链接");
        return;
      }
      this.$router.push(link);
    },
  },

  watch: {
    /**
     * 监听路由变化，重新初始化聊天
     */
    "$route.query.type"(newType, oldType) {
      const newId = this.$route.query.id;
      if (
        newType &&
        newId &&
        (newType !== oldType || newId !== this.chatTargetId)
      ) {
        this.initializeChat(newType, newId);
      }
    },
    "$route.query.id"(newId, oldId) {
      const newType = this.$route.query.type;
      if (newType && newId && (newType !== this.chatType || newId !== oldId)) {
        this.initializeChat(newType, newId);
      }
    },
  },

  mounted() {
    // 获取当前用户ID（假设存储在本地Storage中）
    const token = localStorage.getItem("token");
    const userId = parseInt(localStorage.getItem("user_id"), 10); // 确保转为整数
    if (!token || !userId) {
      // 处理未登录状态
      this.$router.push("/login");
      return;
    }

    this.currentUserId = userId;

    // 在页面加载时获取当前用户的头像
    this.getUserAvatar(this.currentUserId);

    // 连接WebSocket
    connectSocket(token);

    // 注册消息处理函数
    registerPrivateMessageHandler(this.handlePrivateMessage);
    registerGroupMessageHandler(this.handleGroupMessage);

    // 初始化聊天，根据路由查询参数
    const { type, id } = this.$route.query;
    if (type && id) {
      this.initializeChat(type, id);
    } else {
      console.error("Missing chat type or ID in route query.");
    }

    // 不需要在这里加载初始消息历史，因为 initializeChat 已经调用了 loadMessageHistory
  },
};
</script>

<style scoped>
/* 群聊头部 */
.chat-header {
  position: relative;
  /* 用于放置返回按钮 */
  padding: 20px;
  background-color: #075e54;
  color: #ffffff;
  text-align: center;
  border-bottom: 1px solid #128c7e;
  font-size: 1.2em;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  /* 群聊名称居中 */
  box-sizing: border-box;
  /* 确保padding不增加外部尺寸 */
}

/* 返回按钮样式 */
.back-button {
  position: absolute;
  /* 绝对定位 */
  left: 10px;
  /* 靠近左侧 */
  top: 50%;
  /* 垂直居中 */
  transform: translateY(-50%);
  background: none;
  /* 无背景 */
  border: none;
  /* 无边框 */
  color: #ffffff;
  /* 按钮颜色 */
  font-size: 1em;
  /* 字体大小 */
  font-weight: bold;
  cursor: pointer;
  /* 鼠标悬停变手型 */
  padding: 2px 10px;
  /* 增大点击区域的 padding */
  outline: none;
  transition: color 0.3s ease;
  /* 增加悬停效果 */
  z-index: 1050;
}

.options-button {
  background: none;
  border: none;
  font-size: 24px;
  /* 调整图标大小 */
  cursor: pointer;
  color: #ffffff;
  padding: 5px;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  /* 绝对定位 */
  right: 10px;
  /* 靠近右侧 */
  top: 50%;
  /* 垂直居中 */
  transform: translateY(-50%);
  /* 垂直居中 */
  z-index: 1050;
}

/* 群聊名称 */
.group-name {
  flex: 1;
  /* 占据剩余空间，保持居中 */
  text-align: center;
  margin: 0;
  font-size: 1.2em;
  font-weight: bold;
  color: #ffffff;
  /* 确保字体颜色在深色背景下清晰 */
}

.back-button:hover {
  color: #d1d1d1;
  /* 鼠标悬停时按钮变灰 */
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #ece5dd;
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  overflow: hidden;
  /* 防止溢出 */
  box-sizing: border-box;
  /* 确保padding不增加外部尺寸 */
}

/* 优化滚动条 */
.chat-container::-webkit-scrollbar {
  width: 8px;
}

.chat-container::-webkit-scrollbar-thumb {
  background: #cccccc;
  border-radius: 4px;
}

.chat-container::-webkit-scrollbar-thumb:hover {
  background: #888888;
}

.messages {
  flex: 1;
  padding: 0px 0px;
  /* 减少顶部和底部的内边距 */
  overflow-y: auto;
  /* background-image: url('https://i.imgur.com/1H8YqfK.png');  可选：添加背景图 */
  background-color: rgb(236, 229, 221);
  /* 使用指定背景颜色 */
  position: relative;
  display: flex;
  flex-direction: column;
  border-top: 1px solid #ddd;
  /* 顶部分隔线 */
  border-bottom: 1px solid #ddd;
  /* 底部分隔线 */
  box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.1);
  /* 增加内阴影 */
  box-sizing: border-box;
  /* 确保padding不增加外部尺寸 */
  margin: 0;
  /* 确保没有外部边距 */
}

.loading-more {
  text-align: center;
  padding: 10px 0;
  color: #555;
}

.message {
  display: flex;
  margin: 5px 0;
  transition: all 0.3s ease;
  padding: 2px 4px;
  border-radius: 10px;
  align-items: center;
  /* 保证头像与消息内容在同一行 */
}

/* 发送的消息 */
.sent {
  justify-content: flex-end;
  /* 发送的消息对齐右边 */
}

/* 接收的消息 */
.received {
  justify-content: flex-start;
  /* 接收的消息对齐左边 */
}

.message-content {
  max-width: 60%;
  padding: 8px 12px;
  border-radius: 15px;
  position: relative;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  /* 增加轻微的阴影 */
  word-wrap: break-word;
  font-size: 14px;
  display: flex;
  flex-direction: column;
  animation: fadeIn 0.3s ease;
  /* 淡入动画 */
}

.sent .message-content {
  background-color: #dcf8c6;
  /* 绿色气泡 */
  border-bottom-right-radius: 0;
}

.received .message-content {
  background-color: #ffffff;
  /* 白色气泡 */
  border-bottom-left-radius: 0;
}

/* 消息对齐 */
.sent {
  justify-content: flex-end;
  /* 发送的消息对齐右边 */
}

.received {
  justify-content: flex-start;
  /* 接收的消息对齐左边 */
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid rgba(0, 0, 0, 0.1);
  /* 增加边框 */
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  /* 增加阴影 */
  margin: 0 4px;
  /* 默认的间距 */
}

/* 左侧头像 */
.left-avatar {
  margin-right: 7px;
  /* 头像与消息内容的间距 */
}

/* 右侧头像 */
.right-avatar {
  margin-left: 7px;
  /* 头像与消息内容的间距 */
}

.message-time {
  font-size: 0.8em;
  color: #999;
  margin-top: 5px;
  text-align: right;
}

.timestamp {
  text-align: center;
  margin: 20px 0;
  color: #666;
  font-size: 0.8em;
  position: relative;
}

.timestamp::before,
.timestamp::after {
  content: "";
  position: absolute;
  top: 50%;
  width: 36%;
  height: 1px;
  background-color: #ccc;
}

.timestamp::before {
  left: 0;
}

.timestamp::after {
  right: 0;
}

.input-container {
  display: flex;
  padding: 10px;
  border-top: 1px solid #ddd;
  background-color: #f0f0f0;
}

.input-container input {
  flex: 1;
  padding: 10px 15px;
  border: none;
  border-radius: 20px;
  outline: none;
  font-size: 14px;
  background-color: #ffffff;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.input-container input::placeholder {
  color: #999;
}

.send-button {
  margin-left: 10px;
  padding: 0;
  background-color: #09bb07;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease;
}

.send-button:disabled {
  background-color: #a5d6a7;
  cursor: not-allowed;
}

.send-button:hover:not(:disabled) {
  background-color: #08a106;
}

.send-icon {
  width: 20px;
  height: 20px;
}

/* 滚动条样式 */
.messages::-webkit-scrollbar {
  width: 8px;
}

.messages::-webkit-scrollbar-track {
  background: transparent;
}

.messages::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.messages::-webkit-scrollbar-thumb:hover {
  background-color: rgba(0, 0, 0, 0.4);
}

.add-button {
  margin-left: 10px;
  padding: 0;
  background-color: #128c7e;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease;
}

.add-button:hover {
  background-color: #0a6c5c;
}

.add-icon {
  width: 20px;
  height: 20px;
}

/* 黑色遮罩层 */
.order-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  /* 半透明背景 */
  display: flex;
  justify-content: center;
  align-items: flex-end;
  /* 弹窗靠底部 */
  z-index: 1000;
}

/* 订单选择弹窗 */
.order-modal {
  background-color: #fff;
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
  max-height: 70vh;
  overflow-y: auto;
  width: 100%;
  max-width: 100%;
  /* 和主区域一致的宽度 */
  margin: 0 auto;
  /* 居中对齐 */
  box-shadow: 0px -4px 15px rgba(0, 0, 0, 0.4);
  /* 阴影效果 */
  z-index: 1001;
  animation: slideUp 0.3s ease;
  /* 弹窗滑入动画 */
}

/* 弹窗头部样式 */
.order-modal-header {
  display: flex;
  align-items: center;
  /* 垂直居中 */
  justify-content: center;
  /* 水平居中 */
  padding: 15px;
  border-bottom: 1px solid #eee;
  position: relative;
  /* 确保返回按钮不影响标题 */
}

.order-modal-header h2 {
  font-size: 18px;
  color: #333;
  margin: 0;
}

/* 返回按钮样式 */
.modal-back-button {
  position: absolute;
  left: 15px;
  top: 15px;
  background: none;
  border: none;
  font-size: 24px;
  color: #333;
  cursor: pointer;
  z-index: 1002;
  /* 增加z-index以确保按钮在最上层 */
}

.modal-back-button:hover {
  transform: scale(1.1);
  /* 鼠标悬停放大效果 */
}

.back-icon {
  width: 24px;
  height: 24px;
  fill: #333;
  /* 图标颜色 */
  transition: fill 0.2s ease;
}

.modal-back-button:hover .back-icon {
  fill: #128c7e;
  /* 悬停时颜色变化 */
}

/* 弹窗内容样式 */
.order-modal-content {
  padding: 10px 15px;
}

/* 单个订单项样式 */
.order-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px;
  margin: 10px 0;
  /* 调整间距，增加上下分隔 */
  border-radius: 10px;
  /* 增加圆角 */
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.05);
  /* 增加轻微阴影 */
  background-color: #fff;
  /* 背景色 */
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid #f0f0f0;
  /* 边框增强分割感 */
}

.order-info p {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.no-orders {
  text-align: center;
  color: #666;
  padding: 20px;
  font-size: 16px;
}

.order-item:hover {
  background-color: #f9f9f9;
  /* 悬停时背景变浅 */
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  /* 悬停时阴影加深 */
  transform: translateY(-1px);
  /* 增加轻微浮动效果 */
}

/* 订单信息样式 */
.order-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
  /* 信息之间的间距 */
}

.restaurant-name {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.order-address {
  font-size: 14px;
  color: #666;
  text-overflow: ellipsis;
  /* 防止文字超出 */
  overflow: hidden;
  white-space: nowrap;
}

/* 弹窗动画 */
@keyframes slideUp {
  from {
    transform: translateY(100%);
  }

  to {
    transform: translateY(0);
  }
}

.order-content {
  font-size: 16px;
  color: #333;
}

.share-modal-overlay {
  z-index: 1050;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.share-modal {
  background-color: #fff;
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
  transition: all 0.2s ease;
  /* 增加动画效果 */
  width: 240px;
  /* 增大弹窗宽度 */
  max-width: 400px;
  /* 设置最大宽度，适应更大的屏幕 */
}

.modal-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

.modal-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.no-button {
  padding: 12px 30px;
  background-color: #ff5252;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.no-button:hover {
  background-color: #e04848;
  /* 悬停效果 */
}

.yes-button {
  padding: 12px 30px;
  background-color: #09bb07;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.yes-button:hover {
  background-color: #07a105;
  /* 悬停效果 */
}

.order-content {
  display: flex;
  flex-direction: column;
}

.restaurant-name {
  font-weight: bold;
  color: #333;
}

.address {
  color: #666;
  font-size: 14px;
}

.message-card {
  padding: 15px;
  border-radius: 10px;
  background-color: #ffffff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  margin: 10px 0;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.message-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.card-link {
  font-size: 14px;
  color: #09bb07;
  text-decoration: underline;
}
</style>
