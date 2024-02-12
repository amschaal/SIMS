import { boot } from 'quasar/wrappers'
import SchemaForm from 'src/assets/jsonschema/forms/SchemaForm.vue'

export default boot(({ app }) => {
  // registering this because there seem to be issues when using this component recursively from inside SchemaDialog
  app.component('SchemaForm', SchemaForm)
})
