<template>
    <q-select outlined v-model="model" :options="options" label="Type" ref="select"
        option-value="id"
        option-label="name"
        @update:modelValue="val => selected(val)"
    />
</template>

<script>
export default {
  props: ['modelValue'],
  emits: ['update:modelValue'],
  data () {
    return {
      model: this.modelValue,
      options: []
    }
  },
  methods: {
    selected (val) {
      this.$emit('update:modelValue', val)
    }
  },
  mounted: function () {
    this.$api
      .get('/api/submission_types/?order_by=sort_order')
      .then(response => {
        this.options = response.data.results
      })
  }
}
</script>
