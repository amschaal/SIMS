<template>
  <JSONForm
    v-model="model"
    ref="form"
    :api-method="model && model.id ? 'put' : 'post'"
    :api-url="model && model.id ? `/api/pools/${model.id}/` : '/api/pools/'"
    :on-success="onSuccessMethod"
    :on-error="onErrorMethod"
    :hide-buttons="hideButtons"
  >
    <template v-slot:content="{ model, errors, has_error }">
      <q-input outlined v-model="model.name" label="Name"
        :error-message="errors.name"
        :error="has_error.name"
        />
      <q-input outlined v-model="model.description" label="Description"
        :error-message="errors.name"
        :error="has_error.name"
        />
    </template>
  </JSONForm>
</template>
<script>
import JSONForm from './JSONForm.vue'

export default {
  props: ['onSuccess', 'onError', 'hideButtons', 'modelValue'],
  emits: ['update:modelValue'],
  data () {
    return {
      errors: {},
      model: this.modelValue,
      options: [
      ]
    }
  },
  methods: {
    onErrorMethod (error) {
      if (error) {
        this.$q.notify({ color: 'negative', message: this.model.id ? 'Error updating pool' : 'Error creating pool.' })
      }
      if (this.onError) {
        this.onError(error)
      }
    },
    onSuccessMethod (request) {
      console.log('pool!', request)
      this.$emit('update:modelValue', this.model)
      this.$q.notify(this.model.id ? 'Pool updated.' : 'Pool created.')
      if (this.onSuccess) {
        this.onSuccess(request)
      }
    }
  },
  mounted: function () {
    console.log('poolForm', this.modelValue)
  },
  components: {
    JSONForm
  }
}
</script>
