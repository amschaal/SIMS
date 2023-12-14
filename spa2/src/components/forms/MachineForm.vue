<template>
  <JSONForm
    ref="form"
    api-method="post"
    api-url="/api/machines/"
    :on-success="onSuccess"
    :on-error="onError"
    :hide-buttons="hideButtons"
  >
    <template v-slot:content="{ model, _errors, has_error }">
      Errors: {{ _errors }}
      <!-- <q-input outlined v-model="model.type" label="Type"
        :error-message="errors.type"
        :error="has_error.type"
        /> -->
      <q-input outlined v-model="model.name" label="Name"
        :error-message="_errors.name"
        :error="has_error.name"
        />
      <q-input outlined v-model="model.description" label="Description" />
      <q-input outlined v-model="model.num_lanes" type="number" label="Number of Cells/Lanes"
        :error-message="_errors.num_lanes"
        :error="has_error.num_lanes"
      />
      {{ model.data }}
    </template>
  </JSONForm>
</template>
<script>
import JSONForm from './JSONForm.vue'
export default {
  props: ['onSuccess', 'onError', 'hideButtons'],
  data () {
    return {
      model: { data: { foo: 'baz' }, type: 'machine_illumina_hiseq' }
    }
  },
  methods: {
  },
  components: {
    JSONForm
  }
}
</script>
