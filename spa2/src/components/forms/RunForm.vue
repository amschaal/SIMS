<template>
  <JSONTypeForm
    v-model="model"
    :errors="errors"
  >
    <template v-slot:content="{ model, errors, has_error }">
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
    <!-- <template #field_organism="{ v, data }">
      Just an example of how to override
      <div>
        <q-input type="textarea" v-model="data[v.variable]" label="OVERRIDDEN!!"/>
      </div>
    </template> -->
  </JSONTypeForm>
</template>
<script>
import JSONTypeForm from './JSONTypeForm.vue'
// import _ from 'lodash'
export default {
  props: ['modelValue', 'errors'],
  data () {
    return {
      options: [
      ],
      model: this.modelValue // _.cloneDeep(this.modelValue)
    }
  },
  mounted: function () {
    this.$api.get('/api/machines/')
      .then(response => {
        this.options = response.data.results
      })
  },
  components: {
    JSONTypeForm
  }
}
</script>
