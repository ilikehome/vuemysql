<template>
  <div class="account-manage">
    <h2>记账管理</h2>
    
    <!-- 操作按钮（删除原退出登录按钮） -->
    <div class="action-buttons">
      <button @click="showAddModal = true">新增账目</button>
      <!-- 原退出登录按钮已移除 -->
    </div>

    <!-- 账目列表 -->
    <table class="account-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>金额</th>
          <th>类型</th>
          <th>备注</th>
          <th>创建时间</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="account in accountList" :key="account.id">
          <td>{{ account.id }}</td>
          <td>{{ account.amount }}</td>
          <td>{{ account.type }}</td>  <!-- 应显示转换后的"收入"或"支出" -->
          <td>{{ account.remark || '-' }}</td>
          <td>{{ account.created_at }}</td>
          <td>
            <button @click="handleEdit(account)">编辑</button>
            <button @click="handleDelete(account.id)">删除</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 新增/编辑模态框 -->
    <div v-if="showAddModal || showEditModal" class="modal-mask">
      <div class="modal-container">
        <h3>{{ showEditModal ? '编辑账目' : '新增账目' }}</h3>
        <input 
          v-model="formData.amount" 
          type="number" 
          placeholder="金额（必填）" 
          required
        />
        <select v-model="formData.type" required>
          <option value="">选择类型</option>
          <option value="收入">收入</option>
          <option value="支出">支出</option>
        </select>
        <input 
          v-model="formData.remark" 
          placeholder="备注（可选）"
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
  getAccountListApi, 
  addAccountApi, 
  editAccountApi, 
  deleteAccountApi 
} from '@/api/account'  // 需配套创建account.ts接口文件
import { useRouter } from 'vue-router'  // 已正确导入路由函数

// 状态管理
const userStore = useUserStore()
const router = useRouter()  // 新增：初始化路由实例
const accountList = ref<Account[]>([])
const showAddModal = ref(false)
const showEditModal = ref(false)
const formData = ref({ 
  amount: '', 
  type: '', 
  remark: '' 
})
const editingAccountId = ref<number | null>(null)

// 加载账目列表
// 加载账目列表
const loadAccountList = async () => {
  try {
    // 直接获取API返回的数组（无需通过data属性）
    const res = await getAccountListApi() as Account[]
    // 转换类型并赋值给accountList
    accountList.value = res.map(account => ({
      ...account,
      type: account.type === 'income' ? '收入' : '支出'  // 确保类型转换正确
    }))
    // 新增调试：打印确认数据是否正确赋值
    console.log('当前账目列表:', accountList.value)
  } catch (err) {
    alert('获取账目列表失败')
  }
}

// 新增/编辑提交
const submitForm = async () => {
  if (!formData.value.amount || !formData.value.type) {
    alert('金额和类型为必填项')
    return
  }

  try {
    const payload = {
      amount: Number(formData.value.amount),  // 确保转换为数字
      type: formData.value.type,
      remark: formData.value.remark
    }
    if (showEditModal.value) {
      await editAccountApi(editingAccountId.value!, payload)  // 使用转换后的payload
    } else {
      await addAccountApi(payload)  // 使用转换后的payload
    }
    loadAccountList()
    cancelForm()
  } catch (err: any) {
    alert(err.response?.data?.message || '操作失败')
  }
}

// 处理编辑
interface Account {
  id: number;
  amount: number;
  type: string;
  remark?: string;
  created_at: string;
}

const handleEdit = (account: Account) => {
  showEditModal.value = true
  formData.value = { 
    amount: String(account.amount),  // 转换为字符串以匹配表单类型
    type: account.type === 'income' ? '收入' : '支出',  // 确保中文显示
    remark: account.remark || '' 
  }
  editingAccountId.value = account.id
}

// 处理删除
const handleDelete = async (id: number) => {
  if (!confirm('确认删除该账目？')) return
  try {
    await deleteAccountApi(id)
    loadAccountList()
  } catch (err) {
    alert('删除失败')
  }
}

// 取消模态框
const cancelForm = () => {
  showAddModal.value = false
  showEditModal.value = false
  formData.value = { amount: '', type: '', remark: '' }
}

onMounted(loadAccountList)

// 新增退出登录方法
const handleLogout = () => {
  userStore.logout()
  router.push({ name: 'Login' })  // 现在可以正确访问router变量
}
</script>

<style scoped>
.account-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
.account-table th, .account-table td {
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
.modal-container input, .modal-container select {
  width: 100%;
  padding: 8px;
  margin: 10px 0;
}
</style>