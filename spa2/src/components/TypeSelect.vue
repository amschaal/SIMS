<template>
    <q-select outlined v-model="model" :options="options" label="Type" ref="select"
        option-value="id"
        option-label="name"
        @update:model-value="val => selected(val)"
    />
</template>

<script>
export default {
  props: ['modelValue'],
  data () {
    return {
      model: this.modelValue,
      options: []
    }
  },
  methods: {
    selected (val) {
      this.$emit('schema', val.schema)
      this.$emit('update:model-value', val.id)
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
