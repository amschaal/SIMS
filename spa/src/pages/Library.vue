<template>
  <q-page class="q-pa-md q-gutter-md">
    <h4 class="text-center">Library</h4>
    <q-tabs
        v-model="tab"
      >
        <q-tab name="details" label="Details"/>
        <q-tab name="pools" label="Pools"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="details">
            <div class="text-h6">Library</div>
            Library {{library.id}}
          </q-tab-panel>
          <q-tab-panel name="pools">
            <PoolsTable :filters="`libraries__id=${id}`"/>
          </q-tab-panel>
        </q-tab-panels>
  </q-page>
</template>

<style>
</style>

<script>
import Vue from 'vue'
import PoolsTable from '../components/tables/PoolsTable.vue'
export default {
  name: 'library',
  props: ['id'],
  data () {
    return {
      library: {},
      tab: 'details'
    }
  },
  mounted: function () {
    var self = this
    this.$axios
      .get(`/api/libraries/${self.id}/`)
      .then(function (response) {
        Vue.set(self, 'library', response.data)
      })
  },
  components: {
    PoolsTable
  }
}
</script>
