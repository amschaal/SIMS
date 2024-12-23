<template>
  <q-page class="q-pa-sm q-gutter-sm" v-if="project">
    <h6 class="text-center"><router-link :to="{ name: 'projects'}">Projects</router-link> / {{project.id}}</h6>
    <q-btn v-if="project.submission && project.submission.id" color="negative" label="Unimport" @click="unimport"/>
    <DeleteButton v-else :url="`/api/projects/${id}/`"/>
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
            <div class="text-h6">Project</div>
            <Project :instance="project" v-if="project"/>
            <SubmissionData :data="project.submission.data" :schema="project.submission.schema" v-if="project && project.submission"/>
            <FormDialog ref="form_dialog" title="Modify Project" api-method="put" :api-url="`/api/projects/${this.id}/`" v-model="project" v-if="project">
              <template #form="props">
                <JSONModelTypeForm v-model="props.data" :schema="schema" :errors="props.errors" :ui="ui" model-filter="project" :hide="['id']">
                  <!-- <template #field_id="{ v, data, form }">
                  <div>
                    <q-input type="textarea" v-model="data[v.variable]" label="OVERRIDDEN!!"/>
                  </div>
                </template> -->
                </JSONModelTypeForm>
              </template>
            </FormDialog>
            <q-btn label="Modify" color="primary" @click="modify" v-if="project"/>
            <!-- <q-list bordered class="rounded-borders">
            <q-expansion-item
              expand-separator
              icon="list"
              label="Details"
              caption="Full import details"
            >
              <q-card>
                <q-card-section>
                  <h4 v-if="project.submission">Imported {{$filters.formatDate(project.submission.processed)}}</h4>
                  <CustomFields v-model="project.data" :schema="project.schema" ref="submission_fields" v-if="project.submission_schema" :modify="false" :warnings="{}"/>
                </q-card-section>
              </q-card>
            </q-expansion-item>
            </q-list> -->
            <!-- <CustomFields v-model="submission.submission_data" :schema="submission_schema" ref="submission_fields" :warnings="submission.warnings ? submission.warnings.submission_data : {}" v-if="submission_schema" :modify="false"/> -->
          </q-tab-panel>
          <q-tab-panel name="samples" class="q-pa-sm q-gutter-sm">
            <!-- <p>Default Sample Type: {{ default_sample_type }}</p>
            <p>Sample Types: {{ sample_type_ids }}</p>
            <p>Sample Schema ({{ sample_grid_type }}): {{ sample_schema }}</p> -->
            <q-banner inline-actions rounded dense class="text-white bg-orange" v-if="sample_types.length > 1">
              This project contains samples of multiple types, which may have different fields.  Please select a sample type to determine which fields to display.
              <q-select v-model="select_sample_type" :options="sample_types" option-label="name" option-value="id" emit-value map-options filled bg-color="white" dense label="Select which sample type columns to display"/>
            </q-banner>
            <aggrid v-model="project.samples" :key="sample_grid_type" :schema="sample_schema" v-if="project && project.samples && sample_schema" :editable="true" :allow-examples="true" :title="`Samples (displaying columns for type '${sample_grid_type}')`" :validate-url="`/server/api/projects/${id}/validate_samples/`" :save-url="`/server/api/projects/${id}/update_samples/`" :default-row="default_sample" :options="{isCellEditable: isCellEditable}"/>
          </q-tab-panel>
          <q-tab-panel name="pools">
            <PoolsTable :filters="`project__id=${id}`"/>
          </q-tab-panel>
          <q-tab-panel name="runs">
            <RunsTable :filters="`run_pools__pool__samples__sample__project__id=${id}`"/>
          </q-tab-panel>

        </q-tab-panels>
  </q-page>
</template>

<style>
</style>

