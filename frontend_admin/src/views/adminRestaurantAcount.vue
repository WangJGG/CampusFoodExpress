<template>
  <div class="restaurant-account">
    <s-header :name="'商家账号管理'" :back="'/admin'" />
    <a-button type="primary" @click="$router.push('/admin')" style="margin-bottom: 10px">
      返回管理员主页
    </a-button>
    <div class="restaurant-account-box">
      <!-- 顶部的搜索框和添加商家按钮 -->
      <a-space style="margin-bottom: 10px">
        <a-input
          placeholder="输入商家名称进行搜索"
          v-model="searchId"
          @input="searchRestaurant"
        />
        <a-button type="primary" @click="openRestaurantModal('add')">添加商家</a-button>
      </a-space>

      <!-- 商家列表表格 -->
      <a-table :columns="columns" :data="filteredRestaurants" :pagination="false">
        <template #status="{ record }">
          {{ record.status }}
        </template>
        <template #qr_code="{ record }">
          <img :src="record.qr_code" alt="二维码" style="max-width: 100px; max-height: 100px" />
        </template>
        <template #image="{ record }">
          <img :src="record.image" alt="商家图片" style="max-width: 100px; max-height: 100px" />
        </template>
        <template #optional="{ record }">
          <a-space>
            <a-button type="primary" @click="openRestaurantModal('edit', record)">编辑</a-button>
            <a-button :status="record.status === 'normal' ? 'primary' : 'danger'" @click="toggleStatus(record)">
              {{ record.status === 'normal' ? '封禁' : '解禁' }}
            </a-button>
            <a-button status="danger" @click="removeRestaurant(record)">删除</a-button>
          </a-space>
        </template>
      </a-table>
    </div>

    <!-- 添加/编辑商家模态框 -->
    <a-modal
      v-model:visible="restaurantModalVisible"
      :title="modalTitle"
      @cancel="closeRestaurantModal"
      @before-ok="handleConfirm"
    >
      <a-form ref="restaurantForm" :model="restaurantFormData" :rules="rules">
        <a-form-item field="image" label="商家图片">
          <input name="image" type="file" @change="onImageFileChange" style="margin-top: 10px" />
          <img
            v-if="previewImage.url"
            :src="previewImage.url"
            alt="商家图片预览"
            class="image-preview"
          />
          <img
            v-else-if="restaurantFormData.image && typeof restaurantFormData.image === 'string'"
            :src="restaurantFormData.image"
            alt="当前商家图片"
            class="image-preview"
          />
        </a-form-item>
        <a-form-item field="name" label="商家名称">
          <a-input name="name" v-model="restaurantFormData.name" />
        </a-form-item>
        <a-form-item field="address" label="地址">
          <a-input name="address" v-model="restaurantFormData.address" @click="showMap = true" />
        </a-form-item>
        <!-- 地图弹窗 -->
        <a-modal
          v-model:visible="showMap"
          title="选择商家位置"
          :width="800"
          @cancel="showMap = false"
          :footer="null"
        >
          <!-- 地图组件 -->
          <MapComponent @address-selected="handleAddressSelected" />
        </a-modal>
        <a-form-item field="phone" label="电话">
          <a-input name="phone" v-model="restaurantFormData.phone" />
        </a-form-item>
        <a-form-item field="description" label="介绍">
          <a-input name="description" v-model="restaurantFormData.description" />
        </a-form-item>
        <a-form-item field="qr_code" label="二维码信息">
          <input name="qr_code" type="file" @change="onQrCodeFileChange" style="margin-top: 10px" />
          <img
            v-if="previewQrCode.url"
            :src="previewQrCode.url"
            alt="二维码预览"
            class="image-preview"
          />
          <img
            v-else-if="restaurantFormData.qr_code && typeof restaurantFormData.qr_code === 'string'"
            :src="restaurantFormData.qr_code"
            alt="当前二维码"
            class="image-preview"
          />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import sHeader from "@/components/SimpleHeader.vue";
import MapComponent from "@/components/MapComponent.vue";
import { ElMessage } from "element-plus";
import {
  getAllRestaurants,
  addRestaurant,
  updateRestaurant,
  deleteRestaurant,
  forbidRestaurant,
  unforbidRestaurant,
} from "@/service/restaurantService";

const rules = {
  image: [{ required: true, message: "请上传商家图片", trigger: "change" }],
  name: [{ required: true, message: "请输入商家名称", trigger: "blur" }],
  address: [{ required: true, message: "请输入地址", trigger: "blur" }],
  phone: [{ required: true, message: "请输入电话", trigger: "blur" }],
  description: [{ required: true, message: "请输入介绍", trigger: "blur" }],
  qr_code: [{ required: true, message: "请上传二维码信息", trigger: "change" }],
};

const columns = [
  { title: "ID", dataIndex: "id" },
  { title: "商家图片", slotName: "image" },
  { title: "商家名称", dataIndex: "name" },
  { title: "地址", dataIndex: "address" },
  { title: "评分", dataIndex: "rating" },
  { title: "电话", dataIndex: "phone" },
  { title: "介绍", dataIndex: "description" },
  { title: "二维码信息", slotName: "qr_code" },
  { title: "状态", slotName: "status" },
  { title: "操作", slotName: "optional" },
];

const restaurantsData = ref([]);
const filteredRestaurants = ref([]);
const searchId = ref(""); // 搜索字段（商家名称）
const restaurantFormData = reactive({
  image: "",
  name: "",
  address: "",
  phone: "",
  description: "",
  qr_code: "",
  lat: "",
  lng: "",
});
const restaurantModalVisible = ref(false);
const modalTitle = ref("");
const isEditMode = ref(false);
const showMap = ref(false); // 控制地图弹窗显示

