<template>
  <div>
    <div class="row">
      <div class="col-md-4 col-sm-12"><b>Type: </b>{{instance.type}}</div>
      <div class="col-md-4 col-sm-12"><b>Name: </b>{{instance.name}}</div>
      <div class="col-md-4 col-sm-12"><b>Created: </b>{{instance.created}}</div>
    </div>
    <div class="row" v-if="instance.description">
      <div class="col-12"><b>Description: </b>{{instance.description}}</div>
    </div>
    <div class="row" v-if="instance.data && instance.schema">
      <fieldset class="row">
        <legend>{{ instance.type }} fields</legend>
        <DisplayFields v-model="instance.data" :schema="instance.schema" v-if="instance.schema && instance.data"/>
      </fieldset>
    </div>
    <div class="row" v-if="instance.samples && instance.samples.length > 0">
      <div class="col-12">
        <b>Samples: </b>
        <span v-for="(s, i) in instance.samples" :key="i">
          <router-link :to="{ name: 'sample', params: {id: s.id} }">{{s.id}}</router-link>
          <span v-if="i != (instance.samples.length - 1)">, </span>
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
import DisplayFields from 'src/assets/jsonschema/displayFields.vue'
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
  },
  components: { DisplayFields }
}
</script>
