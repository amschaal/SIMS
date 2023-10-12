<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h4 class="text-center">Projects</h4>
    <div style="display: inline-block;  max-width:300px;">
      <q-input outlined v-model="submission_id" label="Submission ID">
         <template v-slot:append>
           <q-btn label="Import" color="primary" @click="importSubmission"/>
         </template>
      </q-input>
      </div>
      <!-- :error-message="errors.name"
      :error="has_error.name" -->

    <ProjectsTable/>
  </q-page>
</template>

<style>
</style>

<script>
import ProjectsTable from '../components/tables/ProjectsTable.vue'
export default {
  data () {
    return {
      submission_id: null,
      errors: {}
    }
  },
  methods: {
    importSubmission () {
      // this.$q.loading.show({
      //   message: `Importing submission ID: '${this.submission_id}'`
      // })
      const self = this
      this.$api.post('/api/projects/import_submission/', { id: this.submission_id })
        .then(function (response) {
          // self.$q.loading.hide()
          self.errors = {}
          self.$q.notify(`Successfully imported submission id "${self.submission_id}"`)
          self.$router.push({ name: 'project', params: { id: response.data.project.id } })
        })
        .catch(function (error) {
          // self.$q.loading.hide()
          if (error.response.data.message) {
            self.$q.notify({ color: 'negative', message: error.response.data.message })
          }
        })
    }
  },
  components: {
    ProjectsTable
  }
}
</script>
