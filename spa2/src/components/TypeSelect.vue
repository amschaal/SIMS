<template>
    <q-select outlined v-model="model" :options="filtered_options" label="Type" ref="select"
        option-value="id"
        option-label="name"
        @update:modelValue="val => selected(val)"
        :error-message="error_messages[field_name]"
        :error="has_error[field_name]"
        :clearable="clearable"
    />
</template>

<script>
export default {
  props: ['modelValue', 'error_messages', 'has_error', 'emit_object', 'modelFilter', 'field', 'clearable'],
  emits: ['update:modelValue', 'schema'],
  data () {
    return {
      model: this.modelValue,
      options: this.$store.jsonschema.getSchemas,
      field_name: this.field || 'type'
    }
  },
  methods: {
    selected (val) {
      this.model = val
      if (val && val.schema) {
        this.$emit('schema', val.schema)
      } else {
        this.$emit('schema', null)
      }
      if (val) {
        this.$emit('update:modelValue', this.emit_object !== undefined ? val : val.id)
      } else {
        this.$emit('update:modelValue', null)
      }
    }
  },
  mounted: function () {
    console.log('mount TypeSelect', this.modelValue)
    // this.$api
    //   .get('/api/model_types/')
    //   .then(response => {
    //     this.options = response.data.results
    //     const opt = this.options.find(opt => opt.id === this.model)
    //     if (opt && opt.schema) {
    //       console.log('emit schema', opt.id, opt.schema)
    //       // this.$emit('schema', opt.schema)
    //       this.selected(opt)
    //     }
    //   })
    const opt = this.options.find(opt => opt.id === this.model)
    if (opt && opt.schema) {
      console.log('emit schema', opt.id, opt.schema)
      // this.$emit('schema', opt.schema)
      this.selected(opt)
    }
  },
  computed: {
    filtered_options () {
      return this.modelFilter ? this.options.filter(o => o.model === this.modelFilter) : this.options
    }
  }
}
</script>
