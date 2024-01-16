<template>
  <div>
    <div class="row">
      <div class="col-md-4 col-sm-12"><b>Type: </b>{{pool.type}}</div>
      <div class="col-md-4 col-sm-12"><b>Name: </b>{{pool.name}}</div>
      <div class="col-md-4 col-sm-12"><b>Created: </b>{{pool.created}}</div>
    </div>
    <div class="row" v-if="pool.description">
      <div class="col-12"><b>Description: </b>{{pool.description}}</div>
    </div>
    <div class="row" v-if="pool.data && pool.schema">
      <fieldset class="row">
        <legend>{{ pool.type }} fields</legend>
        <DisplayFields v-model="pool.data" :schema="pool.schema" v-if="pool.schema && pool.data"/>
      </fieldset>
    </div>
    <div class="row" v-if="pool.samples && pool.samples.length > 0">
      <div class="col-12">
        <b>Samples: </b>
        <span v-for="(s, i) in pool.samples" :key="i">
          <router-link :to="{ name: 'sample', params: {id: s.id} }">{{s.id}}</router-link>
          <span v-if="i != (pool.samples.length - 1)">, </span>
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
import DisplayFields from 'src/assets/jsonschema/displayFields.vue'
export default {
  name: 'PoolDetail',
  props: ['id', 'instance'],
  data () {
    return {
      data: this.instance
    }
  },
  mounted: function () {
    if (!this.instance) {
      const self = this
      this.$api
        .get(`/api/pools/${self.id}/`)
        .then(function (response) {
          console.log('response', response)
          self.data = response.data
        })
    }
  },
  computed: {
    pool () {
      return this.instance ? this.instance : this.data
    }
  },
  components: { DisplayFields }
}
</script>
