<template>
  <JSONTypeForm
    v-model="model"
    :errors="errors"
    model-filter="machine"
  >
    <template v-slot:content="{ model, errors, has_error }">
      Model: {{ model }}
      Errors: {{ errors }}

      <!-- <q-input outlined v-model="model.type" label="Type"
        :error-message="errors.type"
        :error="has_error.type"
        /> -->
      <q-input outlined v-model="model.id" label="ID"
        :error-message="errors.id"
        :error="has_error.id"
        />
      <q-input outlined v-model="model.name" label="Name"
        :error-message="errors.name"
        :error="has_error.name"
        />
      <q-input outlined v-model="model.description" label="Description" />
      <q-input outlined v-model="model.num_lanes" type="number" label="Number of Cells/Lanes"
        :error-message="errors.num_lanes"
        :error="has_error.num_lanes"
      />
      {{ model.data }}
    </template>
  </JSONTypeForm>
</template>
<script>
import JSONTypeForm from './JSONTypeForm.vue'
export default {
  props: ['errors', 'modelValue'],
  data () {
    return {
      model: this.modelValue
    }
  },
  methods: {
  },
  components: {
    JSONTypeForm
  }
}
</script>
