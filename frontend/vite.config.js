import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  // --- 新增的代理配置 ---
  server: {
    host: 'localhost', // 只允许本地访问
    port: 5173, // 使用 Vite 默认端口
    proxy: {
      // 字符串简写写法
      // '/api': 'http://localhost:8000',

      // 选项写法，更灵活
      '/api': {
        target: 'http://localhost:9000', // 目标后端服务地址
        changeOrigin: true, // 需要虚拟主机站点
        // 如果你的后端API路径没有 /api 前缀，可以用这个重写
        // rewrite: (path) => path.replace(/^\/api/, '')
      },
    },
  },
})
