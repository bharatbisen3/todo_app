<template>
  <div class="p-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
      <p class="text-gray-600 mt-1">Welcome back! Here's your overview</p>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div 
        v-for="stat in stats" 
        :key="stat.label"
        class="bg-white rounded-lg shadow-sm p-6 border-l-4"
        :style="{ borderColor: stat.color }"
      >
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600 mb-1">{{ stat.label }}</p>
            <p class="text-3xl font-bold text-gray-900">{{ stat.value }}</p>
            <p class="text-xs text-gray-500 mt-2">{{ stat.change }}</p>
          </div>
          <div 
            class="w-12 h-12 rounded-full flex items-center justify-center"
            :style="{ backgroundColor: stat.color + '20' }"
          >
            <component :is="stat.icon" :style="{ color: stat.color }" class="w-6 h-6" />
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Recent Tasks -->
      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-bold text-gray-900">Recent Tasks</h2>
          <router-link 
            :to="{ name: 'Tasks' }"
            class="text-sm text-blue-600 hover:text-blue-700"
          >
            View All →
          </router-link>
        </div>
        
        <div v-if="recentTasks.loading" class="text-center py-8">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
        
        <div v-else-if="recentTasks.data && recentTasks.data.length" class="space-y-3">
          <div 
            v-for="task in recentTasks.data.slice(0, 5)" 
            :key="task.name"
            class="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50"
          >
            <input 
              type="checkbox" 
              :checked="task.status === 'Completed'"
              class="w-5 h-5 rounded"
            />
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">{{ task.task_title }}</p>
              <p class="text-xs text-gray-500">{{ formatDate(task.creation) }}</p>
            </div>
            <span 
              class="px-2 py-1 text-xs rounded-full"
              :class="getStatusClass(task.status)"
            >
              {{ task.status }}
            </span>
          </div>
        </div>
        
        <div v-else class="text-center py-8 text-gray-500">
          No tasks yet
        </div>
      </div>

      <!-- Upcoming Appointments -->
      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-bold text-gray-900">Upcoming Appointments</h2>
          <router-link 
            :to="{ name: 'Appointments' }"
            class="text-sm text-blue-600 hover:text-blue-700"
          >
            View All →
          </router-link>
        </div>
        
        <div v-if="upcomingAppointments.loading" class="text-center py-8">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
        
        <div v-else-if="upcomingAppointments.data && upcomingAppointments.data.length" class="space-y-3">
          <div 
            v-for="apt in upcomingAppointments.data.slice(0, 5)" 
            :key="apt.name"
            class="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50"
          >
            <div class="w-12 h-12 rounded-lg bg-blue-50 flex flex-col items-center justify-center">
              <span class="text-xs text-blue-600 font-medium">{{ formatDay(apt.appointment_date) }}</span>
              <span class="text-lg font-bold text-blue-600">{{ formatDayNum(apt.appointment_date) }}</span>
            </div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">{{ apt.customer_name || 'Appointment' }}</p>
              <p class="text-xs text-gray-500">{{ formatTime(apt.appointment_time) }}</p>
            </div>
          </div>
        </div>
        
        <div v-else class="text-center py-8 text-gray-500">
          No upcoming appointments
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { createListResource } from 'frappe-ui'
import { ListTodo, Calendar, CheckCircle, Clock } from 'lucide-vue-next'

// Fetch tasks
const recentTasks = createListResource({
  doctype: 'Todo Item',
  fields: ['name', 'task_title', 'status', 'priority', 'creation'],
  orderBy: 'creation desc',
  pageLength: 10,
  auto: true
})

// Fetch appointments
const upcomingAppointments = createListResource({
  doctype: 'Appointment',
  fields: ['name', 'customer_name', 'appointment_date', 'appointment_time', 'status'],
  filters: {
    appointment_date: ['>=', new Date().toISOString().split('T')[0]]
  },
  orderBy: 'appointment_date asc',
  pageLength: 10,
  auto: true
})

// Calculate stats
const stats = computed(() => {
  const tasks = recentTasks.data || []
  const total = tasks.length
  const open = tasks.filter(t => t.status === 'Open').length
  const completed = tasks.filter(t => t.status === 'Completed').length
  const inProgress = tasks.filter(t => t.status === 'In Progress').length
  
  const appointments = upcomingAppointments.data || []
  const upcomingCount = appointments.length

  return [
    {
      label: 'Total Tasks',
      value: total,
      change: '+12% from last week',
      color: '#3B82F6',
      icon: ListTodo
    },
    {
      label: 'Open Tasks',
      value: open,
      change: `${inProgress} in progress`,
      color: '#F59E0B',
      icon: Clock
    },
    {
      label: 'Completed',
      value: completed,
      change: 'Great progress!',
      color: '#10B981',
      icon: CheckCircle
    },
    {
      label: 'Appointments',
      value: upcomingCount,
      change: 'Next 30 days',
      color: '#8B5CF6',
      icon: Calendar
    }
  ]
})

// Helper functions
function getStatusClass(status) {
  const classes = {
    'Open': 'bg-blue-100 text-blue-700',
    'In Progress': 'bg-orange-100 text-orange-700',
    'Completed': 'bg-green-100 text-green-700'
  }
  return classes[status] || 'bg-gray-100 text-gray-700'
}

function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

function formatDay(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { weekday: 'short' }).toUpperCase()
}

function formatDayNum(dateString) {
  const date = new Date(dateString)
  return date.getDate()
}

function formatTime(timeString) {
  if (!timeString) return ''
  return timeString
}
</script>