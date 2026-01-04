import { ref, watch, onMounted } from 'vue'
import { call } from 'frappe-ui'

const currentTheme = ref('light')
const isLoading = ref(false)

export function useTheme() {
  
  // Apply CSS variables to document
  const applyTheme = (cssVariables) => {
    const root = document.documentElement
    
    // Remove old variables
    Object.keys(root.style).forEach(key => {
      if (key.startsWith('--')) {
        root.style.removeProperty(key)
      }
    })
    
    // Apply new variables
    Object.entries(cssVariables).forEach(([key, value]) => {
      root.style.setProperty(key, value)
    })
  }
  
  // Load theme from backend
  const loadTheme = async (themeKey) => {
    isLoading.value = true
    try {
      const properties = await call('theme_master.api.get_theme_properties', {
        theme_key: themeKey
      })
      
      applyTheme(properties)
      currentTheme.value = themeKey
      
      // Save to localStorage
      localStorage.setItem('selected_theme', themeKey)
      
      return true
    } catch (error) {
      console.error('Error loading theme:', error)
      return false
    } finally {
      isLoading.value = false
    }
  }
  
  // Get available themes
  const getAvailableThemes = async () => {
    try {
      const themes = await call('theme_master.api.get_available_themes')
      return themes
    } catch (error) {
      console.error('Error fetching themes:', error)
      return []
    }
  }
  
  // Save user preference
  const saveUserTheme = async (themeKey) => {
    try {
      await call('theme_master.api.save_user_theme', {
        theme_key: themeKey
      })
      return true
    } catch (error) {
      console.error('Error saving theme:', error)
      return false
    }
  }
  
  // Initialize theme on mount
  const initializeTheme = async () => {
    // Try localStorage first
    const savedTheme = localStorage.getItem('selected_theme')
    
    if (savedTheme) {
      await loadTheme(savedTheme)
      return
    }
    
    // Try user settings
    try {
      const userTheme = await call('theme_master.api.get_user_theme')
      if (userTheme) {
        await loadTheme(userTheme)
        return
      }
    } catch (error) {
      console.error('Error loading user theme:', error)
    }
    
    // Load default theme
    try {
      const defaultTheme = await call('theme_master.api.get_default_theme')
      await loadTheme(defaultTheme.theme_key)
    } catch (error) {
      console.error('Error loading default theme:', error)
    }
  }
  
  return {
    currentTheme,
    isLoading,
    loadTheme,
    getAvailableThemes,
    saveUserTheme,
    initializeTheme
  }
}