// 用于文件预览的 reactive 对象
const previewImage = reactive({ url: null });
const previewQrCode = reactive({ url: null });

onMounted(async function () {
  try {
    const data = await getAllRestaurants();
    restaurantsData.value = data;
    filteredRestaurants.value = data;
  } catch (error) {
    ElMessage.error("获取商家数据失败");
  }
});

function searchRestaurant() {
  if (searchId.value) {
    filteredRestaurants.value = restaurantsData.value.filter(function (restaurant) {
      return restaurant.name.includes(searchId.value);
    });
  } else {
    filteredRestaurants.value = restaurantsData.value;
  }
}

function handleAddressSelected(position) {
  restaurantFormData.address = position.address; // 填入选中的地址
  restaurantFormData.lat = position.lat;
  restaurantFormData.lng = position.lng;
  showMap.value = false;
}

function openRestaurantModal(mode, record = null) {
  isEditMode.value = mode === "edit";
  modalTitle.value = isEditMode.value ? "编辑商家" : "添加商家";

  if (isEditMode.value && record) {
    Object.assign(restaurantFormData, record);
  } else {
    Object.assign(restaurantFormData, {
      image: "",
      name: "",
      address: "",
      phone: "",
      description: "",
      qr_code: "",
      lat: "",
      lng: "",
    });
  }
  restaurantModalVisible.value = true;
}

function closeRestaurantModal() {
  restaurantModalVisible.value = false;
  // 重置表单字段和预览数据
  restaurantFormData.qr_code = "";
  previewQrCode.url = null;
  restaurantFormData.image = "";
  previewImage.url = null;
  // 清空所有文件输入框的值
  var fileInputs = document.querySelectorAll('input[type="file"]');
  fileInputs.forEach(function (input) {
    input.value = "";
  });
}

function handleFileChange(event, fieldName, preview) {
  const file = event.target.files[0];
  if (file) {
    const allowedTypes = ["image/png", "image/jpg", "image/jpeg", "image/gif"];
    if (!allowedTypes.includes(file.type)) {
      ElMessage.error("只能上传 png, jpg, jpeg, gif 格式的图片文件！");
      event.target.value = "";
      return;
    }
    restaurantFormData[fieldName] = file;
    const reader = new FileReader();
    reader.onload = function (e) {
      preview.url = e.target.result;
    };
    reader.readAsDataURL(file);
  }
}

function onImageFileChange(event) {
  handleFileChange(event, "image", previewImage);
}

function onQrCodeFileChange(event) {
  handleFileChange(event, "qr_code", previewQrCode);
}

async function handleConfirm() {
  if (isEditMode.value) {
    var index = restaurantsData.value.findIndex(function (item) {
      return item.id === restaurantFormData.id;
    });
    if (index !== -1) {
      const result = await updateRestaurant(restaurantFormData.id, restaurantFormData);
      // 更新后端返回的字段（二维码、图片信息）
      restaurantFormData.qr_code = result.data.qr_code;
      restaurantFormData.image = result.data.image;
      Object.assign(restaurantsData.value[index], restaurantFormData);
    }
  } else {
    // 检查所有必填字段是否已填写
    if (
      !restaurantFormData.image ||
      !restaurantFormData.name ||
      !restaurantFormData.address ||
      !restaurantFormData.phone ||
      !restaurantFormData.description ||
      !restaurantFormData.qr_code ||
      !restaurantFormData.lat ||
      !restaurantFormData.lng
    ) {
      ElMessage.error("所有字段不能为空！");
      return;
    }
    var newRestaurant = Object.assign(
      { id: restaurantsData.value.length + 1, rating: 0 },
      restaurantFormData
    );
    const result = await addRestaurant(newRestaurant);
    newRestaurant.id = result.data.id;
    newRestaurant.qr_code = result.data.qr_code;
    newRestaurant.image = result.data.image;
    newRestaurant.status = result.data.status;
    restaurantsData.value.push(newRestaurant);
  }
  filteredRestaurants.value = restaurantsData.value;
  closeRestaurantModal();
  ElMessage.success("操作成功");
}

async function toggleStatus(restaurant) {
  var index = restaurantsData.value.findIndex(function (r) {
    return r.id === restaurant.id;
  });
  if (index !== -1) {
    var currentStatus = restaurantsData.value[index].status;
    if (currentStatus === "normal") {
      restaurantsData.value[index].status = "forbid";
      try {
        await forbidRestaurant(restaurant.id);
        ElMessage.success("封禁成功");
      } catch (error) {
        ElMessage.error("封禁失败");
      }
    } else {
      restaurantsData.value[index].status = "normal";
      try {
        await unforbidRestaurant(restaurant.id);
        ElMessage.success("解禁成功");
      } catch (error) {
        ElMessage.error("解禁失败");
      }
    }
    filteredRestaurants.value = restaurantsData.value;
  }
}

async function removeRestaurant(restaurant) {
  var index = restaurantsData.value.findIndex(function (r) {
    return r.id === restaurant.id;
  });
  if (index !== -1) {
    restaurantsData.value.splice(index, 1);
    filteredRestaurants.value = restaurantsData.value;
    try {
      await deleteRestaurant(restaurant.id);
      ElMessage.success("删除成功");
    } catch (error) {
      ElMessage.error("删除失败");
    }
  }
}
</script>

<style lang="less" scoped>
@import "../common/style/mixin";

.restaurant-account {
  box-sizing: border-box;
  padding: 20px;

  .restaurant-account-box {
    font-size: 16px;

    a {
      color: #007fff;
    }
  }
}

.image-preview {
  width: 100px;
  height: 100px;
  margin-top: 10px;
  object-fit: cover;
  border: 2px solid #ff7f32;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
