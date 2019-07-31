<template>
  <q-page class="q-pa-md q-gutter-md">
    <q-tabs
        v-model="tab"
      >
        <q-tab name="details" label="Details"/>
        <q-tab name="libraries" label="Libraries"/>
        <q-tab name="pools" label="Pools"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="details">
            <div class="text-h6">Run</div>
            <RunDetailForm :model="run"/>
          </q-tab-panel>
          <q-tab-panel name="libraries">
            <div class="text-h6">Libraries</div>
            <LibrariesTable :filters="`pools__run_pools__run__id=${id}`"/>
          </q-tab-panel>
          <q-tab-panel name="pools">
            <div class="text-h6">Pools</div>
            <PoolsTable :filters="`run_pools__run__id=${id}`"/>
          </q-tab-panel>
        </q-tab-panels>
  </q-page>
</template>

<style>
</style>

<script>
import Vue from 'vue'
import RunDetailForm from '../components/forms/RunDetailForm.vue'
import LibrariesTable from '../components/tables/LibrariesTable.vue'
import PoolsTable from '../components/tables/PoolsTable.vue'
export default {
  name: 'run',
  props: ['id'],
  data () {
    return {
      run: {},
      tab: 'details'
    }
  },
  mounted: function () {
    var self = this
    this.$axios
      .get(`/api/runs/${self.id}/`)
      .then(function (response) {
        Vue.set(self, 'run', response.data)
      })
  },
  components: {
    LibrariesTable,
    PoolsTable,
    RunDetailForm
  }
}
</script>
