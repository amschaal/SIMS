<template>
  <div v-if="library">{{ library }}
    <div class="row">
      <div class="col-md-4 col-sm-12"><b>ID: </b>{{library.id}}</div>
      <div class="col-md-4 col-sm-12"><b>Sample: </b><router-link :to="{ name: 'sample', params: { id: library.sample }}">{{library.sample}}</router-link></div>
      <div class="col-md-4 col-sm-12" ><b>Barcode: </b><router-link v-if="library.barcode" :to="{ name: 'adapter', params: { id: library.barcode }}">{{library.barcode}}</router-link> <span v-else>None</span></div>
    </div>
    <div class="row">
      <div class="col-md-4 col-sm-12"><b>Project: </b><router-link :to="{ name: 'project', params: { id: library.project }}">{{library.project}}</router-link></div>
      <div class="col-md-4 col-sm-12"><b>Created: </b>{{library.created}}</div>
    </div>
    <div class="row" v-if="library.description">
      <div class="col-12"><b>Description: </b>{{library.description}}</div>
    </div>
  </div>
</template>

<style>
</style>

<script>
export default {
  name: 'LibraryDetail',
  props: ['id', 'instance'],
  data () {
    return {
      library: this.instance
    }
  },
  mounted: function () {
    if (!this.instance) {
      const self = this
      this.$api
        .get(`/api/libraries/${self.id}/`)
        .then(function (response) {
          console.log('response', response)
          self.library = response.data
        })
    }
  }
}
</script>
