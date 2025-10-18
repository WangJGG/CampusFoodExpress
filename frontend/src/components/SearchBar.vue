<template>
    <div class="search-container">
        <!-- 直接绑定 placeholderText，避免使用 props 变量 -->
        <input type="text" class="search-input" v-model="searchQuery" :placeholder="placeholderText" />
        <button class="search-button" @click="onSearch">搜索</button>
    </div>
</template>

<script setup>
import { ref, defineProps } from 'vue';
// 使用 defineProps 来定义传递的 prop
defineProps({
    placeholderText: {
        type: String,
        default: '请输入你要搜索的内容',  // 默认值
    },
});

const searchQuery = ref('');

// 处理搜索事件
const onSearch = () => {
    console.log('搜索内容：', searchQuery.value);
};
</script>

<style scoped>
.search-container {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    max-width: 600px;
    margin: 20px auto;
}

.search-input {
    padding: 10px 20px;
    border: 2px solid #FF8A65;
    border-radius: 20px;
    background-color: white;
    font-size: 16px;
    color: #333;
    width: 75%;
    margin-right: 5px;
}

.search-button {
    padding: 10px 20px;
    background-color: #FF8A65;
    color: white;
    border: 2px solid #FF8A65;
    border-radius: 20px;
    cursor: pointer;
    font-size: 16px;
    width: 25%;
}
</style>