<script>
import Project from '../components/details/Project.vue'
import SamplesTable from '../components/tables/SamplesTable.vue'
import PoolsTable from '../components/tables/PoolsTable.vue'
import RunsTable from '../components/tables/RunsTable.vue'
import DeleteButton from '../components/DeleteButton.vue'
// import CustomFields from 'assets/jsonschema/forms/customFields.vue'
import SubmissionData from 'src/components/details/SubmissionData.vue'
import JSONModelTypeForm from 'src/components/forms/JSONModelTypeForm.vue'
import FormDialog from 'src/components/dialogs/FormDialog.vue'
// import JSONSchemaTable from 'src/components/tables/jsonschema/JSONSchemaTable.vue'
// import aggridDialog from 'src/assets/jsonschema/components/aggrid/aggridDialog.vue'
import ModelSchemas from 'src/model_schemas/schemas'
import aggrid from 'src/assets/jsonschema/components/aggrid/aggrid.vue'
import _ from 'lodash'
// import TableDialog from '../components/dialogs/TableDialog.vue'
export default {
  name: 'ProjectPage',
  props: ['id'],
  data () {
    return {
      project: null,
      tab: 'details',
      openSampleDialog: false,
      SamplesTable,
      select_sample_type: null,
      ui: ModelSchemas.layouts.project,
      sample_sheet_tab: 'default'
    }
  },
  mounted: function () {
    this.$api
      .get(`/api/projects/${this.id}/`)
      .then((response) => {
        console.log('response', response)
        // Vue.set(self, 'project', response.data) #Vue2
        this.project = response.data
        this.sample_grid_type = this.default_sample_type
      })
  },
  methods: {
    openDialog () {
      console.log('dialog', this.$refs.dialog)
      this.$refs.dialog.open()
    },
    modify () {
      this.$refs.form_dialog.open(this.project)
    },
    unimport () {
      const submissionId = this.project.submission.id
      this.$api
        .post(`/api/submissions/${submissionId}/unimport/`)
        .then(response => {
          this.$q.notify('Submission unimported.')
          this.$router.push({ name: 'submission', params: { id: submissionId } })
        })
        .catch(error => {
          console.log('error', error)
          this.$q.notify({ color: 'negative', message: 'Failed to unimport data' })
        })
    },
    getSampleTypeSchema (type) {
      return ModelSchemas.getSchema('sample', type)
    },
    isCellEditable (node) {
      const row = node.data
      const rowTypeId = row.type && row.type.id ? row.type.id : row.type
      // console.log('isCellEditable', this.sample_grid_type, rowTypeId)
      if (this.sample_grid_type && (this.sample_grid_type !== rowTypeId)) {
        // this.$q.notify(`This sample is not of type "${this.sample_grid_type}".  Please select the "${rowTypeId}"" type in the above ÷drop down to be able to edit samples of this type.`)
        return false
      }
      return true
    }
    // updateSamples () {
    //   const self = this
    //   this.$api
    //     // .post(`/api/projects/${this.id}/update_samples/`)
    //     .post(`/api/projects/${this.id}/process_samples/`)
    //     .then(function (response) {
    //       console.log('response', response, self.$refs.samples)
    //       let message = `Samples updated.  ${response.data.new_samples.length} new samples imported.`
    //       if (response.data.new_samples.length > 0) {
    //         message += '  New sample ids: ' + response.data.new_samples.map(s => s.id).join(', ')
    //       }
    //       self.$q.notify(message)
    //       self.$refs.samples.$refs.table.refresh()
    //     })
    //     .catch(function (error) {
    //       // console.log('error', error)
    //       self.$q.notify({ color: 'negative', message: 'Failed to import data. Detail: ' + error.response.data.detail })
    //     })
    // }
  },
  components: {
    // SamplesTable,
    RunsTable,
    PoolsTable,
    DeleteButton,
    Project,
    // CustomFields,
    SubmissionData,
    JSONModelTypeForm,
    FormDialog,
    aggrid
    // JSONSchemaTable,
    // aggridDialog
    // TableDialog
  },
  computed: {
    sample_schema () {
      // return ModelSchemas.getSchema('sample', this.default_sample_type)
      return ModelSchemas.getSchema('sample', this.sample_grid_type)
    },
    sample_grid_type () {
      if (this.sample_type_ids.length === 1) {
        return this.sample_type_ids[0]
      } else {
        return this.select_sample_type
      }
    },
    default_sample_type () {
      return this.project && this.project.metadata && this.project.metadata.types ? this.project.metadata.types.sample : null
    },
    default_sample () {
      return { data: {}, project: this.id, type: this.default_sample_type }
    },
    schema () {
      return ModelSchemas.getSchema('project', this.project.type)
    },
    sample_types () {
      if (!this.project || !this.project.samples) {
        return []
      }
      // return ['library']
      const types = this.project.samples.map(s => s.type ? s.type : { id: null, name: 'Untyped' })
      return _.uniqWith(types, (a1, a2) => a1.id === a2.id)
      // return [...new Set(this.project.samples.map(s => s.type ? s.type.id : null))]
    },
    sample_type_ids () {
      return this.sample_types.map(t => t.id)
    }
  }
}
</script>
