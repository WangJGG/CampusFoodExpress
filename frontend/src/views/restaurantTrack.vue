<template>
  <div class="whole-page">
    <header class="header">
      <button class="back-button" @click="goBack">
        <van-icon name="arrow-left" size="18px" />
      </button>
      <div class="title">
        <span class="app-name">我的足迹</span>
      </div>
    </header>
    <div class="search-bar">
      <div class="search-container">
        <input
          type="text"
          class="search-input"
          v-model="searchQuery"
          placeholder="搜索足迹~~"
        />
        <button class="search-button" @click="searchResturants">搜索</button>
      </div>
    </div>

    <div class="map-page">
      <div class="coordinates-display" v-if="coordinates">
        经度: {{ coordinates.lng }}, 纬度: {{ coordinates.lat }}
      </div>
      <div ref="mapContainer" class="map-container"></div>

      <!-- 滑动上拉框 -->
      <div
        class="sliding-panel"
        :class="{ open: panelOpen, partial: !panelOpen }"
        @touchstart="startTouch"
        @touchmove="moveTouch"
        @touchend="endTouch"
      >
        <div class="panel-header" @click="togglePanel">
          <span class="panel-title">
            <i class="fa fa-utensils"></i> 我下过单的餐馆
          </span>
        </div>
        <div class="panel-content">
          <div
            v-if="Object.keys(state.restaurants).length === 0"
            class="empty-message"
          >
            您还没有下过馆子哦~ <span class="emoji">🍽️</span>
          </div>
          <div
            v-else
            v-for="(restaurant, id) in state.restaurants"
            :key="id"
            class="restaurant-item"
            @click="locateRestaurant(restaurant.id)"
          >
            <h4 class="restaurant-name">{{ restaurant.name }}</h4>
            <p class="restaurant-address">
              <i class="fa fa-map-marker-alt"></i> 地址:
              {{ restaurant.address }}
            </p>
            <p class="restaurant-phone">
              <i class="fa fa-phone-alt"></i> 电话: {{ restaurant.phone }}
            </p>
            <p class="restaurant-orders">
              <i class="fa fa-utensils"></i> 下单次数:
              {{ restaurant.orderCount }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { reactive, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { getOrdersByUser } from "@/service/order";
import { getRestaurantById } from "@/service/restaurantService";
import { ElMessage } from 'element-plus'

const router = useRouter();

const state = reactive({
  markers: [],
  restaurants: {},
  loading: true,
});

let map;
const mapContainer = ref(null);
const coordinates = ref(null);
const searchQuery = ref("");
const targetID = ref(-1);
const panelOpen = ref(false); // 控制上拉框是否展开
let startY = 0;

onMounted(async () => {
  await getAllMarkers();  // 获取标记数据
  initMap();              // 初始化地图
  getGeolocation(true);   // 获取用户定位
});

// 切换上拉框的展开和关闭
const togglePanel = () => {
  panelOpen.value = !panelOpen.value;
};

// 手势滑动逻辑
const startTouch = (event) => {
  startY = event.touches[0].clientY;
};

const moveTouch = (event) => {
  const currentY = event.touches[0].clientY;
  const deltaY = currentY - startY;

  if (deltaY < -50) {
    // 上滑超过50px，展开上拉框
    panelOpen.value = true;
  } else if (deltaY > 50) {
    // 下滑超过50px，收起上拉框
    panelOpen.value = false;
  }
};

const endTouch = () => {
  // 滑动结束后的处理逻辑
};

// 定位餐馆到地图中心并收起上拉框
const locateRestaurant = (restaurantId) => {
  const restaurant = state.restaurants[restaurantId];
  if (restaurant && map) {
    console.log("restaurant LNG : ", restaurant.lng);
    map.setCenter([restaurant.lng, restaurant.lat]);
    //map.setCenter(new window.AMap.LngLat(restaurant.lng, restaurant.lat));
    panelOpen.value = false; // 收起上拉框到初始状态
  }
};

// 坐标转换函数
function wgs84togcj02(wgsLat, wgsLng) {
  if (outOfChina(wgsLat, wgsLng)) {
    return [wgsLng, wgsLat];
  }
  const dLat = transformLat(wgsLng - 105.0, wgsLat - 35.0);
  const dLng = transformLng(wgsLng - 105.0, wgsLat - 35.0);
  const radLat = (wgsLat / 180.0) * Math.PI;
  const magic = Math.sin(radLat);
  const magic2 = 1 - 0.00669342162296594323 * magic * magic;
  const sqrtMagic = Math.sqrt(magic2);
  const deltaLat =
    (dLat * 180.0) /
    (((6378137.0 * (1 - 0.00669342162296594323)) / (magic2 * sqrtMagic)) *
      Math.PI);
  const deltaLng =
    (dLng * 180.0) / ((6378137.0 / sqrtMagic) * Math.cos(radLat) * Math.PI);
  const mgLat = wgsLat + deltaLat;
  const mgLng = wgsLng + deltaLng;
  return [mgLng, mgLat];

  function outOfChina(lat, lon) {
    if (lon < 72.004 || lon > 137.8347) return true;
    if (lat < 0.8293 || lat > 55.8271) return true;
    return false;
  }

  function transformLat(x, y) {
    let ret =
      -100.0 +
      2.0 * x +
      3.0 * y +
      0.2 * y * y +
      0.1 * x * y +
      0.2 * Math.sqrt(Math.abs(x));
    ret +=
      ((20.0 * Math.sin(6.0 * x * Math.PI) +
        20.0 * Math.sin(2.0 * x * Math.PI)) *
        2.0) /
      3.0;
    ret +=
      ((20.0 * Math.sin(y * Math.PI) + 40.0 * Math.sin((y / 3.0) * Math.PI)) *
        2.0) /
      3.0;
    ret +=
      ((160.0 * Math.sin((y / 12.0) * Math.PI) +
        320 * Math.sin((y * Math.PI) / 30.0)) *
        2.0) /
      3.0;
    return ret;
  }

  function transformLng(x, y) {
    let ret =
      300.0 +
      x +
      2.0 * y +
      0.1 * x * x +
      0.1 * x * y +
      0.1 * Math.sqrt(Math.abs(x));
    ret +=
      ((20.0 * Math.sin(6.0 * x * Math.PI) +
        20.0 * Math.sin(2.0 * x * Math.PI)) *
        2.0) /
      3.0;
    ret +=
      ((20.0 * Math.sin(x * Math.PI) + 40.0 * Math.sin((x / 3.0) * Math.PI)) *
        2.0) /
      3.0;
    ret +=
      ((150.0 * Math.sin((x / 12.0) * Math.PI) +
        300.0 * Math.sin((x / 30.0) * Math.PI)) *
        2.0) /
      3.0;
    return ret;
  }
}

const initMap = (center) => {
  if (!window.AMap) {
    console.error("高德地图 API 加载失败");
    return;
  }

  map = new window.AMap.Map(mapContainer.value, {
    zoom: 20, // 初始缩放级别，再大就要申请了
    center: center || [121.215252, 31.286054], // 默认中心点
    layers: [
      new window.AMap.TileLayer(), // 默认图层
      // new window.AMap.TileLayer.Satellite()  // 卫星图层
    ],
  });

  map.on("mousemove", (event) => {
    const { lng, lat } = event.lnglat;
    coordinates.value = { lng, lat };
  });

  state.markers.forEach((markerData) => {
    const marker = new window.AMap.Marker({
      position: new window.AMap.LngLat(markerData.lng, markerData.lat),
      title: markerData.name,
      // offset: new window.AMap.Pixel(-13, -30),  // 调整标记的位置
      // content: `<img src="${markerData.icon}" style="width: 26px; height: 52px;" />`  // 自定义标记图标
    });
    marker.setMap(map);

    const infoWindow = new window.AMap.InfoWindow({
      content: `<div style="padding:10px;">
                  <h3>${markerData.name}</h3>
                  <p>地址: ${markerData.address}</p>
                  <p>电话: ${markerData.phone}</p>
                  <p>下单次数: ${
                    state.restaurants[markerData.id].orderCount
                  }</p>
                  <button onclick="handleDetailsClick('${
                    markerData.id
                  }')">查看详情</button>
                </div>`,
      offset: new window.AMap.Pixel(0, -30), // 调整信息窗口的位置
    });

    marker.on("click", () => {
      infoWindow.open(map, marker.getPosition());
    });
  });

  state.loading = false;
};

const getGeolocation = (resetCenter) => {
  if (!window.AMap) {
    console.error("高德地图 API 加载失败");
    return;
  }

  window.AMap.plugin("AMap.Geolocation", function () {
    const geolocation = new window.AMap.Geolocation({
      enableHighAccuracy: true, // 是否使用高精度定位，默认:true
      timeout: 10000, // 超过10秒后停止定位，默认：无穷大
      maximumAge: 0, // 定位结果缓存0毫秒，默认：0
      convert: true, // 自动偏移坐标，偏移后的坐标为高德坐标，默认：true
      showButton: true, // 显示定位按钮，默认：true
      buttonPosition: "LT", // 定位按钮停靠位置，默认：'LB'，左下角
      buttonOffset: new window.AMap.Pixel(50, 50), // 定位按钮与设置的停靠位置的偏移量，默认：Pixel(10, 20)
      showMarker: true, // 定位成功后在定位点显示默认图标，默认：true
      showCircle: true, // 定位成功后用圆圈表示定位精度范围，默认：true
      panToLocation: true, // 定位成功后将定位到的地图中心，默认：true
      zoomToAccuracy: true, // 定位成功后调整地图视野范围使定位位置及精度范围视野内可见，默认：false
      needAddress: true,
    });
    //map.addControl(geolocation);  // 将定位插件添加到地图实例

    geolocation.getCurrentPosition((status, result) => {
      if (status === "complete") {
        const { position } = result;
        const { lat, lng } = position;
        const [gcjLng, gcjLat] = wgs84togcj02(lat, lng); // 注意参数的顺序！！！
        console.log("成功获取当前位置:", { lat: gcjLat, lng: gcjLng });
        if (resetCenter) initMap([gcjLng, gcjLat]);

        // 添加用户位置标记
        addUserMarker(gcjLng, gcjLat, resetCenter);
      } else {
        console.error("获取地理位置失败，请检查网络连接和GPS状态");
        initMap(); // 使用默认中心点
      }
    });
  });
};

const addUserMarker = (lng, lat, resetCenter) => {
  if (map) {
    // 清除现有的用户位置标记
    map.remove(
      map
        .getLayers()
        .filter(
          (layer) =>
            layer instanceof window.AMap.Marker &&
            layer.getTitle() === "当前位置"
        )
    );

    // 添加新的用户位置标记
    const userMarker = new window.AMap.Marker({
      position: new window.AMap.LngLat(lng, lat),
      title: "当前位置",
      icon: "https://vdata.amap.com/icons/b18/1/2.png", // 可以自定义图标
    });
    userMarker.setMap(map);

    if (resetCenter)
      // 将地图中心移动到用户位置
      map.setCenter([lng, lat]);
  }
};

const goBack = () => {
  router.back();
};

const getAllMarkers = async () => {
  try {
    const tmp = {
      markers: [],
      restaurants: {},
    };
    const orderList = await getOrdersByUser();
    // 遍历 orderList.data 并逐个获取 marker 详情
    for (const order of orderList.data) {
      const restaurantId = order.restaurant_id;

      if (!tmp.restaurants[restaurantId]) {
        const response = await getRestaurantById(restaurantId);
        tmp.restaurants[restaurantId] = {
          id: restaurantId,
          name: response.data.name,
          address: response.data.address,
          phone: response.data.phone,
          orderCount: 0,
          lat: response.data.lat,
          lng: response.data.lng,
        };
        tmp.markers.push(response.data);
      }
      tmp.restaurants[restaurantId].orderCount += 1;
    }
    state.markers = tmp.markers;
    state.restaurants = tmp.restaurants;
  } catch (error) {
    console.error("获取标记数据失败:", error);
  }
};

const searchResturants = async () => {
  const query = searchQuery.value.trim().toLowerCase(); // 将查询转换为小写以实现大小写不敏感匹配
  if (query === "") {
    getAllMarkers();
    getGeolocation(true);
    return;
  }

  try {
    for (const restaurant of state.markers) {
      if (restaurant.name.toLowerCase().includes(query)) {
        targetID.value = restaurant.id;
        break;
      }
    }

    // 重新初始化地图标记
    getGeolocation(false);
    initMap([
      state.restaurants[targetID.value].lng,
      state.restaurants[targetID.value].lat,
    ]);
  } catch (error) {
    ElMessage.error('您好像没有去过您搜索的餐馆哦~');
    
    console.error("搜索标记数据失败:", error);
  }
};

const handleDetailsClick = async (MerchantId) => {
  try {
    // 处理后端响应，例如跳转到新页面
    router.push({ path: "/merchantDetail", query: { id: MerchantId } });
  } catch (error) {
    console.error("请求失败:", error);
  }
};

// 将 handleDetailsClick 注册为全局方法
window.handleDetailsClick = handleDetailsClick;
</script>

<style scoped>
.search-bar {
  display: flex;
  align-items: center;
  /* 垂直居中 */
  gap: 10px;
  /* 子元素之间的间距 */
}

.search-input {
  width: 100%;
  border: none;
  /* 移除边框 */
  outline: none;
  /* 移除焦点时的边框效果 */
  padding: 10px;
  font-size: 16px;
  border-radius: 20px;
  /* 确保圆角边框一致 */
  background-color: transparent;
  /* 确保背景与容器一致 */
}

.search-container {
  background-color: #fff8dc;
  /* 确保容器背景色一致 */
  border-radius: 20px;
  padding: 5px;
  /* 避免内边距过多导致视觉错位 */
  border: 1px solid #ccc;
  /* 设置单一边框 */
  box-sizing: border-box;
  /* 确保边框和内边距包含在宽度中 */
}

.app-name {
  font-size: 22px;
  color: black;
  font-weight: bold;
  white-space: nowrap;
  /* 防止文本换行 */
  margin-left: auto;
  /* 推到最右侧 */
}

.map-page {
  height: 80vh;
  /* 设置父元素高度为视口高度 */
  display: flex;
  flex-direction: column;
}

.map-container {
  flex-grow: 1;
  /* 占据剩余空间 */
  width: 100%;
  position: relative;
  /* 确保地图容器内的元素定位正确 */
}

.van-tabbar {
  margin-top: auto;
  /* 固定在底部 */
}

/* 确保地图容器的高度不被底部导航栏覆盖 */
.map-container::before {
  content: "";
  display: block;
  height: 50px;
  /* 底部导航栏的高度 */
}

.coordinates-display {
  position: absolute;
  bottom: 60px;
  /* 调整位置以避开底部导航栏 */
  right: 10px;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
  z-index: 1000;
}

/* 底部上拉框 */

.sliding-panel {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #fff;
  border-top-left-radius: 25px;
  border-top-right-radius: 25px;
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  z-index: 1001;
  height: 67vh;
}

/* 初始状态，仅部分面板可见，约为屏幕的 20% 上方 */
.sliding-panel.partial {
  transform: translateY(calc(67vh - 20vh));
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
}

/* 完全展开状态 */
.sliding-panel.open {
  transform: translateY(0);
  box-shadow: 0 -8px 16px rgba(0, 0, 0, 0.3);
}

/* 面板头部样式，便于用户点击 */
.panel-header {
  padding: 15px;
  background: #ee8534;
  /* 添加颜色渐变效果 */
  color: #fff;
  /* 设置字体颜色为白色，提升可读性 */
  text-align: center;
  cursor: pointer;
  border-top-left-radius: 25px;
  border-top-right-radius: 25px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 拖动手柄 */
.drag-handle {
  width: 50px;
  height: 5px;
  background: #888;
  border-radius: 5px;
  position: absolute;
  top: 8px;
  left: 50%;
  transform: translateX(-50%);
  opacity: 0.7;
}

/* 面板标题样式 */
.panel-title {
  font-size: 18px;
  font-weight: bold;
  display: flex;
  align-items: center;
}

/* 面板标题中的图标样式 */
.panel-title .fa-utensils {
  margin-right: 10px;
  font-size: 20px;
  /* 使图标稍微大一点 */
  color: #fff;
}

/* 面板内容部分，最大高度设置，并且允许滚动 */
.panel-content {
  padding: 15px;
  max-height: calc(67vh - 70px);
  overflow-y: auto;
}

/* 美化后的餐馆列表项样式 */
.restaurant-item {
  margin-bottom: 15px;
  padding: 15px;
  background: #fefefe;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
  cursor: pointer;
}

.restaurant-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.restaurant-name {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.restaurant-address,
.restaurant-phone,
.restaurant-orders {
  font-size: 14px;
  color: #666;
  margin-top: 5px;
  display: flex;
  align-items: center;
}

/* 空消息样式 */
.empty-message {
  text-align: center;
  font-size: 18px;
  margin-top: 20px;
  color: #777;
}

.emoji {
  font-size: 24px;
}
</style>