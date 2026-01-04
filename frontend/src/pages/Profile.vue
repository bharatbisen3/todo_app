<!-- frappe-bench/apps/todo_app/frontend/src/pages/Profile.vue -->

<template>
  <div class="p-8">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">Profile</h1>
    
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      <p class="mt-2 text-gray-600">Loading profile...</p>
    </div>

    <!-- Profile Content -->
    <div v-else class="max-w-4xl">
      <!-- Profile Card -->
      <div class="bg-white rounded-lg shadow-sm p-8 mb-6">
        <div class="flex items-start gap-6">
          <!-- Avatar -->
          <div class="flex-shrink-0">
            <div class="h-24 w-24 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center text-white text-3xl font-bold shadow-lg">
              {{ userInitial }}
            </div>
          </div>

          <!-- User Info -->
          <div class="flex-1">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-2xl font-bold text-gray-900">{{ userData.full_name }}</h2>
                <p class="text-gray-600 mt-1">{{ userData.email }}</p>
              </div>
              <Button @click="showEditModal = true" variant="outline">
                Edit Profile
              </Button>
            </div>

            <!-- User Details -->
            <div class="grid grid-cols-2 gap-4 mt-6">
              <div>
                <p class="text-sm text-gray-500">User Type</p>
                <p class="text-sm font-medium text-gray-900 mt-1">{{ userData.user_type || 'System User' }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">Username</p>
                <p class="text-sm font-medium text-gray-900 mt-1">{{ userData.username || userData.email }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">Member Since</p>
                <p class="text-sm font-medium text-gray-900 mt-1">{{ formatDate(userData.creation) }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">Last Active</p>
                <p class="text-sm font-medium text-gray-900 mt-1">{{ formatRelativeTime(userData.last_active) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Total Tasks</p>
              <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.totalTasks }}</p>
            </div>
            <div class="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">
              <ListTodo class="w-6 h-6 text-blue-600" />
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Completed</p>
              <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.completedTasks }}</p>
            </div>
            <div class="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center">
              <CheckCircle class="w-6 h-6 text-green-600" />
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Appointments</p>
              <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.totalAppointments }}</p>
            </div>
            <div class="w-12 h-12 rounded-full bg-purple-100 flex items-center justify-center">
              <Calendar class="w-6 h-6 text-purple-600" />
            </div>
          </div>
        </div>
      </div>

      <!-- Actions Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Settings -->
        <div class="bg-white rounded-lg shadow-sm p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Settings</h3>
          <div class="space-y-3">
            <button 
              @click="changePassword"
              class="w-full py-3 px-4 bg-gray-50 rounded-lg text-left hover:bg-gray-100 transition-colors flex items-center gap-3"
            >
              <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
              </svg>
              <span class="font-medium">Change Password</span>
            </button>
            <button 
              @click="editProfile"
              class="w-full py-3 px-4 bg-gray-50 rounded-lg text-left hover:bg-gray-100 transition-colors flex items-center gap-3"
            >
              <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              <span class="font-medium">Edit Profile</span>
            </button>
            <button 
              class="w-full py-3 px-4 bg-gray-50 rounded-lg text-left hover:bg-gray-100 transition-colors flex items-center gap-3"
            >
              <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <span class="font-medium">Preferences</span>
            </button>
          </div>
        </div>

        <!-- Help & Support -->
        <div class="bg-white rounded-lg shadow-sm p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Help & Support</h3>
          <div class="space-y-3">
            <button class="w-full py-3 px-4 bg-gray-50 rounded-lg text-left hover:bg-gray-100 transition-colors flex items-center gap-3">
              <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span class="font-medium">Help Center</span>
            </button>
            <button class="w-full py-3 px-4 bg-gray-50 rounded-lg text-left hover:bg-gray-100 transition-colors flex items-center gap-3">
              <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <span class="font-medium">Contact Support</span>
            </button>
            <button 
              @click="logout"
              class="w-full py-3 px-4 bg-red-50 text-red-600 rounded-lg text-left hover:bg-red-100 transition-colors flex items-center gap-3"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              <span class="font-medium">Logout</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Profile Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg p-6 max-w-md w-full">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">Edit Profile</h2>

        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
            <Input v-model="editData.full_name" placeholder="Enter full name" />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <Input v-model="editData.email" type="email" disabled class="bg-gray-50" />
            <p class="text-xs text-gray-500 mt-1">Email cannot be changed</p>
          </div>
        </div>

        <div class="mt-6 flex gap-3 justify-end">
          <Button @click="showEditModal = false" variant="outline">Cancel</Button>
          <Button @click="saveProfile" variant="solid" :loading="saving">Save Changes</Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { call } from 'frappe-ui'
