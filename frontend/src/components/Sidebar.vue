<template>
	<div class="flex h-screen" :style="{ backgroundColor: `var(--theme-bgSecondary, #f3f4f6)` }">
		<!-- Sidebar -->
		<aside
			class="shadow-lg flex flex-col transition-all duration-300"
			:class="isCollapsed ? 'w-20' : 'w-64'"
			:style="{ backgroundColor: `var(--theme-bgPrimary, #ffffff)` }"
		>
			<!-- Header -->
			<div class="p-6 border-b flex items-center justify-between" :style="{ borderColor: `var(--theme-border, #e5e7eb)` }">
				<div v-if="!isCollapsed">
					<h1 class="text-2xl font-bold" :style="{ color: `var(--theme-textPrimary, #111827)` }">Todo App</h1>
					<p class="text-sm mt-1" :style="{ color: `var(--theme-textSecondary, #6b7280)` }">Manage your day</p>
				</div>
				<div v-else class="mx-auto">
					<h1 class="text-2xl font-bold" :style="{ color: `var(--theme-textPrimary, #111827)` }">T</h1>
				</div>

				<!-- Toggle Button -->
				<button
					@click="toggleSidebar"
					class="p-2 rounded-lg hover:bg-gray-100 transition-colors"
					:class="isCollapsed ? 'mx-auto mt-2' : ''"
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="w-5 h-5 transition-transform duration-300"
						:class="isCollapsed ? 'rotate-180' : ''"
						:style="{ color: `var(--theme-textSecondary, #6b7280)` }"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M11 19l-7-7 7-7m8 14l-7-7 7-7"
						/>
					</svg>
				</button>
			</div>

			<!-- Navigation -->
			<nav class="flex-1 p-4 space-y-2">
				<router-link
					v-for="item in navItems"
					:key="item.name"
					:to="{ name: item.route }"
					class="flex items-center gap-3 px-4 py-3 rounded-lg transition-colors relative group"
					:class="
						isActive(item.route)
							? 'font-medium'
							: ''
					"
					:style="isActive(item.route) 
						? { 
								backgroundColor: `var(--theme-accentLight, #dbeafe)`, 
								color: `var(--theme-accent, #3b82f6)` 
							}
						: { 
								color: `var(--theme-textPrimary, #374151)` 
							}"
				>
					<component :is="item.icon" class="w-5 h-5 flex-shrink-0" />
					<span v-if="!isCollapsed">{{ item.label }}</span>
					<span
						v-if="item.badge && !isCollapsed"
						class="ml-auto px-2 py-1 text-xs rounded-full"
						:style="{ 
							backgroundColor: `var(--theme-accentLight, #dbeafe)`, 
							color: `var(--theme-accent, #3b82f6)` 
						}"
					>
						{{ item.badge }}
					</span>

					<!-- Tooltip for collapsed state -->
					<div
						v-if="isCollapsed"
						class="absolute left-full ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-50"
					>
						{{ item.label }}
						<span
							v-if="item.badge"
							class="ml-2 px-2 py-0.5 text-xs rounded-full bg-blue-500"
						>
							{{ item.badge }}
						</span>
					</div>
				</router-link>
			</nav>

			<!-- Theme Selector -->
			<div class="p-4 border-t" :style="{ borderColor: `var(--theme-border, #e5e7eb)` }">
				<ThemeSelector :isCollapsed="isCollapsed" />
			</div>

			<!-- User Profile -->
			<div class="p-4 border-t" :style="{ borderColor: `var(--theme-border, #e5e7eb)` }">
				<router-link
					:to="{ name: 'Profile' }"
					class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-gray-100 cursor-pointer transition-colors relative group"
					:class="isActive('Profile') ? 'bg-blue-50' : ''"
				>
					<div
						class="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold flex-shrink-0"
						:style="{ backgroundColor: `var(--theme-accent, #3b82f6)` }"
					>
						{{ userInitial }}
					</div>
					<div v-if="!isCollapsed" class="flex-1">
						<p class="text-sm font-medium" :style="{ color: `var(--theme-textPrimary, #111827)` }">{{ currentUser }}</p>
						<p class="text-xs" :style="{ color: `var(--theme-textSecondary, #6b7280)` }">View Profile</p>
					</div>

					<!-- Tooltip for collapsed state -->
					<div
						v-if="isCollapsed"
						class="absolute left-full ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-50"
					>
						{{ currentUser }}
					</div>
				</router-link>
			</div>
		</aside>

		<!-- Main Content -->
		<main class="flex-1 overflow-y-auto" :style="{ backgroundColor: `var(--theme-bgSecondary, #f9fafb)` }">
			<router-view />
		</main>
	</div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Home, ListTodo, Calendar, CreditCard } from 'lucide-vue-next'
import { call } from 'frappe-ui'
import ThemeSelector from '@/components/ThemeSelector.vue'

const route = useRoute()
const currentUser = ref('User')
const isCollapsed = ref(false)

onMounted(async () => {
	try {
		const user = await call('frappe.auth.get_logged_user')
		if (user) {
			currentUser.value = user.split('@')[0]
		}
	} catch (error) {
		console.error('Error fetching user:', error)
	}
})

const userInitial = computed(() => {
	return currentUser.value.charAt(0).toUpperCase()
})

const navItems = computed(() => [
	{
		name: 'Dashboard',
		label: 'Home',
		icon: Home,
		route: 'Dashboard',
	},
	{
		name: 'Tasks',
		label: 'Tasks',
		icon: ListTodo,
		route: 'Tasks',
		badge: '5',
	},
	{
		name: 'Appointments',
		label: 'Appointments',
		icon: Calendar,
		route: 'Appointments',
	},
	{
		name: 'Payment',
		label: 'Payment',
		icon: CreditCard,
		route: 'Payment',
	},
])

function isActive(routeName) {
	return route.name === routeName
}

function toggleSidebar() {
	isCollapsed.value = !isCollapsed.value
}
</script>

<style scoped>
/* Smooth theme transitions */
aside, nav a, button {
  transition: all 0.3s ease;
}
</style>