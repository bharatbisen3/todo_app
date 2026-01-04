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











<template>
  <Sidebar />
</template>

<!-- 
<script setup>
import Sidebar from '@/components/Sidebar.vue'
</script>
 -->


 <script setup>
import { onMounted } from 'vue'
import { useTheme } from './composables/useTheme'

const { initializeTheme } = useTheme()

onMounted(async () => {
  await initializeTheme()
})
</script>
