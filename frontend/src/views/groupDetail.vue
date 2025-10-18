<template>
  <div class="whole-page">
    <header class="header">
      <button class="back-button" @click="goBack">
        <van-icon name="arrow-left" size="18px" />
      </button>
      <span class="app-name">群聊详情</span>
    </header>

    <div class="group-chat-page">
      <!-- 群聊成员卡片 -->
      <div class="group-members-card">
        <div class="card-header">
          <h3 class="title">群聊成员 ({{ groupData.members.length }})</h3>
        </div>
        <div class="members-list">
          <div
            v-for="(member, index) in groupMembers.members"
            :key="index"
            class="member-item"
          >
            <img class="member-avatar" :src="member.avatar" alt="成员头像" />
            <!-- 仅在成员列表弹窗中显示删除按钮 -->
            <button
              v-if="isAllMembersVisible && isGroupOwner"
              @click="removeMember(index)"
              class="remove-member-btn"
            >
              删除
            </button>
          </div>
          <div
            v-if="groupData.members.length > 0"
            class="view-all-link"
            @click="viewAllMembers"
          >
            <span class="view-all">查看全部成员 ></span>
          </div>
        </div>
      </div>

      <!-- 群聊名称与公告卡片 -->
      <div class="group-details-card">
        <div class="card-header">
          <h3 class="title">群聊信息</h3>
        </div>

        <!-- 群聊头像部分 -->
        <div class="group-avatar" @click="showAvatarPreview">
          <img :src="groupData.image" alt="群聊头像" />
        </div>

        <!-- 头像预览弹窗 -->
        <div v-if="isAvatarPreviewVisible" class="avatar-preview-modal">
          <div class="avatar-preview-content">
            <img :src="groupData.image" alt="预览头像" class="preview-image" />
            <button @click="changeAvatar" class="change-avatar-btn">
              更换头像
            </button>
            <button @click="closeAvatarPreview" class="close-btn">×</button>
          </div>
        </div>

        <div class="group-name" @click="showEditModal('name')">
          <div class="label-container">
            <span class="label">群聊名称:</span>
          </div>
          <span>{{ groupData.groupName }}</span>
        </div>

        <div class="divider"></div>

        <div class="group-announcement" @click="showEditModal('announcement')">
          <div class="label-container">
            <span class="label">群公告:</span>
          </div>
          <span>{{ groupData.groupAnnouncement }}</span>
        </div>
      </div>

      <!-- 底部操作按钮 -->
      <div class="action-buttons">
        <button
          v-if="groupData.isGroupOwner"
          @click="
            router.push({
              path: '/addGroupMember',
              query: {
                id: group_id,
                memberList: JSON.stringify(groupData.members),
              },
            })
          "
          class="action-btn add-member-btn"
        >
          添加成员
        </button>
        <button
          v-if="groupData.isGroupOwner"
          @click="removeGroup"
          class="action-btn dissolve-group-btn"
        >
          解散群聊
        </button>
        <button v-else @click="leaveGroup" class="action-btn leave-group-btn">
          退出群聊
        </button>
      </div>

      <!-- 编辑群聊名称/群公告弹框 -->
      <div v-if="isModalVisible" class="modal">
        <div class="modal-content">
          <h3>{{ modalTitle }}</h3>
          <div v-if="isModalType === 'name'">
            <input
              v-model="newGroupName"
              :disabled="!groupData.isGroupOwner"
              type="text"
              placeholder="输入新的群聊名称"
            />
          </div>
          <div v-if="isModalType === 'announcement'">
            <textarea
              v-model="newGroupAnnouncement"
              :disabled="!groupData.isGroupOwner"
              placeholder="输入新的群公告内容"
            ></textarea>
          </div>
          <button v-if="groupData.isGroupOwner" @click="saveChanges">
            保存
          </button>
          <button @click="closeModal">取消</button>
        </div>
      </div>

      <!-- 所有成员列表弹窗 -->
      <div v-if="isAllMembersVisible" class="members-modal">
        <div class="modal-content">
          <h3>全部成员</h3>
          <!-- 关闭按钮 -->
          <button class="close-btn" @click="closeMembersModal">×</button>
          <div
            v-for="(member, index) in groupMembers.members"
            :key="index"
            class="member-item"
          >
            <img class="member-avatar" :src="member.avatar" alt="成员头像" />
            <span class="member-name">{{ member.nickname }}</span>
            <!-- 仅在所有成员弹窗中显示删除按钮 -->
            <button
              v-if="groupData.isGroupOwner && index !== 0"
              @click="removeMember(index)"
              class="remove-member-btn"
            >
              删除
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import {
  getGroup,
  updateGroup,
  deleteGroupMember,
  deleteGroup,
} from "@/service/group";
import { useRouter, useRoute } from "vue-router";
import { getUserInfo, getInfoById } from "@/service/user";
import { ElMessage } from "element-plus";
const route = useRoute();
const router = useRouter();

