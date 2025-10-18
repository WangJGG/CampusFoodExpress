<template>
  <div class="map-container">
    <div class="coordinates-display" v-if="coordinates">
      经度: {{ coordinates.lng }}, 纬度: {{ coordinates.lat }}
    </div>
    <div ref="mapContainer" class="map"></div>

    <!-- 输入框和确定按钮 -->
    <div class="form-container">
      <input
        name = "address-input"
        v-model="addressInput"
        type="text"
        placeholder="请输入地址"
        class="address-input"
        :disabled="!coordinates"
      />
      <button
        name="address-submit-button"
        @click="submitAddress"
        :disabled="!addressInput || !coordinates"
        class="submit-button"
      >
        确定
      </button>
    </div>
  </div>
</template>
    
<script setup>
import { ref, onMounted, defineEmits } from "vue";

const mapContainer = ref(null);
let map;
const addressInput = ref("");
const coordinates = ref(null);
const select = ref(null);
let selectedMarker = null; // 存储已选中的标记
// 定义自定义事件以避免警告
const emit = defineEmits(["address-selected"]); // 定义 'address-selected' 事件

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

const submitAddress = () => {
  if (coordinates.value && addressInput.value) {
    // 提交选中的地址和输入框内容
    emit("address-selected", {
      lng: select.value?.lng,
      lat: select.value?.lat,
      address: addressInput.value,
    });
  }
};

// 处理点击地图后的选点
const handleMapClick = (event) => {
  const { lng, lat } = event.lnglat;
  select.value = { lng, lat };
  selectMarker(lng, lat);
};

const initMap = (center) => {
  try {
    if (!window.AMap) {
      console.error("高德地图 API 加载失败");
      return;
    }

    map = new window.AMap.Map(mapContainer.value, {
      zoom: 20, // 初始缩放级别，再大就要申请了
      center: center || [121.215252, 31.286054], // 默认中心点
      layers: [
        new window.AMap.TileLayer(), // 默认图层
      ],
    });

    // 添加地图事件监听
    map.on("mousemove", (event) => {
      const { lng, lat } = event.lnglat;
      coordinates.value = { lng, lat };
    });

    // 监听地图点击事件
    map.on("click", handleMapClick);
  } catch (error) {
    console.error("地图初始化失败:", error);
  }
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

const selectMarker = (lng, lat) => {
  if (map) {
    // 如果已有标记，先移除之前的标记
    if (selectedMarker) {
      selectedMarker.setMap(null); // 移除已有的标记
    }

    // 添加选中位置标记
    selectedMarker = new window.AMap.Marker({
      position: new window.AMap.LngLat(lng, lat),
      title: "选中位置",
      //icon: 'https://vdata.amap.com/icons/b18/1/2.png'  // 可以自定义图标
    });

    selectedMarker.setMap(map); // 将标记添加到地图

    // 将地图中心移动到选定位置
    map.setCenter([lng, lat]);
  }
};

onMounted(async () => {
  try {
    initMap(); // 初始化地图
    getGeolocation(true); // 获取地理位置信息
  } catch (error) {
    console.error("地图初始化失败:", error);
  }
});
</script>
  
<style scoped>
.map-container {
  height: 70vh;
  display: flex;
  flex-direction: column;
}

.map {
  flex-grow: 1;
  width: 100%;
}

.coordinates-display {
  position: absolute;
  bottom: 60px;
  right: 10px;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
  z-index: 1000;
}

.form-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
}

.address-input {
  width: 250px;
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 5px;
  transition: border-color 0.3s ease;
}

.address-input:focus {
  border-color: #409eff;
  outline: none;
}

.submit-button {
  padding: 10px 20px;
  font-size: 14px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:disabled {
  background-color: #dcdfe6;
  cursor: not-allowed;
}

.submit-button:hover:not(:disabled) {
  background-color: #66b1ff;
}
</style>
  