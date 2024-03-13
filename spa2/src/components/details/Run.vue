<template>
  <div>
    <div class="row">
      <div class="col-md-4 col-sm-12"><b>Type: </b><span v-if="run.type && run.type.name">{{run.type.name}}</span><span v-else>None</span></div>
      <div class="col-md-4 col-sm-12"><b>Machine: </b>{{run.machine}}</div>
      <div class="col-md-4 col-sm-12"><b>Name: </b>{{run.name}}</div>
      <div class="col-md-4 col-sm-12"><b>Created: </b>{{run.created}}</div>
    </div>
    <div class="row" v-if="run.description">
      <div class="col-12"><b>Description: </b>{{run.description}}</div>
    </div>
    <div class="row" v-if="run.data && run.schema && run.schema.properties">
      <fieldset class="col-12">
        <legend v-if="run.type">{{ run.type.name }} fields</legend>
        <DisplayFields v-model="run.data" :schema="run.schema" v-if="run.schema && run.data"/>
      </fieldset>
    </div>
    <table class="full-width">
        <thead><th>Index</th><th>Pool</th><th>Description</th></thead>
        <tbody>
        <tr v-for="(p, ind)  in pools" v-bind:key="p.id">
          <td :index="ind">{{ p.index }} </td>
          <td>
            <span v-if="p.pool">
              <router-link :to="{ name: 'pool', params: { id: p.pool.id }}">{{p.pool.name}}</router-link>
              <span v-if="p.pool.samples.length > 0"> ({{p.pool.samples.length}} samples)
                <q-tooltip>
                  {{p.pool.samples.map(s => s.id).join(', ')}}
                </q-tooltip>
              </span>
              <span v-if="p.pool.pools.length > 0"> ({{p.pool.pools.length}} pools)
                <q-tooltip>
                  {{p.pool.pools.map(p => p.name).join(', ')}}
                </q-tooltip>
              </span>
            </span>
          </td>
          <td>
          </td>
        </tr>
      </tbody>
      </table>
  </div>
</template>

<style>
</style>

<script>
import DisplayFields from 'src/assets/jsonschema/components/display/displayFields.vue'
import _ from 'lodash'
export default {
  name: 'RunDetail',
  props: ['id', 'instance'],
  data () {
    return {
      // instance: this.run
      data: null
    }
  },
  mounted: function () {
    if (!this.instance && this.id) {
      const self = this
      this.$api
        .get(`/api/runs/${self.id}/`)
        .then(function (response) {
          console.log('response', response)
          self.data = response.data
        })
    }
  },
  computed: {
    pools () {
      return _.orderBy(this.run.run_pools, 'index')
    },
    run () {
      return this.instance ? this.instance : this.data
    }
  },
  components: { DisplayFields }
}
</script>
