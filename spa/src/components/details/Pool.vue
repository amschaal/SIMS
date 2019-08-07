<template>
  <div>
    <div class="row">
      <div class="col-md-4 col-sm-12"><b>Name: </b>{{pool.name}}</div>
      <div class="col-md-4 col-sm-12"><b>Created: </b>{{pool.created | formatDate}}</div>
    </div>
    <div class="row" v-if="pool.description">
      <div class="col-12"><b>Description: </b>{{pool.description}}</div>
    </div>
    <div class="row" v-if="pool.libraries && pool.libraries.length > 0">
      <div class="col-12">
        <b>Libraries: </b>
        <span v-for="(l, i) in pool.libraries" :key="i">
          <router-link :to="{ name: 'library', params: {id: l.id} }">{{l.id}}</router-link>
          <span v-if="i != (pool.libraries.length - 1)">, </span>
        </span>
      </div>
    </div>
    <div class="row" v-if="pool.pools && pool.pools.length > 0">
      <div class="col-12">
        <b>Pools: </b>
        <span v-for="(p, i) in pool.pools" :key="i">
          <router-link :to="{ name: 'pool', params: {id: p.id} }">{{p.name}}</router-link>
          <span v-if="i != (pool.pools.length - 1)">, </span>
        </span>
      </div>
    </div>
  </div>
</template>

<style>
</style>

<script>
import Vue from 'vue'
export default {
  name: 'pool',
  props: ['id', 'pool'],
  mounted: function () {
    if (!this.pool) {
      var self = this
      this.$axios
        .get(`/api/pools/${self.id}/`)
        .then(function (response) {
          console.log('response', response)
          Vue.set(self, 'pool', response.data)
        })
    }
  }
}
</script>
