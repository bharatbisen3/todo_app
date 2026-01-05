<template>
  <div class="theme-selector">
    <!-- Full selector when expanded -->
    <div v-if="!isCollapsed">
      <label class="block text-xs font-medium mb-2 text-gray-600">
        🎨 Theme
      </label>
      <select 
        v-model="selectedTheme"
        @change="handleThemeChange"
        class="w-full px-3 py-2 rounded-lg border border-gray-300 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-900 cursor-pointer"
      >
        <option value="light">☀️ Light</option>
        <option value="dark">🌙 Dark</option>
        <option value="blue">🌊 Blue Ocean</option>
        <option value="green">🌿 Forest Green</option>
        <option value="purple">💜 Royal Purple</option>
      </select>
    </div>
    
    <!-- Compact button when collapsed -->
    <button 
      v-else
      @click="cycleTheme"
      class="w-full p-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors"
      title="Change Theme"
    >
      <span class="text-xl">{{ themeEmoji }}</span>
    </button>
  </div>
</template>

<script setup>
import { ref, watch, computed, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme'

const props = defineProps({
  isCollapsed: {
    type: Boolean,
    default: false
  }
})

const { currentTheme, changeTheme } = useTheme()
const selectedTheme = ref('light')

const themes = ['light', 'dark', 'blue', 'green', 'purple']
const themeEmojis = {
  light: '☀️',
  dark: '🌙',
  blue: '🌊',
  green: '🌿',
  purple: '💜'
}

let currentIndex = 0

const themeEmoji = computed(() => {
  return themeEmojis[selectedTheme.value] || '☀️'
})

// Sync with composable
watch(currentTheme, (newTheme) => {
  selectedTheme.value = newTheme
  currentIndex = themes.indexOf(newTheme)
})

onMounted(() => {
  selectedTheme.value = currentTheme.value
  currentIndex = themes.indexOf(currentTheme.value)
})

function handleThemeChange() {
  console.log('🎨 Theme changed to:', selectedTheme.value)
  changeTheme(selectedTheme.value)
}

function cycleTheme() {
  currentIndex = (currentIndex + 1) % themes.length
  selectedTheme.value = themes[currentIndex]
  console.log('🔄 Cycling to:', selectedTheme.value)
  changeTheme(selectedTheme.value)
}
</script>

<style scoped>
.theme-selector select {
  cursor: pointer;
}

.theme-selector select:hover {
  border-color: #60a5fa;
}

.theme-selector select:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
</style>