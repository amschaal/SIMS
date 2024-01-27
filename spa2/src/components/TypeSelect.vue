<template>
    <q-select outlined v-model="model" :options="options" label="Type" ref="select"
        option-value="id"
        option-label="name"
        @update:modelValue="val => selected(val)"
        :error-message="error_messages.type"
        :error="has_error.type"
    />
</template>

<script>
export default {
  props: ['modelValue', 'error_messages', 'has_error', 'emit_object'],
  emits: ['update:modelValue', 'schema'],
  data () {
    return {
      model: this.modelValue,
      options: []
    }
  },
  methods: {
    selected (val) {
      this.$emit('schema', val.schema)
      this.$emit('update:modelValue', this.emit_object ? val : val.id)
    }
  },
  mounted: function () {
    this.$api
      .get('/api/model_types/')
      .then(response => {
        this.options = response.data.results
        const opt = this.options.find(opt => opt.id === this.model)
        if (opt && opt.schema) {
          this.$emit('schema', opt.schema)
        }
      })
  }
}
</script>
