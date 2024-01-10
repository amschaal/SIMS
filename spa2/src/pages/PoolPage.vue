<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h6 class="text-center"><router-link :to="{ name: 'pools'}">Pools</router-link> / {{pool.name}}</h6>
    <DeleteButton :url="`/api/pools/${id}/`" :redirect="{name: 'pools'}"/>
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
            <!-- <PoolForm :model="pool" v-if="pool.id && modify" :on-success="onModifySuccess"/> -->
            <BaseFormDialog ref="pool_form" :form-component="PoolForm" title="Create Pool" v-model="pool" v-if="pool.id"/>
            <q-btn label="Modify" color="primary" @click="open('pool_form')" v-if="pool.id"/>
            <!-- <q-btn label="Cancel" @click="modify=false" v-if="modify"/>
            <q-btn label="Modify" @click="modify=true" v-if="!modify"/> -->
          </q-tab-panel>
          <q-tab-panel name="samples">
            <TableDialog :table-component="SamplesTable" :options="{'selection': 'multiple'}" ref="samples" :on-select="addSamples"/>
            <q-btn label="Add samples" color="primary" @click="open('samples')" class="on-left"/>
            <q-btn label="Remove selected" color="negative" @click="removeSamples" />
            <SamplesTable :filters="`pools__id=${id}`" ref="samples_table" :options="{'selection': 'multiple'}"/>
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
import Pool from '../components/details/Pool.vue'
import SamplesTable from '../components/tables/SamplesTable.vue'
import PoolsTable from '../components/tables/PoolsTable.vue'
import RunsTable from '../components/tables/RunsTable.vue'
import TableDialog from '../components/dialogs/TableDialog.vue'
import DeleteButton from '../components/DeleteButton.vue'
import PoolForm from 'src/components/forms/PoolForm.vue'
import BaseFormDialog from '../components/dialogs/BaseFormDialog.vue'
// import PoolFormDialog from '../components/forms/PoolFormDialog.vue'
export default {
  name: 'PoolPage',
  props: ['id'],
  data () {
    return {
      pool: {},
      modify: false,
      tab: 'details',
      SamplesTable,
      PoolsTable,
      PoolForm
    }
  },
  methods: {
    addSamples (samples) {
      samples = samples.map(l => l.id)
      console.log('addSamples', samples)
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
      samples = this.$refs.samples_table.$refs.table.selected.map(l => l.id)
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
      pools = this.$refs.pools_table.$refs.table.selected.map(l => l.id)
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
    BaseFormDialog
    // PoolForm // PoolFormDialog
  }
}
</script>
