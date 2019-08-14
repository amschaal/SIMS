<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h6 class="text-center"><router-link :to="{ name: 'projects'}">Projects</router-link> / {{project.id}}</h6>
    <DeleteButton :url="`/api/projects/${id}/`"/>
    <q-tabs
        v-model="tab"
      >
        <q-tab name="details" label="Details"/>
        <q-tab name="samples" label="Samples"/>
        <q-tab name="runs" label="Runs"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="details">
            <div class="text-h6">Project</div>
            <Project :project="project"/>
          </q-tab-panel>
          <q-tab-panel name="samples" class="q-pa-sm q-gutter-sm">
            <!-- {{project.sample_data.length}} -->
            <!-- <BaseDialog ref="dialog" title="Samples">
              <template v-slot:content>
                <SamplesTable :filters="`project__id=${id}`" :options="{'selection': 'multiple'}"/>
              </template>
            </BaseDialog> -->
            <!-- <TableDialog table-component="SamplesTable" ref="dialog"/> -->
            <!-- <TableDialog :table-component="SamplesTable" :options="{'selection': 'multiple'}" ref="dialog"/>
            <q-btn label="Samples" color="primary" @click="openDialog" /> -->
            <q-btn label="Import Samples" @click="updateSamples"/>
            <SamplesTable :filters="`project__id=${id}`" ref="samples"/>
          </q-tab-panel>
          <q-tab-panel name="runs">
            <RunsTable :filters="`run_pools__pool__libraries__sample__project__id=${id}`"/>
          </q-tab-panel>

        </q-tab-panels>
  </q-page>
</template>

<style>
</style>

<script>
import Vue from 'vue'
import Project from '../components/details/Project.vue'
import SamplesTable from '../components/tables/SamplesTable.vue'
import RunsTable from '../components/tables/RunsTable.vue'
import DeleteButton from '../components/DeleteButton.vue'
// import TableDialog from '../components/dialogs/TableDialog.vue'
export default {
  name: 'project',
  props: ['id'],
  data () {
    return {
      project: {},
      tab: 'details',
      openSampleDialog: false,
      SamplesTable: SamplesTable
    }
  },
  mounted: function () {
    var self = this
    this.$axios
      .get(`/api/projects/${self.id}/`)
      .then(function (response) {
        console.log('response', response)
        Vue.set(self, 'project', response.data)
      })
  },
  methods: {
    openDialog () {
      console.log('dialog', this.$refs.dialog)
      this.$refs.dialog.open()
    },
    updateSamples () {
      var self = this
      this.$axios
        .post(`/api/projects/${this.id}/update_samples/`)
        .then(function (response) {
          console.log('response', response, self.$refs.samples)
          var message = `Samples updated.  ${response.data.new_samples.length} new samples imported.`
          if (response.data.new_samples.length > 0) {
            message += '  New sample ids: ' + response.data.new_samples.map(s => s.id).join(', ')
          }
          self.$q.notify(message)
          self.$refs.samples.$refs.table.refresh()
        })
    }
  },
  components: {
    SamplesTable,
    RunsTable,
    DeleteButton,
    Project
    // TableDialog
  }
}
</script>
