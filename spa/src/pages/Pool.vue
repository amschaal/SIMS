<template>
  <q-page class="q-pa-md q-gutter-md">
    <h4 class="text-center">Pool</h4>
    <q-tabs
        v-model="tab"
      >
        <q-tab name="details" label="Details"/>
        <q-tab name="libraries" label="Libraries"/>
        <q-tab name="pools" label="Pools"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="details">
            <div class="text-h6">Pool</div>
            Pool {{pool.id}}
          </q-tab-panel>
          <q-tab-panel name="libraries">
            <div class="text-h6">Libraries</div>
            <TableDialog :table-component="LibrariesTable" :options="{'selection': 'multiple'}" ref="libraries" :on-select="addLibraries"/>
            <q-btn label="Add libraries" color="primary" @click="open('libraries')" />
            <LibrariesTable :filters="`pools__id=${id}`" ref="libraries_table"/>
          </q-tab-panel>
          <q-tab-panel name="pools">
            <div class="text-h6">Pools</div>
            <TableDialog :table-component="PoolsTable" :options="{'selection': 'multiple'}" ref="pools" :on-select="addPools"/>
            <q-btn label="Add pools" color="primary" @click="open('pools')" />
            <PoolsTable :filters="`pooled__id=${id}`" ref="pools_table"/>
          </q-tab-panel>
        </q-tab-panels>
  </q-page>
</template>

<style>
</style>

<script>
import Vue from 'vue'
import LibrariesTable from '../components/tables/LibrariesTable.vue'
import PoolsTable from '../components/tables/PoolsTable.vue'
import TableDialog from '../components/dialogs/TableDialog.vue'
// import PoolFormDialog from '../components/forms/PoolFormDialog.vue'
export default {
  name: 'pool',
  props: ['id'],
  data () {
    return {
      pool: {},
      tab: 'details',
      LibrariesTable: LibrariesTable,
      PoolsTable: PoolsTable
    }
  },
  methods: {
    addLibraries (libraries) {
      libraries = libraries.map(l => l.id)
      console.log('addLibraries', libraries)
      var self = this
      this.$axios
        .post(`/api/pools/${self.id}/add_libraries/`, { libraries: libraries })
        .then(function (response) {
          self.$q.notify('Libraries added.')
          self.$refs.libraries_table.$refs.table.refresh()
        })
        // .catch(function (error) {
        //   console.log(error.code)
        //   self.$q.notify('Failed to add libraries.')
        // })
    },
    addPools (pools) {
      pools = pools.map(p => p.id)
      var self = this
      this.$axios
        .post(`/api/pools/${self.id}/add_pools/`, { pools: pools })
        .then(function (response) {
          self.$q.notify('Pools added.')
          self.$refs.pools_table.$refs.table.refresh()
        })
    },
    open (table) {
      this.$refs[table].open()
    }
  },
  mounted: function () {
    var self = this
    this.$axios
      .get(`/api/pools/${self.id}/`)
      .then(function (response) {
        Vue.set(self, 'pool', response.data)
      })
  },
  components: {
    LibrariesTable,
    PoolsTable,
    TableDialog
    // PoolFormDialog
  }
}
</script>
