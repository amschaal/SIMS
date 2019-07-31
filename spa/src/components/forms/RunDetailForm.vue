<template>
  <BaseForm
    :model="model"
    ref="form"
    api-method="put"
    :api-url="`/api/runs/${model.id}/`"
    :on-success="onSuccess"
    :on-error="onError"
    :hide-buttons="hideButtons"
  >
    <template v-slot:content="{ data, errors, has_error }">
      <q-select outlined v-model="model.machine" :options="options" label="Machine"
        :error-message="errors.machine"
        :error="has_error.machine"
        option-value="id"
        option-label="name"
        emit-value
        map-options
        />
      <q-input outlined v-model="model.name" label="Name"
        :error-message="errors.name"
        :error="has_error.name"
        />
      <q-input outlined v-model="model.description" label="Description" />
    </template>
  </BaseForm>
</template>
<script>
import BaseForm from './BaseForm.vue'
export default {
  props: ['hideButtons', 'model'], // 'onSuccess', 'onError',
  data () {
    return {
      errors: {},
      data: {},
      options: [
      ]
    }
  },
  methods: {
    onSuccess: function () {
      this.$q.notify('Run updated.')
    },
    onError: function () {
      this.$q.notify('Error updating run.')
    }
  },
  mounted: function () {
    var self = this
    this.$axios.get('/api/machines/')
      .then(function (response) {
        self.options = response.data.results
      })
  },
  components: {
    BaseForm
  }
}
</script>
