<template>
  <BaseForm
    :model="data"
    ref="form"
    api-method="post"
    api-url="/api/runs/"
    :on-success="onSuccess"
    :on-error="onError"
    :hide-buttons="hideButtons"
  >
    <template v-slot:content="{ data, errors, has_error }">
      <q-select outlined v-model="data.machine" :options="options" label="Machine"
        :error-message="errors.machine"
        :error="has_error.machine"
        option-value="id"
        option-label="name"
        emit-value
        map-options
        />
      <q-input outlined v-model="data.name" label="Name"
        :error-message="errors.name"
        :error="has_error.name"
        />
      <q-input outlined v-model="data.description" label="Description" />
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
      data: {},
      options: [
      ]
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