// 状态变量，用于控制头像预览的显示
const isAvatarPreviewVisible = ref(false);

// 定义一个 reactive 对象来存储所有群聊数据
const groupData = reactive({
  groupName: "",
  groupAnnouncement: "",
  isGroupOwner: false,
  owner_user_id: null,
  image: "",
  members: [],
});

const groupMembers = reactive({
  members: [],
  loading: true,
});

const state = reactive({
  user: {},
  loading: true,
});

const isModalVisible = ref(false);
const isModalType = ref("");
const modalTitle = ref("");
const newGroupName = ref("");
const newGroupAnnouncement = ref("");
const newGroupImage = ref("");
const isAllMembersVisible = ref(false);
const group_id = route.query.id;

// 显示头像预览模态框
const showAvatarPreview = () => {
  isAvatarPreviewVisible.value = true;
};

// 关闭头像预览模态框
const closeAvatarPreview = () => {
  isAvatarPreviewVisible.value = false;
};

// 头像更换的处理函数
const changeAvatar = () => {
  // 创建一个文件选择框
  const fileInput = document.createElement("input");
  fileInput.type = "file";
  fileInput.accept = "image/*"; // 限制只能选择图片文件

  // 当文件选择完成后触发
  fileInput.onchange = (event) => {
    const file = event.target.files[0]; // 获取用户选择的文件

    if (file) {
      const reader = new FileReader();

      // 读取文件并更新头像预览
      reader.onload = (e) => {
        const imageUrl = e.target.result;

        // 更新头像的预览（假设你有一个方法来更新头像预览）
        document.querySelector(".preview-image").src = imageUrl;

        // 修改 modal 类型为 'image'
        isModalType.value = "image";
        newGroupImage.value = imageUrl;

        // 调用保存更改的函数
        saveChanges();
      };

      // 读取图片文件
      reader.readAsDataURL(file);
    }
  };

  // 触发文件选择框
  fileInput.click();
};

const fetchGroupData = async () => {
  try {
    const response = await getGroup(group_id);
    const data = response.data.group;

    // 将后端返回的数据赋值给 groupData
    groupData.groupName = data.name;
    groupData.groupAnnouncement = data.description;
    groupData.owner_user_id = data.owner_user_id;
    groupData.image = data.image;
    groupData.members = data.members; // 直接替换 members 数组
    console.log("groupData.members: ", groupData.members);
  } catch (error) {
    console.error("获取群聊数据失败", error);
    ElMessage.error("获取群聊数据失败");
    goBack();
  }
};

const fetchMemberData = async () => {
  groupMembers.loading = true; // 开始加载

  try {
    // 遍历 groupData.members 数组，获取每个成员的详细信息
    const memberPromises = groupData.members.map(async (member) => {
      try {
        // 调用后端接口获取成员详细信息
        const response = await getInfoById(member.user_id);
        // 获取返回的数据
        const memberInfo = response.data;
        // 合并成员原有的信息和从后端获取的用户信息
        return memberInfo;
      } catch (error) {
        console.error(`获取成员 ${member.user_id} 信息失败`, error);
        return { ...member, error: true }; // 如果出错，添加一个 error 标志
      }
    });

    // 等待所有获取成员信息的请求完成
    const membersWithInfo = await Promise.all(memberPromises);

    // 更新 groupMembers.members，包含所有成员的详细信息
    groupMembers.members = membersWithInfo;
    groupMembers.loading = false; // 结束加载
    console.log("groupMembers.members: ", groupMembers.members);
  } catch (error) {
    console.error("获取群成员数据失败", error);
    ElMessage.error("获取群成员数据失败");
    groupMembers.loading = false; // 结束加载
  }
};

