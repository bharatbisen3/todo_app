import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import { getProxyOptions } from 'frappe-ui/src/utils/vite-dev-server'
import fs from 'fs'

const configPath = path.resolve(__dirname, '../../../sites/common_site_config.json')
const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'))
const webserver_port = config.webserver_port_map['internal.algoware.in'] || 8001

export default defineConfig({
  plugins: [vue()],
  base: '/assets/todo_app/frontend/',  // ADD THIS LINE
  server: {
    port: 8080,
    proxy: getProxyOptions({ port: webserver_port }),
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  build: {
    outDir: '../todo_app/public/frontend',
    emptyOutDir: true,
    target: 'es2015',
  },
  optimizeDeps: {
    include: ['frappe-ui > feather-icons', 'showdown', 'engine.io-client'],
  },
})