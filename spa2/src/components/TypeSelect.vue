<template>
    <q-select outlined v-model="model" :options="options" label="Type"
        option-value="id"
        option-label="name"
        option-disable="inactive"
        map-options
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
      console.log('selection', val.id)
      this.$emit('schema', val.schema)
      this.$emit('update:model-value', val.id)
    }
  },
  mounted: function () {
    this.$api
      .get('/api/model_types/')
      .then(response => {
        this.options = response.data.results
      })
  }
}
</script>
