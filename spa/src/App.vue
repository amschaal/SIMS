<template>
  <div id="q-app">
    <router-view />
  </div>
</template>

<script>
import Vue from 'vue'
import { date } from 'quasar'

Vue.filter('formatDate', function (value) {
  if (value) {
    return date.formatDate(String(value), 'MM/DD/YYYY hh:mm')
  }
})
export default {
  name: 'App'
}
</script>

<style>
</style>
