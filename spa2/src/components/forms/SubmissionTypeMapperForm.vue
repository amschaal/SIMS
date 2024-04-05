<template>
  <BaseForm :api-url="`/api/submission_type_mappers/`" api-method="post" v-model="model" :on-success="onSuccess" :on-error="onError">
      <template v-slot:content="{ model, errors, has_error }">
        <TypeSelect v-model="model.model_type" model-filter="project" :error_messages="errors" :has_error="has_error" field="model_type"/>
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
import TypeSelect from '../TypeSelect.vue'
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
        message: 'Error creating submission type mapper.'
      })
    }
  },
  components: {
    BaseForm,
    TypeSelect
  }
}
</script>
