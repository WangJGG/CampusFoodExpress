<template>
  <div class="order-list">
    <el-card v-for="order in orders" :key="order.id" class="order-card" shadow="hover">
      <div class="order-header">
        <h3>{{ order.restaurant_name }}</h3>
        <el-tag v-if="order.status === 'Completed'" type="success">已完成</el-tag>
        <el-tag v-else-if="order.status === '待评价'" type="warning">待评价</el-tag>
      </div>

      <div class="order-details">9
        <p>订单号：{{ order.id }}</p>
        <p>下单时间：{{ order.order_time }}</p>
        <p>总金额：￥{{ order.total_price }}</p>

        <ul class="food-list">
          <li v-for="item in order.items" :key="item.id">
            <span class="food-name">{{ item.name }}</span>
          </li>
        </ul>
      </div>

      <div class="order-actions">
        <el-button size="mini" type="primary" @click="rateOrder(order.id)">
          评价该订单
        </el-button>
        <el-button size="mini" type="warning" @click="complainOrder(order.id)">
          投诉该订单
        </el-button>
        <el-button size="mini" @click="reorder(order.id)">
          再来一单
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "OrderList",
  props: {
    orders: {
      type: Array,
      required: true,
    },
  },
  methods: {
    rateOrder(orderId) {
      // 跳转到评价页面
      this.$router.push(`/rate/${orderId}`);
    },
    complainOrder(orderId) {
      // 处理投诉逻辑，可以弹出对话框或发送请求
      this.$emit("complainOrder", orderId);
      alert(`投诉订单 ${orderId}`);
    },
    reorder(orderId) {
      // 实现“再来一单”逻辑
      this.$emit("reorder", orderId);
      alert(`再次下单 ${orderId}`);
    },
  },
});
</script>

<style scoped>
.order-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.order-card {
  padding: 16px;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-details {
  margin-top: 12px;
}

.food-list {
  margin-top: 8px;
  padding-left: 0;
  list-style: none;
}

.food-list li {
  display: flex;
  justify-content: space-between;
  padding: 4px 0;
}

.food-name {
  font-weight: bold;
}

.order-actions {
  margin-top: 12px;
  display: flex;
  gap: 8px;
}
</style>