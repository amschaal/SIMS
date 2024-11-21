import { defineStore } from 'pinia'
import { api } from 'src/boot/axios'

export const useJsonSchemaStore = defineStore('jsonschema', {
  state: () => ({
    schemas: [],
    loadingSchemas: false,
    modelSchemas: {
      project: {},
      sample: {},
      pool: {}
    }
  }),
  getters: {
    typeSchemas: (state) => {
      const typeSchemas = {}
      state.schemas.forEach(t => {
        typeSchemas[t.id] = t
      })
      return typeSchemas
    },
    getSchemas: (state) => {
      return state.schemas
    }
  },
  actions: {
    async refreshTypeSchemas () {
      // try {
      console.log('refresh schemas')
      const data = await api.get('/api/model_types/?page_size=100')
      this.schemas = data.data.results
      // } catch {
      //   throw Error('Unable to fetch model type schemas')
      // }
    },
    async getTypeSchema (typeId) {
      if (!this.typeSchemas) {
        await this.refreshTypeSchemas()
      }
      return this.typeSchemas[typeId]
    }
  }
})
