<template>
  <q-page class="">
    <q-tabs
        v-model="tab"
      >
        <q-tab name="details" label="Details"/>
        <q-tab name="libraries" label="Libraries"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="details">
            <div class="text-h6">Sample</div>
            Sample {{sample.id}}
          </q-tab-panel>
          <q-tab-panel name="libraries">
            <div class="text-h6">Libraries</div>
            <!-- <SamplesTable/> -->
          </q-tab-panel>
        </q-tab-panels>
  </q-page>
</template>

<style>
</style>

<script>
import Vue from 'vue'
// import SamplesTable from '../components/SamplesTable.vue'
export default {
  name: 'sample',
  props: ['id'],
  data () {
    return {
      sample: {},
      tab: 'details'
    }
  },
  mounted: function () {
    var self = this
    this.$axios
      .get(`/api/samples/${self.id}/`)
      .then(function (response) {
        console.log('response', response)
        Vue.set(self, 'sample', response.data)
      })
  },
  components: {
    // SamplesTable
  }
}
</script>
