<template>
    <q-input
      v-model="text"
      filled
      type="textarea"
      style="width:100%"
      @update:model-value="onInput"
    />
</template>
<script>
// import Vue from 'vue'

export default {
  props: ['modelValue'],
  data () {
    return {
      text: this.modelValue
    }
  },
  methods: {
    onInput () {
      alert('changed')
      this.$emit('update:model-value', this.text)
    }
  },
  mounted () {
    // Vue.nextTick(() => {
    // })
  }
}
</script>
