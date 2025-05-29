import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'  // 新增：用于路径解析

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {  // 新增：别名配置
    alias: {
      '@': path.resolve(__dirname, 'src')  // @ 指向 src 目录
    }
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
})
