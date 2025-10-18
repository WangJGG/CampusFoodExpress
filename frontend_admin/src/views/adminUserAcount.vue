<template>
  <div class="user-account">
    <sHeader :name="'用户账号管理'" :back="'/admin'" />
    <a-button type="primary" @click="goTo('/admin')" style="margin-bottom: 10px">
      返回管理员主页
    </a-button>

    <div class="user-account-box">
      <!-- 顶部的搜索框 -->
      <a-space style="margin-bottom: 10px">
        <a-input
          placeholder="输入用户账号进行搜索"
          v-model="searchId"
          @input="searchUser"
        />
      </a-space>

      <!-- 用户列表表格 -->
      <a-table :columns="columns" :data="filteredUsers" :pagination="false">
        <template #status="{ record }">
          {{ record.status }}
        </template>
        <template #avatar="{ record }">
          <img :src="record.avatar" alt="头像" style="max-width: 100px; max-height: 100px;" />
        </template>
        <template #optional="{ record }">
          <a-space>
            <a-button
              :status="record.status === 'normal' ? 'primary' : 'danger'"
              @click="toggleBan(record)"
            >
              {{ record.status === 'normal' ? '封禁' : '解禁' }}
            </a-button>
            <a-button status="danger" @click="removeUser(record)">删除</a-button>
          </a-space>
        </template>
      </a-table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import sHeader from '@/components/SimpleHeader.vue'
import { getUser, banUser, unbanUser, deleteUser } from '@/service/admin'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const columns = [
  { title: "ID", dataIndex: "id" },
  { title: "头像", slotName: "avatar" },
  { title: "昵称", dataIndex: "nickname" },
  { title: "账号", dataIndex: "phone" },
  { title: "签名", dataIndex: "bio" },
  { title: "状态", slotName: "status" },
  { title: "操作", slotName: "optional" }
]

const usersData = ref([])
const filteredUsers = ref([])
const searchId = ref('')
const router = useRouter()

onMounted(async () => {
  try {
    const { data } = await getUser()
    usersData.value = data
    filteredUsers.value = data
  } catch (error) {
    ElMessage.error("获取用户数据失败")
  }
})

function searchUser() {
  if (searchId.value) {
    filteredUsers.value = usersData.value.filter(user =>
      user.phone.includes(searchId.value)
    )
  } else {
    filteredUsers.value = usersData.value
  }
}

async function toggleBan(user) {
  const index = usersData.value.findIndex(u => u.id === user.id)
  if (index !== -1) {
    const currentStatus = usersData.value[index].status
    if (currentStatus === 'normal') {
      usersData.value[index].status = 'forbided'
      try {
        await banUser(user.id)
        ElMessage.success("封禁成功")
      } catch (error) {
        ElMessage.error("封禁失败")
      }
    } else {
      usersData.value[index].status = 'normal'
      try {
        await unbanUser(user.id)
        ElMessage.success("解禁成功")
      } catch (error) {
        ElMessage.error("解禁失败")
      }
    }
    filteredUsers.value = usersData.value
  }
}

async function removeUser(user) {
  const index = usersData.value.findIndex(u => u.id === user.id)
  if (index !== -1) {
    try {
      await deleteUser(user.id)
      usersData.value.splice(index, 1)
      filteredUsers.value = usersData.value
      ElMessage.success("删除成功")
    } catch (error) {
      ElMessage.error("删除失败")
    }
  }
}

function goTo(path) {
  router.push(path)
}
</script>

<style lang="less" scoped>
@import '../common/style/mixin';

.user-account {
  box-sizing: border-box;
  padding: 20px;

  .user-account-box {
    font-size: 16px;

    a {
      color: #007fff;
    }
  }
}
</style>
