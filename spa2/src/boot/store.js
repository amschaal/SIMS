import { boot } from 'quasar/wrappers'
import { useJsonSchemaStore } from 'stores/jsonschema'
export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api
  const jsonschema = useJsonSchemaStore()
  jsonschema.refreshTypeSchemas()
  app.config.globalProperties.$store = {}
  app.config.globalProperties.$store.jsonschema = jsonschema
})
