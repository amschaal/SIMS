<template>
  <div>
    <div class="row">
      <div class="col-md-4 col-sm-12"><b>ID: </b>{{sample.id}}</div>
      <div class="col-md-4 col-sm-12"><b>Project: </b><router-link :to="{ name: 'project', params: { id: sample.project }}">{{sample.project}}</router-link></div>
    </div>
    <div class="row">
      <div class="col-md-4 col-sm-12"><b>Name: </b>{{sample.name}}</div>
      <div class="col-md-4 col-sm-12"><b>Imported: </b>{{sample.imported | formatDate}}</div>
    </div>
    <div class="row">
      <div class="col-12" v-for="(v, k) in sample.data" :key="k"><b>{{k}}: </b>{{v}}</div>
    </div>
  </div>
</template>

<style>
</style>

<script>
import Vue from 'vue'
export default {
  name: 'sample',
  props: ['id', 'sample'],
  data () {
    return {
      // project: this.instance
    }
  },
  mounted: function () {
    if (!this.project) {
      var self = this
      this.$axios
        .get(`/api/sample/${self.id}/`)
        .then(function (response) {
          console.log('response', response)
          Vue.set(self, 'sample', response.data)
        })
    }
  }
}
</script>
