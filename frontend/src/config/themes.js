export const themes = {
  light: {
    name: 'Light',
    colors: {
      // Background colors
      bgPrimary: '#ffffff',
      bgSecondary: '#f3f4f6',
      bgTertiary: '#e5e7eb',
      
      // Text colors
      textPrimary: '#111827',
      textSecondary: '#6b7280',
      textTertiary: '#9ca3af',
      
      // Border colors
      border: '#e5e7eb',
      borderHover: '#d1d5db',
      
      // Accent colors
      accent: '#3b82f6',
      accentHover: '#2563eb',
      accentLight: '#dbeafe',
      
      // Status colors
      success: '#10b981',
      warning: '#f59e0b',
      error: '#ef4444',
      info: '#3b82f6',
      
      // Shadow
      shadow: 'rgba(0, 0, 0, 0.1)',
    }
  },
  
  dark: {
    name: 'Dark',
    colors: {
      bgPrimary: '#1f2937',
      bgSecondary: '#111827',
      bgTertiary: '#374151',
      
      textPrimary: '#f9fafb',
      textSecondary: '#d1d5db',
      textTertiary: '#9ca3af',
      
      border: '#374151',
      borderHover: '#4b5563',
      
      accent: '#3b82f6',
      accentHover: '#2563eb',
      accentLight: '#1e3a8a',
      
      success: '#10b981',
      warning: '#f59e0b',
      error: '#ef4444',
      info: '#3b82f6',
      
      shadow: 'rgba(0, 0, 0, 0.3)',
    }
  },
  
  blue: {
    name: 'Blue Ocean',
    colors: {
      bgPrimary: '#eff6ff',
      bgSecondary: '#dbeafe',
      bgTertiary: '#bfdbfe',
      
      textPrimary: '#1e3a8a',
      textSecondary: '#1e40af',
      textTertiary: '#3b82f6',
      
      border: '#93c5fd',
      borderHover: '#60a5fa',
      
      accent: '#2563eb',
      accentHover: '#1d4ed8',
      accentLight: '#dbeafe',
      
      success: '#10b981',
      warning: '#f59e0b',
      error: '#ef4444',
      info: '#3b82f6',
      
      shadow: 'rgba(37, 99, 235, 0.15)',
    }
  },
  
  green: {
    name: 'Forest Green',
    colors: {
      bgPrimary: '#f0fdf4',
      bgSecondary: '#dcfce7',
      bgTertiary: '#bbf7d0',
      
      textPrimary: '#14532d',
      textSecondary: '#166534',
      textTertiary: '#15803d',
      
      border: '#86efac',
      borderHover: '#4ade80',
      
      accent: '#22c55e',
      accentHover: '#16a34a',
      accentLight: '#dcfce7',
      
      success: '#10b981',
      warning: '#f59e0b',
      error: '#ef4444',
      info: '#3b82f6',
      
      shadow: 'rgba(34, 197, 94, 0.15)',
    }
  },
  
  purple: {
    name: 'Royal Purple',
    colors: {
      bgPrimary: '#faf5ff',
      bgSecondary: '#f3e8ff',
      bgTertiary: '#e9d5ff',
      
      textPrimary: '#581c87',
      textSecondary: '#6b21a8',
      textTertiary: '#7c3aed',
      
      border: '#c084fc',
      borderHover: '#a855f7',
      
      accent: '#9333ea',
      accentHover: '#7e22ce',
      accentLight: '#f3e8ff',
      
      success: '#10b981',
      warning: '#f59e0b',
      error: '#ef4444',
      info: '#3b82f6',
      
      shadow: 'rgba(147, 51, 234, 0.15)',
    }
  }
}

export const getTheme = (themeName) => {
  return themes[themeName?.toLowerCase()] || themes.light
}