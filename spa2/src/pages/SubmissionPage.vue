<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h6 class="text-center"><router-link :to="{ name: 'submissions'}">Submissions</router-link> / {{submission.id}}</h6>
    <DeleteButton :url="`/api/submissions/${id}/`"/>
    <q-tabs
        v-model="tab"
      >
        <q-tab name="details" label="Details"/>
        <q-tab name="samples" label="Samples"/>
        <q-tab name="pools" label="Pools"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="details">
            <SubmissionImportDialog ref="import_dialog" :submission-type="submission.type.id" v-if="submission.type" :import="process"/>
            <q-btn v-if="!submission.project && submission.type" label="Import project/samples/pools" @click="openDialog" color="primary"/>
            <div class="text-h6">Submission</div>
            <Submission :instance="submission" v-if="submission.id"/>
          </q-tab-panel>
          <q-tab-panel name="samples" class="q-pa-sm q-gutter-sm">
            <SamplesTable :filters="`submission__id=${id}`" ref="samples"/>
          </q-tab-panel>
          <q-tab-panel name="pools" class="q-pa-sm q-gutter-sm">
            <PoolsTable :filters="`submission__id=${id}`" ref="pools"/>
          </q-tab-panel>
        </q-tab-panels>
  </q-page>
</template>

<style>
</style>

<script>
import Submission from '../components/details/Submission.vue'
import SamplesTable from '../components/tables/SamplesTable.vue'
import PoolsTable from 'src/components/tables/PoolsTable.vue'
import DeleteButton from '../components/DeleteButton.vue'
import SubmissionImportDialog from '../components/dialogs/SubmissionImportDialog.vue'
// import TableDialog from '../components/dialogs/TableDialog.vue'
export default {
  name: 'SubmissionPage',
  props: ['id'],
  data () {
    return {
      submission: {},
      tab: 'details',
      openSampleDialog: false,
      SamplesTable
    }
  },
  mounted: function () {
    const self = this
    this.$api
      .get(`/api/submissions/${self.id}/`)
      .then(function (response) {
        console.log('response', response)
        // Vue.set(self, 'submission', response.data) #Vue2
        self.submission = response.data
      })
  },
  methods: {
    openDialog () {
      console.log('dialog', this.$refs.dialog)
      this.$refs.import_dialog.open()
    },
    process (importer) {
      const self = this
      this.$api
        // .post(`/api/submissions/${this.id}/update_samples/`)
        .post(`/api/submissions/${this.id}/process/`, { importer })
        .then(function (response) {
          console.log('response', response, self.$refs.samples)
          self.$q.notify(`Successfully imported submission id "${self.id}"`)
          let message = `Samples updated.  ${response.data.new_samples.length} new samples imported.`
          if (response.data.new_samples.length > 0) {
            message += '  New sample ids: ' + response.data.new_samples.map(s => s.id).join(', ')
          }
          self.$q.notify(message)
          self.$router.push({ name: 'project', params: { id: response.data.project.id } })
          // self.$refs.samples.$refs.table.refresh()
        })
        .catch(function (error) {
          // console.log('error', error)
          self.$q.notify({ color: 'negative', message: 'Failed to import data. Detail: ' + error.response.data.detail })
        })
    }
  },
  components: {
    SamplesTable,
    PoolsTable,
    DeleteButton,
    Submission,
    SubmissionImportDialog
    // TableDialog
  }
}
</script>
