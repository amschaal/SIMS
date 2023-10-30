<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h6 class="text-center"><router-link :to="{ name: 'runs'}">Runs</router-link> / {{run.name}}</h6>
    <DeleteButton :url="`/api/runs/${id}/`"/>
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
import RunDetailForm from '../components/forms/RunDetailForm.vue'
import LibrariesTable from '../components/tables/LibrariesTable.vue'
import PoolsTable from '../components/tables/PoolsTable.vue'
import DeleteButton from '../components/DeleteButton.vue'
export default {
  name: 'RunPage',
  props: ['id'],
  data () {
    return {
      run: {},
      tab: 'details'
    }
  },
  mounted: function () {
    const self = this
    this.$api
      .get(`/api/runs/${self.id}/`)
      .then(function (response) {
        self.run = response.data
      })
  },
  components: {
    LibrariesTable,
    PoolsTable,
    RunDetailForm,
    DeleteButton
  }
}
</script>
