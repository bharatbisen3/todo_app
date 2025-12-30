<template>
  <div class="flex flex-col h-screen bg-gray-50">
    <!-- Main Content Area -->
    <main class="flex-1 overflow-y-auto pb-20">
      <router-view />
    </main>

    <!-- Bottom Navigation -->
    <nav class="fixed bottom-0 left-0 w-full bg-white border-t border-gray-200 shadow-lg pb-safe z-50">
      <div class="flex justify-around items-center h-16">
        <button 
          v-for="item in navItems" 
          :key="item.name"
          @click="navigate(item)"
          class="flex flex-col items-center justify-center w-full h-full space-y-1 transition-colors"
          :class="isActive(item.route) ? 'text-blue-600' : 'text-gray-500'"
        >
          <component :is="item.icon" class="w-6 h-6 stroke-2" />
          <span class="text-[10px] font-medium">{{ item.label }}</span>
        </button>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { Home, ListTodo, Bell, User } from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()

// Navigation items
const navItems = [
  { name: 'Home', label: 'Tasks', icon: ListTodo, route: 'Home' },
  { name: 'Notifications', label: 'Alerts', icon: Bell, route: 'Notifications' },
  { name: 'Profile', label: 'Profile', icon: User, route: 'Profile' },
]

// Navigate to route
function navigate(item) {
  router.push({ name: item.route })
}

// Check if route is active
function isActive(routeName) {
  return route.name === routeName
}
</script>

<style scoped>
.pb-safe {
  padding-bottom: env(safe-area-inset-bottom);
}
</style>