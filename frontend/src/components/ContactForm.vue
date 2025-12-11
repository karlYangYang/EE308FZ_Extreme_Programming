<script setup>
import { ref, reactive, watch } from 'vue'
import { Plus, Minus, Message, Iphone, Location, Share } from '@element-plus/icons-vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  editData: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'submit'])

const visible = ref(false)
const formRef = ref(null)

const form = reactive({
  name: '',
  is_favorite: false,
  methods: []
})

const rules = {
  name: [{ required: true, message: '请输入联系人姓名', trigger: 'blur' }]
}

const methodTypes = [
  { label: '电话', value: 'phone', icon: Iphone },
  { label: '邮箱', value: 'email', icon: Message },
  { label: '地址', value: 'address', icon: Location },
  { label: '社交媒体', value: 'social', icon: Share }
]

watch(() => props.modelValue, (val) => {
  visible.value = val
  if (val) {
    if (props.editData) {
      form.name = props.editData.name
      form.is_favorite = props.editData.is_favorite
      // Copy methods to avoid reference issues
      form.methods = props.editData.methods ? JSON.parse(JSON.stringify(props.editData.methods)) : []
    } else {
      form.name = ''
      form.is_favorite = false
      form.methods = [{ type: 'phone', value: '' }]
    }
  }
})

watch(visible, (val) => {
  emit('update:modelValue', val)
})

const addMethod = () => {
  form.methods.push({ type: 'phone', value: '' })
}

const removeMethod = (index) => {
  form.methods.splice(index, 1)
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate((valid) => {
    if (valid) {
      emit('submit', { ...form })
      visible.value = false
    }
  })
}
</script>

<template>
  <el-dialog
    v-model="visible"
    :title="editData ? '编辑联系人' : '新建联系人'"
    width="500px"
    destroy-on-close
    class="contact-dialog"
  >
    <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
      <el-form-item label="姓名" prop="name">
        <el-input v-model="form.name" placeholder="请输入姓名" size="large" />
      </el-form-item>
      
      <el-form-item label="收藏">
        <el-switch
          v-model="form.is_favorite"
          active-text="设为星标联系人"
        />
      </el-form-item>
      
      <div class="methods-section">
        <div class="section-header">
          <label class="el-form-item__label">联系方式</label>
          <el-button type="primary" link @click="addMethod">
            <el-icon><Plus /></el-icon> 添加方式
          </el-button>
        </div>
        
        <div v-for="(method, index) in form.methods" :key="index" class="method-row">
          <el-select v-model="method.type" style="width: 110px">
            <el-option
              v-for="item in methodTypes"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
              <div class="option-content">
                <el-icon><component :is="item.icon" /></el-icon>
                <span>{{ item.label }}</span>
              </div>
            </el-option>
          </el-select>
          
          <el-input 
            v-model="method.value" 
            placeholder="请输入号码/地址" 
            style="flex: 1; margin: 0 10px"
          />
          
          <el-button type="danger" circle plain size="small" @click="removeMethod(index)">
            <el-icon><Minus /></el-icon>
          </el-button>
        </div>
      </div>
    </el-form>
    
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="visible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">
          保存
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style scoped lang="scss">
.contact-dialog {
  :deep(.el-dialog) {
    border-radius: var(--radius-lg);
    overflow: hidden;
  }
  
  :deep(.el-dialog__header) {
    margin-right: 0;
    padding: 20px 24px;
    border-bottom: 1px solid var(--border-color-light);
  }
  
  :deep(.el-dialog__body) {
    padding: 24px;
  }
  
  :deep(.el-dialog__footer) {
    padding: 16px 24px;
    border-top: 1px solid var(--border-color-light);
    background-color: var(--surface-secondary);
  }
}

.methods-section {
  margin-top: 24px;
  background: var(--surface-secondary);
  padding: 20px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  
  .el-form-item__label {
    font-weight: 600;
    color: var(--text-primary);
  }
}

.method-row {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  gap: 12px;
  
  &:last-child {
    margin-bottom: 0;
  }
  
  :deep(.el-input__wrapper) {
    background-color: white;
  }
}

.option-content {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-primary);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
