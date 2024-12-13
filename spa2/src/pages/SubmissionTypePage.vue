<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h6 class="text-center"><router-link :to="{ name: 'submission_types'}">Submission Types</router-link> / {{type.name}}</h6>
    <q-tabs
        v-model="tab"
      >
        <q-tab name="details" label="Details"/>
        <q-tab name="submissions" label="Submissions"/>
        <q-tab name="importers" label="Importers"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="details">
            <q-markup-table flat bordered>
              <tbody>
                <tr>
                  <td class="text-left field">Name</td>
                  <td class="text-left">{{ type.name }}</td>
                </tr>
                <tr>
                  <td class="text-left field">Description</td>
                  <td class="text-left">{{ type.description }}</td>
                </tr>
              </tbody>
            </q-markup-table>
          </q-tab-panel>
          <q-tab-panel name="submissions">
            <SubmissionsTable :filters="`submission_type=${id}`"/>
          </q-tab-panel>
          <q-tab-panel name="importers">
            <ImporterTable :filters="`submission_type=${id}`"/>
            <fieldset>
              <legend>Create a new importer</legend>
              <ImporterForm v-model="foo" :on-success="importerCreated"/>
            </fieldset>
          </q-tab-panel>
        </q-tab-panels>
  </q-page>
</template>

<style>
</style>

<script>
import ImporterTable from 'src/components/tables/ImporterTable.vue'
import ImporterForm from 'src/components/forms/ImporterForm.vue'
import SubmissionsTable from '../components/tables/SubmissionsTable.vue'
export default {
  name: 'SubmissionTypePage',
  props: ['id'],
  data () {
    return {
      type: {},
      tab: 'details',
      ImporterForm,
      foo: { submission_type: this.id }
    }
  },
  mounted: function () {
    const self = this
    this.$api
      .get(`/api/submission_types/${self.id}/`)
      .then(function (response) {
        self.type = response.data
      })
  },
  methods: {
    openDialog () {
      this.$refs.importer_form.open()
    },
    importerCreated (request) {
      this.$q.notify('Importer created.')
      this.$router.push({ name: 'importer', params: { id: request.data.id } })
      this.$refs.importer_form.$refs.dialog.close()
    }
  },
  components: {
    ImporterTable,
    ImporterForm,
    SubmissionsTable
  }
}
</script>
