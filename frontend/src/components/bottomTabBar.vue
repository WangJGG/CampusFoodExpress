<template>
  <van-tabbar v-model="activeTab" fixed>
    <van-tabbar-item icon="home-o" @click="goTo('/main')">首页</van-tabbar-item>
    <van-tabbar-item icon="location-o" @click="goTo('/foodMap')"
      >地图</van-tabbar-item
    >
    <van-tabbar-item icon="orders-o" @click="goTo('/foodOrder')"
      >订单</van-tabbar-item
    >
    <van-tabbar-item icon="friends-o" @click="goTo('/friends')"
      >消息</van-tabbar-item
    >
    <van-tabbar-item icon="user-o" @click="goTo('/userPage')"
      >我的</van-tabbar-item
    >
  </van-tabbar>
</template>
  
  <script setup>
import { useRouter } from "vue-router";

import { ref, watch } from "vue";

const props = defineProps({
  active: {
    type: Number,
    default: 0,
  },
});
const router = useRouter();
// 使用一个本地变量来绑定 v-model
const activeTab = ref(props.active);

// 监听 props.active 的变化，并更新本地变量
watch(
  () => props.active,
  (newValue) => {
    activeTab.value = newValue;
  }
);

// 定义方法
const goTo = (path) => {
  // 使用 Vue Router 的编程式导航跳转到指定路径
  router.push(path);
};
</script>