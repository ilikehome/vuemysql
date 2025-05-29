<template>
  <div class="user-manage">
    <h2>用户管理</h2>
    
    <!-- 操作按钮 -->
    <div class="action-buttons">
      <button @click="showAddModal = true">新增用户</button>
    </div>

    <!-- 用户列表 -->
    <table class="user-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>用户名</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in userList" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>
            <button @click="handleEdit(user)">编辑</button>
            <button @click="handleDelete(user.id)">删除</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 新增/编辑模态框 -->
    <div v-if="showAddModal || showEditModal" class="modal-mask">
      <div class="modal-container">
        <h3>{{ showEditModal ? '编辑用户' : '新增用户' }}</h3>
        <input 
          v-model="formData.username" 
          placeholder="用户名" 
          required
        />
        <input 
          v-model="formData.password" 
          type="password" 
          placeholder="密码（编辑时可选）"
        />
        <div class="modal-actions">
          <button @click="submitForm">提交</button>
          <button @click="cancelForm">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { 
  getUserListApi, 
  addUserApi, 
  editUserApi, 
  deleteUserApi 
} from '@/api/user'

// 状态管理
const userStore = useUserStore()
const userList = ref<any[]>([])
const showAddModal = ref(false)
const showEditModal = ref(false)
const formData = ref({ username: '', password: '' })
const editingUserId = ref<number | null>(null)

// 加载用户列表
const loadUserList = async () => {
  try {
    const res = await getUserListApi()
    userList.value = res.data
  } catch (err) {
    console.error('Failed to load users:', err)
  }
}

// 新增/编辑提交
const submitForm = async () => {
  try {
    if (showEditModal.value) {
      await editUserApi(editingUserId.value!, formData.value)
    } else {
      await addUserApi(formData.value)
    }
    loadUserList()
    cancelForm()
  } catch (err: any) {
    alert(err.response?.data?.message || '操作失败')
  }
}

// 处理编辑
const handleEdit = (user: any) => {
  showEditModal.value = true
  formData.value = { username: user.username, password: '' }
  editingUserId.value = user.id
}

// 处理删除
const handleDelete = async (id: number) => {
  if (!confirm('确认删除该用户？')) return
  try {
    await deleteUserApi(id)
    loadUserList()
  } catch (err) {
    alert('删除失败')
  }
}

// 取消模态框
const cancelForm = () => {
  showAddModal.value = false
  showEditModal.value = false
  formData.value = { username: '', password: '' }
}

onMounted(loadUserList)
</script>

<style scoped>
.user-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
.user-table th, .user-table td {
  padding: 12px;
  border: 1px solid #e5e7eb;
  text-align: left;
}
.action-buttons {
  margin: 20px 0;
}
.modal-mask {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  min-width: 300px;
}
.modal-container input {
  width: 100%;
  padding: 8px;
  margin: 10px 0;
}
</style>