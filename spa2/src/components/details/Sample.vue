<template>
  <div>
    <div class="row">
      <div class="col-md-4 col-sm-12"><b>ID: </b>{{sample.id}}</div>
      <div class="col-md-4 col-sm-12"><b>Project: </b><router-link :to="{ name: 'project', params: { id: sample.project }}">{{sample.project}}</router-link></div>
      <div class="col-md-4 col-sm-12"><b>Type: </b><span v-if="sample.type">{{sample.type.name}}</span><span v-else>{{sample.type}}</span></div>
    </div>
    <div class="row">
      <div class="col-md-4 col-sm-12"><b>Name: </b>{{sample.name}}</div>
      <div class="col-md-4 col-sm-12"><b>Alias: </b>{{sample.alias}}</div>
      <div class="col-md-4 col-sm-12"><b>Imported: </b>{{$filters.formatDate(sample.imported)}}<span v-if="sample.submission"> from <router-link  :to="{ name: 'submission', params: { id: sample.submission }}">submission</router-link></span></div>
      <div class="col-md-4 col-sm-12" v-if="sample && sample.pools && sample.pools.length">
        <b>Pools: </b>
        <router-link v-for="(pool, index) in sample.pools" :key="pool.id" :to="{ name: 'pool', params: { id: pool.id }}"><template v-if="index > 0">, </template> {{pool.name}}</router-link></div>
    </div>
    <fieldset class="col-12" v-if="barcodes">
      <legend>Barcodes</legend>
      <div class="row">
        <div class="col-md-3 col-sm-12" v-if="barcodes.i5"><b>i5: </b>{{barcodes.i5}}</div>
        <div class="col-md-3 col-sm-12" v-if="barcodes.i7"><b>i7: </b>{{barcodes.i7}}</div>
        <div class="col-md-3 col-sm-12" v-if="barcodes.adapter_db"><b>Adapter DB: </b>{{barcodes.adapter_db}}</div>
        <div class="col-md-3 col-sm-12" v-if="barcodes.adapter"><b>Adapter: </b>{{barcodes.adapter}}</div>
      </div>
    </fieldset>
    <div class="row" v-if="sample.data && sample.type && sample.schema">
      <fieldset class="col-12">
        <legend>{{ sample.type.name }} fields</legend>
        <DisplayFields v-model="sample.data" :schema="sample.schema" v-if="sample.schema && sample.data"/>
      </fieldset>
    </div>
    <!-- <div class="row">
      <div class="col-12" v-for="(v, k) in sample.data" :key="k"><b>{{k}}: </b>{{v}}</div>
    </div> -->
  </div>
</template>

<style>
</style>

<script>
import DisplayFields from 'src/assets/jsonschema/components/display/displayFields.vue'
import _ from 'lodash'
export default {
  name: 'SampleDetail',
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
        .get(`/api/sample/${self.id}/`)
        .then(function (response) {
          console.log('response', response)
          self.data = response.data
        })
    }
  },
  computed: {
    sample () {
      return this.instance || this.data
    },
    barcodes () {
      return _.isEmpty(this.sample.barcodes) ? null : this.sample.barcodes
    }
  },
  components: {
    DisplayFields
  }
}

// import { defineComponent, ref } from 'vue'

// export default defineComponent({
//   name: 'sample',
//   props: ['id', 'sample'],
//   components: {
//   },

//   setup () {
//     if (!this.project) {
//       var self = this
//       this.$api
//         .get(`/api/sample/${self.id}/`)
//         .then(function (response) {
//           console.log('response', response)
//           Vue.set(self, 'sample', response.data)
//         })
//     }
//   }
// })

</script>
