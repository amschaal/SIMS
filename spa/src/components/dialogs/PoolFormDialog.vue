<template>
  <FormDialog
    :model="model"
    ref="dialog"
    title="Create Pool"
    api-method="post"
    api-url="/api/pools/"
    :on-success="onSuccess"
    :on-error="onError">
    <template v-slot:content="{ data, errors, has_error }">
      Pool
      <q-input outlined v-model="data.name" label="Name"
        :error-message="errors.name"
        :error="has_error.name"
        />
      <q-input outlined v-model="data.description" label="Description" />
    </template>
  </FormDialog>
</template>
<script>
import FormDialog from './FormDialog.vue'
export default {
  props: ['model', 'apiUrl', 'apiMethod', 'onSuccess', 'onError'],
  data () {
    return {
      errors: {},
      data: this.model
    }
  },
  // methods: {
  // },
  // mounted: function () {
  //
  // },
  components: {
    FormDialog
  }
}
</script>
