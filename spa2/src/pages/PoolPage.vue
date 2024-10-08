<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h6 class="text-center"><router-link :to="{ name: 'pools'}">Pools</router-link> / {{pool.name}}</h6>
    <DeleteButton :url="`/api/pools/${id}/`" :redirect="{name: 'pools'}"/>
    <q-btn label="Lock" color="primary" @click="lock" v-if="pool && !pool.locked"/>
    <q-btn label="Unlock" color="positive" @click="unlock" v-if="pool && pool.locked"/>
    <q-tabs
        v-model="tab"
      >
        <q-tab name="details" label="Details"/>
        <q-tab name="samples" label="Samples"/>
        <q-tab name="pools" label="Pools"/>
        <q-tab name="runs" label="Runs"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="details">
            <Pool :instance="pool" v-if="pool.id"/>
            <SubmissionData v-if="pool.submission_data" :data="pool.submission_data"/>
            <!-- <PoolForm :model="pool" v-if="pool.id && modify" :on-success="onModifySuccess"/> -->
            <BaseFormDialog ref="pool_form" :form-component="PoolForm" title="Create Pool" v-model="pool" v-if="pool.id"/>
            <q-btn label="Modify" color="primary" @click="open('pool_form')" v-if="pool.id"/>
            <!-- <q-btn label="Cancel" @click="modify=false" v-if="modify"/>
            <q-btn label="Modify" @click="modify=true" v-if="!modify"/> -->
          </q-tab-panel>
          <q-tab-panel name="samples">
            <TableDialog :table-component="SamplesTable" :options="{'selection': 'multiple'}" ref="samples" @selected="addSamples"/>
            <q-btn label="Add samples" color="primary" @click="open('samples')" class="on-left" v-if="pool && !pool.locked"/>
            <q-btn label="Remove selected" color="negative" @click="removeSamples(selectedSamples)" v-if="pool && !pool.locked && selectedSamples.length"/>
            <SamplesTable :filters="`pools__id=${id}`" ref="samples_table" :options="{'selection': 'multiple'}" v-model:selection="selectedSamples"/>
          </q-tab-panel>
          <q-tab-panel name="pools">
            <TableDialog :table-component="PoolsTable" :options="{'selection': 'multiple', 'locked_only': true}" ref="pools" @selected="addPools"/>
            <q-btn label="Add pools" color="primary" @click="open('pools')" class="on-left" v-if="pool && !pool.locked"/>
            <q-btn label="Remove selected" color="negative" @click="removePools(selectedPools)" v-if="pool && !pool.locked && selectedPools.length" />
            <PoolsTable :filters="`pooled__id=${id}`" ref="pools_table" :options="{'selection': 'multiple'}" v-model:selection="selectedPools"/>
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
import Pool from '../components/details/Pool.vue'
import SamplesTable from '../components/tables/SamplesTable.vue'
import PoolsTable from '../components/tables/PoolsTable.vue'
import RunsTable from '../components/tables/RunsTable.vue'
import TableDialog from '../components/dialogs/TableDialog.vue'
import DeleteButton from '../components/DeleteButton.vue'
import PoolForm from 'src/components/forms/PoolForm.vue'
import BaseFormDialog from '../components/dialogs/BaseFormDialog.vue'
import SubmissionData from 'src/components/details/SubmissionData.vue'

// import PoolFormDialog from '../components/forms/PoolFormDialog.vue'
export default {
  name: 'PoolPage',
  props: ['id'],
  data () {
    return {
      pool: {},
      modify: false,
      tab: 'details',
      selectedSamples: [],
      selectedPools: [],
      SamplesTable,
      PoolsTable,
      PoolForm
    }
  },
  methods: {
    addSamples (samples) {
      samples = samples.map(l => l.id)
      const self = this
      this.$api
        .post(`/api/pools/${self.id}/add_samples/`, { samples })
        .then(function (response) {
          self.$q.notify('Samples added.')
          self.$refs.samples_table.$refs.table.refresh()
        })
        .catch(function (error) {
          console.log(error.response)
          self.$q.notify({ color: 'negative', message: 'Failed to add samples.' })
        })
    },
    removeSamples (samples) {
      // samples = this.$refs.samples_table.$refs.table.selected.map(l => l.id)
      samples = samples.map(s => s.id)
      console.log('removeSamples', samples)
      const self = this
      this.$api
        .post(`/api/pools/${self.id}/remove_samples/`, { samples })
        .then(function (response) {
          self.$q.notify('Samples removed.')
          self.$refs.samples_table.$refs.table.selected = []
          self.$refs.samples_table.$refs.table.refresh()
        })
        .catch(function (error) {
          console.log(error.code)
          self.$q.notify({ color: 'negative', message: 'Failed to remove samples.' })
        })
    },
    addPools (pools) {
      pools = pools.map(p => p.id)
      const self = this
      this.$api
        .post(`/api/pools/${self.id}/add_pools/`, { pools })
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
      pools = pools.map(p => p.id)
      const self = this
      this.$api
        .post(`/api/pools/${self.id}/remove_pools/`, { pools })
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
    onModifySuccess (request) {
      this.$q.notify('Pool updated.')
      this.modify = false
    },
    open (table) {
      console.log('table', this.$refs, this.$refs[table])
      this.$refs[table].open(this.pool)
    },
    lock () {
      this.$api
        .post(`/api/pools/${this.id}/lock/`)
        .then(response => {
          this.$q.notify('Pool locked.')
          this.pool.locked = response.data.locked
        })
        .catch(error => {
          console.log(error.code)
          this.$q.notify({ color: 'negative', message: 'Failed to lock pool. ' })
        })
    },
    unlock () {
      this.$api
        .post(`/api/pools/${this.id}/unlock/`)
        .then(response => {
          this.$q.notify('Pool unlocked.  It is now possible to add samples or pools to this pool.')
          this.pool.locked = response.data.locked
        })
        .catch(error => {
          console.log(error)
          this.$q.notify({ color: 'negative', message: 'Failed to unlock pool.  ' + (error.response.data ? error.response.data.detail : '') })
        })
    }
  },
  mounted: function () {
    const self = this
    this.$api
      .get(`/api/pools/${self.id}/`)
      .then(function (response) {
        self.pool = response.data
      })
  },
  components: {
    Pool,
    SamplesTable,
    PoolsTable,
    RunsTable,
    TableDialog,
    DeleteButton,
    BaseFormDialog,
    SubmissionData
    // PoolForm // PoolFormDialog
  }
}
</script>
