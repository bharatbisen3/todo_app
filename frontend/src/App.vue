<!-- <template>
  <div>
    <router-view />
  </div>
</template> -->

<!-- 
<template>
  <MobileLayout />
</template>

<script setup>
import MobileLayout from '@/components/MobileLayout.vue'
</script> 
-->









<!-- 
<template>
  <Sidebar />
</template>


<script setup>
import Sidebar from '@/components/Sidebar.vue'
</script>


<!-- 
 <script setup>
import { onMounted } from 'vue'
import { useTheme } from './composables/useTheme'

const { initializeTheme } = useTheme()

onMounted(async () => {
  await initializeTheme()
})
</script> -->









<script setup>
import { onMounted } from 'vue'
import { setConfig, frappeRequest } from 'frappe-ui'
import { useTheme } from '@/composables/useTheme'
import Sidebar from '@/components/Sidebar.vue'

const { themeLoaded } = useTheme()

setConfig('resourceFetcher', frappeRequest)

onMounted(() => {
  console.log('🚀 App mounted')
})
</script>

<template>
  <div v-if="themeLoaded">
    <Sidebar />
  </div>
  <div v-else class="flex items-center justify-center min-h-screen bg-gray-50">
    <div class="text-center">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
      <p class="mt-4 text-gray-600">Loading your workspace...</p>
    </div>
  </div>
</template>

<style>
/* Global theme transition */
* {
  transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}
</style>