// 在组件挂载时加载数据
onMounted(async () => {
  await fetchGroupData();
  await fetchMemberData();
  const response = await getUserInfo();
  state.user = response.data;
  state.loading = false;
  console.log("user.id: ", state.user.id);
  console.log("owner_user_id: ", groupData.owner_user_id);
  if (state.user.id == groupData.owner_user_id) groupData.isGroupOwner = true;
  else groupData.isGroupOwner = false;
});

// Modal Functions
const showEditModal = (type) => {
  isModalType.value = type;
  modalTitle.value = type === "name" ? "群聊名称" : "群公告";
  if (type === "name") {
    newGroupName.value = groupData.groupName;
  } else {
    newGroupAnnouncement.value = groupData.groupAnnouncement;
  }
  isModalVisible.value = true;
};

const closeModal = () => {
  isModalVisible.value = false;
};

const saveChanges = async () => {
  let updateData = {};

  updateData.id = group_id;

  if (isModalType.value === "name") {
    updateData.name = newGroupName.value;
  } else if (isModalType.value === "announcement") {
    updateData.description = newGroupAnnouncement.value;
  } else if (isModalType.value === "image") {
    updateData.image = newGroupImage.value;
  }

  // 调用 updateGroup 函数与后端交互
  const response = await updateGroup(updateData);

  if (response.data && response.data.message === "Group updated successfully") {
    // 更新前端显示的群聊名称和公告
    if (isModalType.value === "name") {
      groupData.groupName = newGroupName.value;
    } else if (isModalType.value === "announcement") {
      groupData.groupAnnouncement = newGroupAnnouncement.value;
    } else if (isModalType.value === "image") {
      groupData.image = newGroupImage.value;
    }

    isModalVisible.value = false;
  } else {
    // 处理错误或显示失败信息
    console.error(response.data.error || "An error occurred");
  }
};

const viewAllMembers = () => {
  isAllMembersVisible.value = true;
};

const closeMembersModal = () => {
  isAllMembersVisible.value = false;
};

const removeMember = async (index) => {
  const memberId = groupData.members[index].id;

  try {
    // 调用后端删除成员接口
    const response = await deleteGroupMember(memberId);

    if (
      response.data &&
      response.data.message === "Member deleted successfully"
    ) {
      // 如果删除成功，从前端数组中移除该成员
      groupData.members.splice(index, 1);
      // 更新 groupData.members 的视图
      groupData.members = [...groupData.members]; // 用新的数组来强制更新视图

      // 如果 groupMembers.members 也需要更新
      const memberIndex = groupMembers.members.findIndex(
        (member) => member.id === memberId
      );
      groupMembers.members.splice(memberIndex, 1);
      // 强制更新 groupMembers.members 的视图
      groupMembers.members = [...groupMembers.members]; // 使用新的数组来强制更新视图
    } else {
      ElMessage.error("删除成员失败");
    }
  } catch (error) {
    console.error("删除成员失败:", error);
    ElMessage.error("删除成员失败");
  }
};

const leaveGroup = async () => {
  try {
    // 找到当前用户的成员的索引
    const memberIndex = groupMembers.members.findIndex(
      (member) => member.id === state.user.id
    );
    console.log(groupMembers.members);

    if (memberIndex !== -1) {
      // 调用 removeMember 删除当前成员
      removeMember(memberIndex);
      router.push("/main");
    } else {
      ElMessage.error("未找到该成员");
    }
  } catch (error) {
    console.error("删除成员失败:", error);
    ElMessage.error("删除成员失败");
  }
};

const removeGroup = async () => {
  try {
    // 调用后端删除群聊接口
    const response = await deleteGroup(group_id);
    console.log(response.data);
    if (
      response.data &&
      response.data.message ===
        "Group and its members and messages deleted successfully"
    ) {
      router.push("/friends");
    } else {
      ElMessage.error("删除群聊失败");
    }
  } catch (error) {
    console.error("删除群聊失败:", error);
    ElMessage.error("删除群聊失败");
  }
};

const goBack = () => {
  router.back();
};
</script>

<style scoped>
.group-chat-page {
  padding: 20px;
  background-color: #f4f7fb;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 420px;
  margin: 20px auto;
}

