import { defineStore } from 'pinia'
import { api } from 'src/boot/axios'

export const useJsonSchemaStore = defineStore('jsonschema', {
  state: () => ({
    typeSchemas: null,
    loadingSchemas: false,
    modelSchemas: {
      project: {},
      sample: {},
      pool: {}
    }
  }),
  getters: {
  },
  actions: {
    async refreshTypeSchemas () {
      const data = await api.get('/api/model_types/')
      this.typeSchemas = {}
      data.data.results.forEach(t => {
        this.typeSchemas[t.id] = t
      })
    },
    async getTypeSchema (typeId) {
      if (!this.typeSchemas) {
        await this.refreshTypeSchemas()
      }
      return this.typeSchemas[typeId]
    }
  }
})
