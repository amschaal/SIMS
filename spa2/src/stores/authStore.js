import { defineStore } from 'pinia'
import { api } from 'src/boot/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    loading: false,
    error: null
  }),
  actions: {
    async fetchUser () {
      this.loading = true
      this.error = null

      try {
        const response = await api.get('/api/get_user')
        this.user = response.data.user
      } catch (err) {
        this.error = err
      } finally {
        this.loading = false
      }
    }
  }
})
