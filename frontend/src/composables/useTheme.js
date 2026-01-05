import { ref } from 'vue'
import { call } from 'frappe-ui'
import { getTheme } from '@/config/themes'

const currentTheme = ref('light')
const themeLoaded = ref(false)

export function useTheme() {
  
  // Apply theme to DOM
  function applyTheme(themeName) {
    const theme = getTheme(themeName)
    const root = document.documentElement
    
    // Apply CSS variables
    Object.entries(theme.colors).forEach(([key, value]) => {
      root.style.setProperty(`--theme-${key}`, value)
    })
    
    // Store theme name
    root.setAttribute('data-theme', themeName.toLowerCase())
    currentTheme.value = themeName.toLowerCase()
    
    console.log('✅ Theme applied:', themeName)
  }
  
  // Load user preferences
  async function loadTheme() {
    try {
      console.log('🔄 Loading theme...')
      const preferences = await call('todo_app.api.get_user_preferences')
      console.log('📥 Preferences:', preferences)
      
      if (preferences?.theme) {
        applyTheme(preferences.theme.toLowerCase())
      } else {
        applyTheme('light')
      }
    } catch (error) {
      console.error('❌ Error loading theme:', error)
      applyTheme('light')
    } finally {
      themeLoaded.value = true
    }
  }
  
  // Change theme
  async function changeTheme(themeName) {
    console.log('🎨 Changing theme to:', themeName)
    applyTheme(themeName)
    
    try {
      const result = await call('todo_app.api.update_user_preferences', {
        theme: themeName.charAt(0).toUpperCase() + themeName.slice(1)
      })
      console.log('💾 Saved:', result)
    } catch (error) {
      console.error('❌ Save failed:', error)
    }
  }
  
  // Auto-load on first use
  if (!themeLoaded.value) {
    loadTheme()
  }
  
  return {
    currentTheme,
    themeLoaded,
    changeTheme,
    applyTheme
  }
}