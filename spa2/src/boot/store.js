import { boot } from 'quasar/wrappers'
import { useJsonSchemaStore } from 'stores/jsonschema'
import { useAuthStore } from 'stores/authStore'
export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api
  const jsonschema = useJsonSchemaStore()
  jsonschema.refreshTypeSchemas()
  const authStore = useAuthStore()
  authStore.fetchUser()
  app.config.globalProperties.$store = {}
  app.config.globalProperties.$store.jsonschema = jsonschema
  app.config.globalProperties.$store.auth = userStore
})
