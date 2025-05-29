const typeOptions = [
  { label: '收入', value: 'income' },  // 显示中文，但value用英文
  { label: '支出', value: 'expense' }
]

const formData = ref({
  type: 'income',  // 默认值也使用英文
  // ...其他字段
})