.back-button-right {
  position: absolute;
  top: 30px;
  /* 可以增加为 30px 或更多 */
  margin-bottom: 60px;
  /* 增大按钮下方的间距 */
  right: 20px;
  font-size: 24px;
  /* 增大字体 */
  font-weight: 500;
  color: #007bff;
  cursor: pointer;
  transition: color 0.3s ease;
}

.back-button-right:hover {
  color: #0056b3;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  /* 为卡片头部和其他内容之间添加间距 */
}

.title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.group-members-card,
.group-details-card {
  margin-bottom: 15px;
  background-color: #ffffff;
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.group-avatar img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
}

.members-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.member-item {
  display: flex;
  align-items: center;
}

.member-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 10px;
}

.member-name {
  font-size: 14px;
  color: #666;
}

.view-all-link {
  margin-top: 12px;
  text-align: center;
}

.view-all {
  color: #007bff;
  cursor: pointer;
}

/* 群聊名称与群公告 */

.group-avatar {
  margin-bottom: 15px;
  /* 为群聊头像和群聊名称之间添加间距 */
  /* text-align: center; 可选：使头像居中 */
}

.group-name,
.group-announcement {
  margin-bottom: 18px;
}

.label-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.group-name .label,
.group-announcement .label {
  font-weight: bold;
  color: #444;
}

/* 群公告显示样式 */
.group-name span,
.group-announcement span {
  display: -webkit-box;
  /* 创建多行文本区域 */
  -webkit-box-orient: vertical;
  /* 设置为垂直方向的盒子布局 */
  -webkit-line-clamp: 5;
  /* 限制最大显示 5 行 */
  overflow: hidden;
  /* 隐藏超出的部分 */
  text-overflow: ellipsis;
  /* 使用省略号表示超出部分 */
  word-wrap: break-word;
  /* 允许长单词换行 */
  white-space: normal;
  /* 允许文本换行 */
  width: 100%;
  /* 让 span 宽度为 100%，适应父容器 */
  color: #777;
  line-clamp: 5;
  /* 适应标准属性 */
}

/* divider 样式 */
.divider {
  margin: 12px 0;
  border-bottom: 1px solid #f1f1f1;
}

/* 美化底部按钮 */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.action-btn {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 12px;
  padding: 12px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s ease, transform 0.3s ease;
}

.action-btn:hover {
  background-color: #0056b3;
}

.action-btn:active {
  transform: translateY(2px);
}

