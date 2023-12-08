<template>
    <div class="q-pa-md" style="max-width: 300px">
        {{ options }}
      <div class="q-gutter-md">
        <q-badge color="secondary" multi-line>
          Model: "{{ model }}"
        </q-badge>
        <q-select outlined v-model="model" :options="options" label="Type"
            option-value="id"
            option-label="name"
            option-disable="inactive"
            map-options
            @update:model-value="val => selected(val)"
        />
      </div>
    </div>
  </template>

<script>
export default {
//   props: ['id', 'instance'],
  data () {
    return {
      model: this.instance,
      options: []
    }
  },
  methods: {
    selected (val) {
      console.log('selection', val)
      this.$emit('schema', val.schema)
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
