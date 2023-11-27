<template>
  <BaseForm
    :model="model"
    ref="form"
    api-method="post"
    api-url="/api/machines/"
    :on-success="onSuccess"
    :on-error="onError"
    :hide-buttons="hideButtons"
  >
    <template v-slot:content="{ model, errors, has_error }">
      <q-input outlined v-model="model.name" label="Name"
        :error-message="errors.name"
        :error="has_error.name"
        />
      <q-input outlined v-model="model.description" label="Description" />
      <q-input outlined v-model="model.num_lanes" type="number" label="Number of Cells/Lanes"
        :error-message="errors.num_lanes"
        :error="has_error.num_lanes"
      />
    </template>
  </BaseForm>
</template>
<script>
import BaseForm from './BaseForm.vue'
export default {
  props: ['onSuccess', 'onError', 'hideButtons'],
  data () {
    return {
      errors: {},
      model: {}
    }
  },
  components: {
    BaseForm
  }
}
</script>
