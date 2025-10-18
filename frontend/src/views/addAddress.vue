<template>
  <div id="add-address">
    <!-- 顶部导航栏 -->
    <div class="header">
      <button class="back-button" @click="router.push('/rewardPublish')">
        <van-icon name="arrow-left" size="24px" />
      </button>
      <h1>新增收货地址</h1>
    </div>

    <!-- 地址选择表单-->
    <form @submit.prevent="saveAddress">
      <!-- <button @click="showMap = true">选择地点</button> -->
      <!-- 输入收货地址 -->
      <div class="form-group">
        <label for="location">收货地址</label>
        <input v-model="location" type="text" placeholder="详细地址，例如某地1层101室" required />
      </div>

      <!-- 地图组件 -->
      <div v-if="showMap" class="map-modal">
        <div class="map-modal-content">
          <button class="close-button" @click="showMap = false">×</button>
          <h3>选择商家位置</h3>
          <MapComponent @address-selected="handleAddressSelected" />
        </div>
      </div>

      <!-- 标签选择 -->
      <div class="form-group">
        <label for="tag">标签</label>
        <div class="tags">
          <button v-for="tag in tags" :key="tag" type="button" :class="{ active: selectedTag === tag }"
            @click="selectTag(tag)">
            {{ tag }}
          </button>
        </div>
      </div>

      <!-- 联系人信息 -->
      <div class="form-group">
        <label for="contact">联系人</label>
        <input v-model="contactName" type="text" placeholder="请填写收货人的姓名" required />
        <div class="gender-options">
          <label><input type="radio" value="先生" v-model="contactGender" /> 先生</label>
          <label><input type="radio" value="女士" v-model="contactGender" /> 女士</label>
        </div>
      </div>

      <!-- 手机号码 -->
      <div class="form-group">
        <label for="phone">手机号</label>
        <input v-model="phone" type="text" placeholder="请填写收货手机号码" required />
      </div>

      <!-- 保存地址按钮 -->
      <button type="submit" class="save-button">保存地址</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import MapComponent from '@/components/MapComponent.vue';
import { addAddress } from '@/service/order';
import { ElMessage } from 'element-plus'

const router = useRouter();

const location = ref('');
const showMap = ref(false);
const tags = ['宿舍', '实验室', '外卖柜', '其他'];
const selectedTag = ref('');
const contactName = ref('');
const contactGender = ref('先生');
const phone = ref('');
const lat = ref(null);
const lng = ref(null);

// 选择标签
const selectTag = (tag) => {
  selectedTag.value = tag;
};

// 处理选择的地址
const handleAddressSelected = (address) => {
  location.value = address.address;
  lat.value = address.lat;
  lng.value = address.lng;
  showMap.value = false; // 关闭地图弹窗
};

// 保存地址
const saveAddress = () => {
  // 正则表达式：匹配10-15位数字
  const phoneRegex = /^[0-9]{10,15}$/;
  if (!phoneRegex.test(phone.value)) {
    ElMessage.error('手机号码格式不正确，请输入10到15位的数字');
    return;
  }

  const addressData = {
    location: location.value,
    tag: selectedTag.value,
    contactName: contactName.value,
    contactGender: contactGender.value,
    phone: phone.value,
    lat: lat.value,
    lng: lng.value,
  };
  console.log("保存的地址数据:", addressData);
  addAddress(addressData)
    .then(response => {
      if (response.status === 201) {
        ElMessage.success('地址保存成功！~');
        router.back();
      } else {
        ElMessage.error('地址保存失败，请稍后重试。');
      }
    })
    .catch(() => ElMessage.error('地址保存失败，请稍后重试。'));
};

</script>

<style scoped>
#add-address {
  font-family: Arial, sans-serif;
  background-color: #f8f4ec;
  min-height: 100vh;
  padding-bottom: 20px;
}

.header h1 {
  flex-grow: 1;
  text-align: center;
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

/* 表单样式 */
.form-group {
  margin: 20px 15px;
  background-color: #ffffff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}

.form-group label {
  font-weight: bold;
  color: #666;
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
input[type="number"],
button[type="submit"] {
  width: 100%;
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #fdfdfd;
}

/* 标签选择样式 */
.tags {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.tags button {
  padding: 5px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f8f8f8;
  cursor: pointer;
}

.tags button.active {
  background-color: #ffcc00;
  color: white;
}

/* 性别选择样式 */
.gender-options {
  margin-top: 10px;
  display: flex;
  gap: 15px;
}

/* 保存地址按钮样式 */
.save-button {
  display: block;
  width: 70%;
  max-width: 400px;
  padding: 12px;
  background-color: #ffd700;
  color: #333;
  font-size: 16px;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin: 20px auto;
  /* 设置居中 */
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease, transform 0.2s ease;
}


.save-button:hover {
  background-color: #ffcc00;
  transform: scale(1.02);
}

.save-button:active {
  background-color: #f4b400;
  transform: scale(0.98);
}

.map-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.map-modal-content {
  background: white;
  padding: 20px;
  width: 80%;
  max-width: 800px;
  border-radius: 8px;
  position: relative;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 24px;
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
}
</style>
