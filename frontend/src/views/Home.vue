<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { 
  getContacts, createContact, updateContact, deleteContact, 
  toggleFavorite, exportContacts, importContacts 
} from '@/api/contacts'
import { 
  Plus, Search, Star, StarFilled, Download, Upload, 
  Delete, Edit, More, UserFilled, Phone, Message, Location, Share,
  SwitchButton, ArrowDown
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import ContactForm from '@/components/ContactForm.vue'

const router = useRouter()
const userStore = useUserStore()

const contacts = ref([])
const loading = ref(false)
const searchQuery = ref('')
const showFavoritesOnly = ref(false)

const showContactDialog = ref(false)
const editingContact = ref(null)
const importInput = ref(null)

const filteredContacts = computed(() => {
  return contacts.value.filter(contact => {
    // Search filter
    const matchSearch = searchQuery.value 
      ? contact.name.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
        contact.methods.some(m => m.value.toLowerCase().includes(searchQuery.value.toLowerCase()))
      : true
    
    // Favorite filter
    const matchFavorite = showFavoritesOnly.value ? contact.is_favorite : true
    
    return matchSearch && matchFavorite
  })
})

const fetchContacts = async () => {
  loading.value = true
  try {
    const res = await getContacts()
    contacts.value = res.contacts
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}

const handleCreate = () => {
  editingContact.value = null
  showContactDialog.value = true
}

const handleEdit = (contact) => {
  editingContact.value = contact
  showContactDialog.value = true
}

const handleSubmit = async (formData) => {
  try {
    if (editingContact.value) {
      await updateContact(editingContact.value.id, formData)
      ElMessage.success('更新成功')
    } else {
      await createContact(formData)
      ElMessage.success('创建成功')
    }
    fetchContacts()
  } catch (error) {
    console.error(error)
  }
}

const handleDelete = (contact) => {
  ElMessageBox.confirm(
    `确定要删除联系人 "${contact.name}" 吗?`,
    '警告',
    {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(async () => {
    try {
      await deleteContact(contact.id)
      ElMessage.success('删除成功')
      fetchContacts()
    } catch (error) {
      console.error(error)
    }
  })
}

const handleToggleFavorite = async (contact) => {
  try {
    await toggleFavorite(contact.id)
    contact.is_favorite = !contact.is_favorite
    // Resort or refresh might be needed if sorting by favorite
    fetchContacts() 
  } catch (error) {
    console.error(error)
  }
}

const handleExport = async () => {
  try {
    const blob = await exportContacts()
    const url = window.URL.createObjectURL(new Blob([blob]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `通讯录_${new Date().toISOString().slice(0,10)}.xlsx`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch (error) {
    ElMessage.error('导出失败')
    console.error(error)
  }
}

const triggerImport = () => {
  importInput.value.click()
}

const handleImport = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  const formData = new FormData()
  formData.append('file', file)
  
  try {
    const res = await importContacts(formData)
    ElMessage.success(res.message)
    fetchContacts()
  } catch (error) {
    ElMessage.error('导入失败')
  } finally {
    event.target.value = '' // Reset input
  }
}

const getMethodIcon = (type) => {
  const map = {
    phone: Phone,
    email: Message,
    address: Location,
    social: Share
  }
  return map[type] || Message
}

const getMethodLabel = (type) => {
    const map = {
    phone: '电话',
    email: '邮箱',
    address: '地址',
    social: '社交'
  }
  return map[type] || type
}

// Generate consistent color from string
const stringToColor = (str) => {
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash)
  }
  const hue = Math.abs(hash) % 360
  return `hsl(${hue}, 65%, 55%)`
}

onMounted(() => {
  fetchContacts()
})
</script>

<template>
  <div class="home-container">
    <!-- Glassmorphic Navbar -->
    <nav class="navbar glass-panel">
      <div class="nav-content">
        <div class="logo">
          <div class="logo-icon">
            <el-icon><UserFilled /></el-icon>
          </div>
          <span class="logo-text">Address Book</span>
        </div>
        
        <div class="user-menu">
          <el-dropdown trigger="click" @command="handleLogout">
            <div class="user-dropdown-trigger">
              <el-avatar :size="32" :style="{ backgroundColor: stringToColor(userStore.user.username || 'U') }">
                {{ (userStore.user.username || 'U').charAt(0).toUpperCase() }}
              </el-avatar>
              <span class="username">{{ userStore.user.username }}</span>
              <el-icon class="dropdown-arrow"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </nav>
    
    <main class="page-container main-content">
      <!-- Floating Toolbar -->
      <div class="toolbar glass-panel">
        <div class="left-tools">
          <el-input
            v-model="searchQuery"
            placeholder="搜索联系人..."
            :prefix-icon="Search"
            class="search-input"
            clearable
          />
          <el-button 
            :type="showFavoritesOnly ? 'warning' : 'default'"
            :plain="!showFavoritesOnly"
            class="filter-btn"
            @click="showFavoritesOnly = !showFavoritesOnly"
          >
            <el-icon :class="{ 'is-active': showFavoritesOnly }"><Star /></el-icon> 
            <span class="btn-text">收藏</span>
          </el-button>
        </div>
        
        <div class="right-tools">
          <el-button type="primary" class="create-btn" @click="handleCreate">
            <el-icon><Plus /></el-icon> 新建联系人
          </el-button>
          
          <el-dropdown trigger="click">
            <el-button class="icon-btn" circle>
              <el-icon><More /></el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleExport">
                  <el-icon><Download /></el-icon> 导出 Excel
                </el-dropdown-item>
                <el-dropdown-item @click="triggerImport">
                  <el-icon><Upload /></el-icon> 导入 Excel
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          
          <input 
            type="file" 
            ref="importInput" 
            style="display: none" 
            accept=".xlsx,.xls"
            @change="handleImport"
          />
        </div>
      </div>
      
      <!-- Contacts Grid -->
      <div v-loading="loading" class="contacts-area">
        <transition-group name="list" tag="div" class="contacts-grid">
          <div 
            v-for="contact in filteredContacts" 
            :key="contact.id" 
            class="contact-card"
          >
            <div class="card-content" @click="handleEdit(contact)">
              <div class="card-header">
                <div class="avatar-wrapper">
                  <el-avatar 
                    :size="56" 
                    :class="{ 'is-favorite': contact.is_favorite }"
                    :style="{ backgroundColor: stringToColor(contact.name) }"
                  >
                    {{ contact.name.charAt(0).toUpperCase() }}
                  </el-avatar>
                </div>
                <div class="info">
                  <h3>{{ contact.name }}</h3>
                  <span class="meta">{{ contact.methods.length }} 种联系方式</span>
                </div>
                
                <button 
                  class="fav-btn" 
                  :class="{ active: contact.is_favorite }"
                  @click.stop="handleToggleFavorite(contact)"
                >
                  <el-icon><StarFilled v-if="contact.is_favorite" /><Star v-else /></el-icon>
                </button>
              </div>
              
              <div class="card-body">
                <div 
                  v-for="method in contact.methods.slice(0, 3)" 
                  :key="method.id" 
                  class="method-item"
                >
                  <el-icon class="method-icon"><component :is="getMethodIcon(method.type)" /></el-icon>
                  <span class="method-value">{{ method.value }}</span>
                </div>
                <div v-if="contact.methods.length > 3" class="more-badge">
                  +{{ contact.methods.length - 3 }} 更多
                </div>
              </div>
            </div>
            
            <div class="card-actions glass-panel">
              <el-button text size="small" @click.stop="handleEdit(contact)">
                <el-icon><Edit /></el-icon>
              </el-button>
              <el-button text size="small" type="danger" @click.stop="handleDelete(contact)">
                <el-icon><Delete /></el-icon>
              </el-button>
            </div>
          </div>
        </transition-group>
        
        <div v-if="filteredContacts.length === 0 && !loading" class="empty-state">
          <el-empty description="暂无联系人" :image-size="160" />
        </div>
      </div>
    </main>
    
    <ContactForm 
      v-model="showContactDialog"
      :edit-data="editingContact"
      @submit="handleSubmit"
    />
  </div>
</template>

<style scoped lang="scss">
.home-container {
  min-height: 100vh;
  /* Background handled by global body style, utilizing transparency here */
}

/* Navbar */
.navbar {
  height: 70px;
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid rgba(255, 255, 255, 0.5);
  
  .nav-content {
    max-width: 1200px;
    margin: 0 auto;
    height: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 24px;
  }
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  
  .logo-icon {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
    color: white;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: var(--shadow-md);
  }
  
  .logo-text {
    font-weight: 700;
    font-size: 20px;
    background: linear-gradient(to right, var(--text-primary), var(--color-primary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
  }
}

.user-menu {
  display: flex;
  align-items: center;
  
  .user-dropdown-trigger {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 6px 12px 6px 6px;
    border-radius: var(--radius-lg);
    cursor: pointer;
    transition: var(--transition-fast);
    
    &:hover {
      background: rgba(99, 102, 241, 0.08);
    }
    
    .el-avatar {
      font-size: 14px;
      font-weight: 600;
      color: white;
    }
  }
  
  .username {
    font-weight: 600;
    color: var(--text-secondary);
    font-size: 14px;
  }
  
  .dropdown-arrow {
    color: var(--text-muted);
    font-size: 12px;
    transition: var(--transition-fast);
  }
}

/* Main Content */
.main-content {
  padding-top: 32px;
  padding-bottom: 64px;
}

/* Toolbar */
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding: 16px 24px;
  border-radius: var(--radius-lg);
  flex-wrap: wrap;
  gap: 16px;
  
  .left-tools {
    display: flex;
    gap: 16px;
    flex: 1;
    min-width: 300px;
    
    .search-input {
      max-width: 320px;
    }
  }
  
  .right-tools {
    display: flex;
    gap: 12px;
  }
}

/* Contact Grid */
.contacts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.contact-card {
  position: relative;
  background: var(--surface-color);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color-light);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-hover);
    border-color: var(--color-primary-soft);
    
    .card-actions {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .card-content {
    padding: 24px;
    flex: 1;
    cursor: pointer;
  }
}

.card-header {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-bottom: 20px;
  
  .avatar-wrapper {
    margin-bottom: 12px;
    position: relative;
    
    .el-avatar {
      font-size: 20px;
      font-weight: 600;
      color: white;
      border: 3px solid white;
      box-shadow: var(--shadow-md);
      
      &.is-favorite {
        border-color: #fff7ed; /* Light orange ring */
        box-shadow: 0 0 0 2px var(--color-warning);
      }
    }
  }
  
  h3 {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 4px;
  }
  
  .meta {
    font-size: 13px;
    color: var(--text-muted);
  }
  
  .fav-btn {
    position: absolute;
    top: -4px;
    right: -4px;
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    transition: var(--transition-fast);
    padding: 8px;
    
    &:hover, &.active {
      color: var(--color-warning);
      transform: scale(1.1);
    }
  }
}

.card-body {
  .method-item {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
    font-size: 14px;
    color: var(--text-secondary);
    padding: 6px 10px;
    background: var(--bg-color);
    border-radius: var(--radius-sm);
    
    .method-icon {
      color: var(--color-primary);
    }
    
    .method-value {
      flex: 1;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
  }
}

.card-actions {
  position: absolute;
  bottom: 12px;
  left: 50%;
  transform: translateX(-50%) translateY(10px);
  padding: 4px 8px;
  border-radius: 20px;
  display: flex;
  gap: 4px;
  opacity: 0;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-md);
}

/* Animations using Vue TransitionGroup */
.list-move, /* apply transition to moving elements */
.list-enter-active,
.list-leave-active {
  transition: all 0.4s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

.list-leave-active {
  position: absolute; 
}
</style>
