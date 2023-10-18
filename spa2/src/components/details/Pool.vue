<template>
  <div>
    <div class="row">
      <div class="col-md-4 col-sm-12"><b>Name: </b>{{instance.name}}</div>
      <div class="col-md-4 col-sm-12"><b>Created: </b>{{instance.created}}</div>
    </div>
    <div class="row" v-if="instance.description">
      <div class="col-12"><b>Description: </b>{{instance.description}}</div>
    </div>
    <div class="row" v-if="instance.libraries && instance.libraries.length > 0">
      <div class="col-12">
        <b>Libraries: </b>
        <span v-for="(l, i) in instance.libraries" :key="i">
          <router-link :to="{ name: 'library', params: {id: l.id} }">{{l.id}}</router-link>
          <span v-if="i != (instance.libraries.length - 1)">, </span>
        </span>
      </div>
    </div>
    <div class="row" v-if="instance.pools && instance.pools.length > 0">
      <div class="col-12">
        <b>Pools: </b>
        <span v-for="(p, i) in instance.pools" :key="i">
          <router-link :to="{ name: 'pool', params: {id: p.id} }">{{p.name}}</router-link>
          <span v-if="i != (instance.pools.length - 1)">, </span>
        </span>
      </div>
    </div>
  </div>
</template>

<style>
</style>

<script>
export default {
  name: 'PoolDetail',
  props: ['id', 'pool'],
  data () {
    return {
      instance: this.pool
    }
  },
  mounted: function () {
    if (!this.instance) {
      const self = this
      this.$api
        .get(`/api/pools/${self.id}/`)
        .then(function (response) {
          console.log('response', response)
          self.instance = response.data
        })
    }
  }
}
</script>
