import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/pages/Dashboard.vue'),
  },
  {
    path: '/tasks',
    name: 'Tasks',
    component: () => import('@/pages/Home.vue'),
  },
  {
    path: '/appointments',
    name: 'Appointments',
    component: () => import('@/pages/Appointments.vue'),
  },
  {
    path: '/payment',
    name: 'Payment',
    component: () => import('@/pages/Payment.vue'),
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/pages/Profile.vue'),
  },
]

let router = createRouter({
  history: createWebHistory('/todo'),
  routes,
})

export default router