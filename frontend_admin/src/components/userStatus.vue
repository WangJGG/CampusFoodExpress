<template>
  <div class="user-status" @click="handleClick">
    <span class="status-label">{{ currentStatus }}</span>
  </div>
</template>

<script>
import { getStatus, checkActiveStatus } from '@/service/userStatus';

export default {
  name: 'UserStatus',
  data() {
    return {
      statusList: ['😋在干饭', '😢饿饿', '🥣等饭吃'], // 默认状态列表
      currentStatusIndex: null,
      hasActiveStatus: false, // 判断用户是否有活动状态
      currentStatus: '+',
    };
  },
  watch: {
  hasActiveStatus() {
    this.checkAndFetchCurrentStatus();
    // this.showCurrentStatus();
  },
  currentStatusIndex() {
    this.showCurrentStatus();
  },
},
  mounted() {
    this.checkAndFetchCurrentStatus();
    // this.showCurrentStatus();
  },
  async created() {
    await this.checkAndFetchCurrentStatus();
  },
  methods: {
    showCurrentStatus() {
    if (this.hasActiveStatus) {
      // 有活动状态时，根据状态序号更新状态文字
      this.currentStatus = this.statusList[this.currentStatusIndex] || '未知状态';
      console.log('当前状态:', this.currentStatus);
    } else {
      // 没有活动状态时显示 '+'
      this.currentStatus = '+';
    }
  },
    // 检查是否有活动状态，并获取当前状态
    async checkAndFetchCurrentStatus() {
      try {
        // 检查是否有活动状态
        const checkResponse = await checkActiveStatus();
        this.hasActiveStatus = checkResponse.has_status;

        if (this.hasActiveStatus) {
          // 获取当前活动状态的 ID
          const statusResponse = await getStatus();
          const statusId = statusResponse?.status?.status_id;

          // 根据状态 ID 更新当前状态序号
          if (statusId !== undefined && statusId !== null && statusId < this.statusList.length) {
            this.currentStatusIndex = statusId;
          } else {
            console.warn('未找到有效的状态 ID');
            this.currentStatusIndex = null;
          }
        } else {
          // 没有活动状态时，显示 '+'
          this.currentStatusIndex = null;
        }
      } catch (error) {
        console.error('检查和获取当前状态失败:', error);
        this.hasActiveStatus = false;
        this.currentStatusIndex = null;
      }
    },

    // 处理点击事件
    async handleClick() {
      try {
        if (this.hasActiveStatus) {
          // 刷新当前状态
          await this.checkAndFetchCurrentStatus();
        }
        // 跳转到状态详情页面
        this.$router.push({
          path: '/statusDetail',
          query: { status: this.currentStatus },
        });
      } catch (error) {
        console.error('跳转状态详情页面失败:', error);
        alert('跳转状态详情页面失败，请检查网络连接或联系管理员');
      }
    },
  },
};
</script>

<style scoped>
.user-status {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 120px;
  height: 40px;
  border-radius: 20px;
  background-color: #fee200;
  color: #333;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.user-status:hover {
  background-color: #f47c3c;
}

.status-label {
  font-weight: bold;
}
</style>
