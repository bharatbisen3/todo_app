<template>
  <div class="theme-switcher">
    <label class="block text-sm font-medium text-gray-700 mb-2">
      Theme
    </label>
    
    <div v-if="loading" class="text-sm text-gray-500">
      Loading themes...
    </div>
    
    <div v-else class="grid grid-cols-2 gap-3">
      <button
        v-for="theme in themes"
        :key="theme.theme_key"
        @click="selectTheme(theme.theme_key)"
        :class="[
          'p-4 rounded-lg border-2 transition-all',
          currentTheme === theme.theme_key
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-200 hover:border-gray-300'
        ]"
      >
        <div class="flex items-center justify-between">
          <span class="font-medium text-gray-900">{{ theme.theme_name }}</span>
          <div
            v-if="currentTheme === theme.theme_key"
            class="w-5 h-5 rounded-full bg-blue-500 flex items-center justify-center"
          >
            <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
            </svg>
          </div>
        </div>
      </button>
    </div>
    
    <p v-if="!loading && themes.length === 0" class="text-sm text-gray-500">
      No themes available
    </p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useTheme } from '../composables/useTheme'

const { currentTheme, loadTheme, getAvailableThemes, saveUserTheme } = useTheme()

const themes = ref([])
const loading = ref(true)

onMounted(async () => {
  themes.value = await getAvailableThemes()
  loading.value = false
})

const selectTheme = async (themeKey) => {
  const success = await loadTheme(themeKey)
  
  if (success) {
    await saveUserTheme(themeKey)
  }
}
</script>