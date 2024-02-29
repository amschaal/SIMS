<template>
    <span v-if="value">
        <router-link v-if="routerName && id && value.id" :to="{ name: value[routerName], params: { id: value[id] }}">{{ getLabel }}</router-link>
        <span v-else>{{ getLabel }}</span>
    </span>
  </template>
<script>
export default {
  name: 'LibraryDetail',
  props: {
    label: { type: String, default () { return 'name' } },
    id: { type: String, default () { return 'id' } },
    routerName: String,
    value: { type: [Object, String, Number], default () { return {} } }
  },
  computed: {
    getLabel () {
      if (this.label && this.value[this.label]) {
        return this.value[this.label]
      } else if (this.id && this.value[this.id]) {
        return this.value[this.id]
      } else {
        return this.value
      }
    }
  }
}
</script>
