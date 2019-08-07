<template>
  <div>
    <div class="row">
      <div class="col-md-4 col-sm-12"><b>ID: </b>{{library.id}}</div>
      <div class="col-md-4 col-sm-12"><b>Sample: </b><router-link :to="{ name: 'sample', params: { id: library.sample }}">{{library.sample}}</router-link></div>
      <div class="col-md-4 col-sm-12"><b>Barcode: </b><router-link :to="{ name: 'adapter', params: { id: library.barcode }}">{{library.barcode}}</router-link></div>
    </div>
    <div class="row">
      <div class="col-md-4 col-sm-12"><b>Project: </b><router-link :to="{ name: 'project', params: { id: library.project }}">{{library.project}}</router-link></div>
      <div class="col-md-4 col-sm-12"><b>Created: </b>{{library.created | formatDate}}</div>
    </div>
    <div class="row" v-if="library.description">
      <div class="col-12"><b>Description: </b>{{library.description}}</div>
    </div>
  </div>
</template>

<style>
</style>

<script>
import Vue from 'vue'
export default {
  name: 'library',
  props: ['id', 'library'],
  mounted: function () {
    if (!this.project) {
      var self = this
      this.$axios
        .get(`/api/library/${self.id}/`)
        .then(function (response) {
          console.log('response', response)
          Vue.set(self, 'library', response.data)
        })
    }
  }
}
</script>
