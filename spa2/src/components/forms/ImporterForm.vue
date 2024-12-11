<template>
  <BaseForm :api-url="`/api/importers/`" api-method="post" v-model="model" :on-success="onSuccess" :on-error="onError">
      <template v-slot:content="{ model, errors, has_error }">
        <q-input outlined v-model="model.name" label="Name"
          :error-message="errors.name"
          :error="has_error.name"
          />
        <q-input
          outlined
          v-model="model.description"
          label="Description"
          :error-message="errors.description"
          :error="has_error.description"
          />
      </template>
    </BaseForm>
</template>
<script>
import BaseForm from './BaseForm.vue'
export default {
  props: ['errors', 'modelValue', 'onSuccess'],
  data () {
    return {
      model: this.modelValue
    }
  },
  methods: {
    onError () {
      this.$q.notify({
        type: 'negative',
        message: 'Error creating submission type importer.'
      })
    }
  },
  components: {
    BaseForm
  }
}
</script>