/* 区分不同按钮 */
.add-member-btn {
  background: linear-gradient(145deg, #4caf50, #388e3c);
}

.dissolve-group-btn {
  background: linear-gradient(145deg, #ff5722, #ff3d00);
}

.leave-group-btn {
  background: linear-gradient(145deg, #ffcc00, #ffbb00);
}

/* 编辑框样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  /* 半透明黑色背景，保持阴影效果 */
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 编辑弹窗的背景颜色 */
.modal-content {
  background: #f5f5f5;
  /* 淡灰色背景 */
  padding: 20px;
  border-radius: 10px;
  width: 400px;
  max-height: 80%;
  overflow-y: auto;
}

.modal h3 {
  font-size: 20px;
  margin-bottom: 20px;
  color: #333;
}

.modal input,
/* 编辑群公告的文本框样式 */
.modal textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  line-height: 1.5;
  min-height: 150px;
  /* 固定的最小高度 */
  max-height: 200px;
  /* 固定的最大高度 */
  resize: none;
  /* 禁用调整大小 */
  overflow-y: auto;
  /* 超出部分显示滚动条 */
  box-sizing: border-box;
}

/* 如果文本框的内容超过最大高度时，显示垂直滚动条 */
.modal textarea::-webkit-scrollbar {
  width: 8px;
  /* 设置滚动条宽度 */
}

.modal textarea::-webkit-scrollbar-thumb {
  background-color: #888;
  /* 滚动条的颜色 */
  border-radius: 4px;
}

.modal textarea::-webkit-scrollbar-thumb:hover {
  background-color: #555;
  /* 鼠标悬停时滚动条颜色 */
}

.modal input:focus,
.modal textarea:focus {
  border-color: #ffcc00;
  /* 聚焦时的黄色边框 */
}

/* 编辑弹窗按钮样式 */
.modal button {
  background: linear-gradient(145deg, #ffe066, #ffcc33);
  /* 适中的黄色渐变背景 */
  color: white;
  border: none;
  border-radius: 30px;
  /* 圆角 */
  padding: 12px 20px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  transition: transform 0.3s ease, background 0.3s ease;
  /* 平滑的交互效果 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  /* 阴影效果 */
  width: 100%;
  margin-top: 10px;
  /* 按钮间距 */
}

/* 按钮悬停效果 */
.modal button:hover {
  transform: translateY(-4px);
  /* 鼠标悬停时的上浮效果 */
  background: linear-gradient(145deg, #ffcc33, #ffe066);
  /* 悬停时渐变方向变化 */
}

/* 按钮点击效果 */
.modal button:active {
  transform: translateY(2px);
  /* 点击时按钮下沉 */
}

/* 保存按钮和取消按钮的颜色区分 */
.modal button:first-child {
  background: linear-gradient(145deg, #66bb6a, #4caf50);
  /* 适中的绿色渐变 */
}

.modal button:first-child:hover {
  background: linear-gradient(145deg, #4caf50, #66bb6a);
  /* 悬停时反向渐变 */
}

.modal button:last-child {
  background: linear-gradient(145deg, #ff7043, #ff5722);
  /* 适中的红色渐变 */
}

.modal button:last-child:hover {
  background: linear-gradient(145deg, #ff5722, #ff7043);
  /* 悬停时反向渐变 */
}

/* 处理“查看全部成员”弹窗 */
.members-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 所有成员列表弹窗 */
.members-modal .modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  max-width: 400px;
  width: 100%;
  max-height: 80%;
  overflow-y: auto;
}

/* 成员列表样式 */
.members-modal .members-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  /* 成员之间的垂直间距 */
}

/* 每个成员项的样式 */
.members-modal .member-item {
  display: flex;
  align-items: center;
  padding: 8px 0;
  /* 每个成员上下的间距 */
  border-bottom: 1px solid #f1f1f1;
  /* 分隔线 */
}

/* 成员头像 */
.members-modal .member-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 10px;
}

/* 删除按钮样式 */
.members-modal .remove-member-btn {
  background: linear-gradient(145deg, #ff6b6b, #ff4c4c);
  /* 红色渐变背景 */
  color: white;
  border: none;
  border-radius: 50%;
  /* 圆形按钮 */
  padding: 8px 12px;
  font-size: 14px;
  cursor: pointer;
  position: absolute;
  right: 10px;
  /* 将按钮定位到右上角 */
  top: 50%;
  transform: translateY(-50%);
  /* 垂直居中 */
  transition: background 0.3s ease, transform 0.3s ease;
}

/* 所有成员列表弹窗的关闭按钮样式 */
.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: none;
  font-size: 24px;
  color: #333;
  cursor: pointer;
}

.close-btn:hover {
  color: #ff5722;
}

/* 删除按钮仅在成员列表弹窗中显示 */

/* 普通成员列表中的删除按钮不显示 */
.group-members-card .remove-member-btn {
  display: none;
}

/* 头像预览模态框样式 */
.avatar-preview-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  /* 背景半透明 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  /* 确保模态框在所有元素之上 */
}

.avatar-preview-content {
  background: white;
  padding: 30px;
  /* 增加内边距，使弹框更大 */
  border-radius: 12px;
  text-align: center;
  width: 400px;
  /* 增大弹窗宽度 */
  height: auto;
  /* 高度自适应 */
}

/* 头像预览样式 */
.preview-image {
  width: 200px;
  /* 增大头像尺寸 */
  height: 200px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 20px;
}

/* 更换头像按钮样式 */
.change-avatar-btn {
  background: linear-gradient(145deg, #ff9800, #f57c00);
  color: white;
  border: none;
  border-radius: 30px;
  padding: 12px 20px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  transition: transform 0.3s ease;
  margin-top: 20px;
  /* 增加按钮与头像之间的间距 */
  width: 100%;
  /* 使按钮占满弹框宽度 */
}

.change-avatar-btn:hover {
  transform: translateY(-4px);
}

/* 关闭按钮样式 */
.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: none;
  color: black;
  font-size: 24px;
  cursor: pointer;
}
</style>
