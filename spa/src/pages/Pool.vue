<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h6 class="text-center"><router-link :to="{ name: 'pools'}">Pools</router-link> / {{pool.name}}</h6>
    <DeleteButton :url="`/api/pools/${id}/`" :redirect="{name: 'pools'}"/>
    <q-tabs
        v-model="tab"
      >
        <q-tab name="details" label="Details"/>
        <q-tab name="libraries" label="Libraries"/>
        <q-tab name="pools" label="Pools"/>
        <q-tab name="runs" label="Runs"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="details">
            <Pool :pool="pool"/>
          </q-tab-panel>
          <q-tab-panel name="libraries">
            <TableDialog :table-component="LibrariesTable" :options="{'selection': 'multiple'}" ref="libraries" :on-select="addLibraries"/>
            <q-btn label="Add libraries" color="primary" @click="open('libraries')" class="on-left"/>
            <q-btn label="Remove selected" color="negative" @click="removeLibraries" />
            <LibrariesTable :filters="`pools__id=${id}`" ref="libraries_table" :options="{'selection': 'multiple'}"/>
          </q-tab-panel>
          <q-tab-panel name="pools">
            <TableDialog :table-component="PoolsTable" :options="{'selection': 'multiple'}" ref="pools" :on-select="addPools"/>
            <q-btn label="Add pools" color="primary" @click="open('pools')" class="on-left"/>
            <q-btn label="Remove selected" color="negative" @click="removePools" />
            <PoolsTable :filters="`pooled__id=${id}`" ref="pools_table" :options="{'selection': 'multiple'}"/>
          </q-tab-panel>
          <q-tab-panel name="runs">
            <RunsTable :filters="`run_pools__pool__id=${id}`" ref="runs_table"/>
          </q-tab-panel>
        </q-tab-panels>
  </q-page>
</template>

<style>
</style>

<script>
import Vue from 'vue'
import Pool from '../components/details/Pool.vue'
import LibrariesTable from '../components/tables/LibrariesTable.vue'
import PoolsTable from '../components/tables/PoolsTable.vue'
import RunsTable from '../components/tables/RunsTable.vue'
import TableDialog from '../components/dialogs/TableDialog.vue'
import DeleteButton from '../components/DeleteButton.vue'
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
        .catch(function (error) {
          console.log(error.response)
          self.$q.notify({ color: 'negative', message: 'Failed to add libraries.' })
        })
    },
    removeLibraries (libraries) {
      libraries = this.$refs.libraries_table.$refs.table.selected.map(l => l.id)
      console.log('removeLibraries', libraries)
      var self = this
      this.$axios
        .post(`/api/pools/${self.id}/remove_libraries/`, { libraries: libraries })
        .then(function (response) {
          self.$q.notify('Libraries removed.')
          self.$refs.libraries_table.$refs.table.selected = []
          self.$refs.libraries_table.$refs.table.refresh()
        })
        .catch(function (error) {
          console.log(error.code)
          self.$q.notify({ color: 'negative', message: 'Failed to remove libraries.' })
        })
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
        .catch(function (error) {
          console.log(error.code)
          self.$q.notify({ color: 'negative', message: 'Failed to add pools.' })
        })
    },
    removePools (pools) {
      pools = this.$refs.pools_table.$refs.table.selected.map(l => l.id)
      var self = this
      this.$axios
        .post(`/api/pools/${self.id}/remove_pools/`, { pools: pools })
        .then(function (response) {
          self.$q.notify('Pools removed.')
          self.$refs.pools_table.$refs.table.selected = []
          self.$refs.pools_table.$refs.table.refresh()
        })
        .catch(function (error) {
          console.log(error.code)
          self.$q.notify({ color: 'negative', message: 'Failed to remove pools.' })
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
    Pool,
    LibrariesTable,
    PoolsTable,
    RunsTable,
    TableDialog,
    DeleteButton
    // PoolFormDialog
  }
}
</script>
