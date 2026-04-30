import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: true,
    proxy: { 
      '/userPick': { 
        target: 'http://127.0.0.1:5001',
        changeOrigin: true,
        secure: false,
      },

      '/addUser': { 
        target: 'http://127.0.0.1:5001',
        changeOrigin: true,
        secure: false,
      },

      '/getDraftStatus':{
        target: 'http://127.0.0.1:5001',
        changeOrigin: true,
        secure: false,
      },

      '/pullDraftResults':{
        target: 'http://127.0.0.1:5001',
        changeOrigin: true,
        secure: false,
      },

      '/pullUserTeam':{
        target: 'http://127.0.0.1:5001',
        changeOrigin: true,
        secure: false,
      },

      '/getAvailablePlayers':{
        target: 'http://127.0.0.1:5001',
        changeOrigin: true,
        secure: false,
      }
    },
  },
})