import { Button, Input } from 'frappe-ui'
import { ListTodo, Calendar, CheckCircle } from 'lucide-vue-next'
import { createListResource } from 'frappe-ui'

const loading = ref(true)
const saving = ref(false)
const showEditModal = ref(false)

const userData = ref({
  full_name: '',
  email: '',
  username: '',
  user_type: '',
  creation: '',
  last_active: ''
})

const editData = ref({
  full_name: '',
  email: ''
})

const stats = ref({
  totalTasks: 0,
  completedTasks: 0,
  totalAppointments: 0
})

// Fetch user data
onMounted(async () => {
  try {
    // Get current user
    const user = await call('frappe.auth.get_logged_user')
    
    // Get user details
    const userDetails = await call('frappe.client.get', {
      doctype: 'User',
      name: user
    })
    
    userData.value = {
      full_name: userDetails.full_name || userDetails.first_name || 'User',
      email: userDetails.email,
      username: userDetails.username,
      user_type: userDetails.user_type,
      creation: userDetails.creation,
      last_active: userDetails.last_active || new Date().toISOString()
    }

    editData.value = {
      full_name: userData.value.full_name,
      email: userData.value.email
    }

    // Fetch stats
    await fetchStats()
  } catch (error) {
    console.error('Error fetching profile:', error)
  } finally {
    loading.value = false
  }
})

// Fetch statistics
async function fetchStats() {
  try {
    // Get tasks count
    const tasksCount = await call('frappe.client.get_count', {
      doctype: 'Todo Item'
    })

    const completedCount = await call('frappe.client.get_count', {
      doctype: 'Todo Item',
      filters: { status: 'Completed' }
    })

    const appointmentsCount = await call('frappe.client.get_count', {
      doctype: 'Appointment'
    })

    stats.value = {
      totalTasks: tasksCount,
      completedTasks: completedCount,
      totalAppointments: appointmentsCount
    }
  } catch (error) {
    console.error('Error fetching stats:', error)
  }
}

const userInitial = computed(() => {
  return userData.value.full_name.charAt(0).toUpperCase()
})

function editProfile() {
  showEditModal.value = true
}

async function saveProfile() {
  saving.value = true
  try {
    await call('frappe.client.set_value', {
      doctype: 'User',
      name: userData.value.email,
      fieldname: 'full_name',
      value: editData.value.full_name
    })

    userData.value.full_name = editData.value.full_name
    showEditModal.value = false
    alert('Profile updated successfully!')
  } catch (error) {
    console.error('Error updating profile:', error)
    alert('Failed to update profile')
  } finally {
    saving.value = false
  }
}

function changePassword() {
  window.open('/app/user/' + userData.value.email, '_blank')
}

async function logout() {
  if (confirm('Are you sure you want to logout?')) {
    window.location.href = '/api/method/logout'
  }
}

function formatDate(dateString) {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })
}

function formatRelativeTime(dateString) {
  if (!dateString) return 'Just now'
  const date = new Date(dateString)
  const now = new Date()
  const diffInSeconds = Math.floor((now - date) / 1000)

  if (diffInSeconds < 60) return 'Just now'
  if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`
  if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`
  if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)}d ago`
  return formatDate(dateString)
}
</script>