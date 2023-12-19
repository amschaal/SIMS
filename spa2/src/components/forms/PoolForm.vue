<template>
  <JSONForm
    :model="model"
    ref="form"
    api-method="post"
    api-url="/api/pools/"
    :on-success="onSuccess"
    :on-error="onError"
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
  props: ['onSuccess', 'onError', 'hideButtons'],
  data () {
    return {
      errors: {},
      model: {},
      options: [
      ]
    }
  },
  mounted: function () {
  },
  components: {
    JSONForm
  }
}
</script>
