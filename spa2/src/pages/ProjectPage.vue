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
            <!-- {{project.sample_data.length}} -->
            <!-- <BaseDialog ref="dialog" title="Samples">
              <template v-slot:content>
                <SamplesTable :filters="`project__id=${id}`" :options="{'selection': 'multiple'}"/>
              </template>
            </BaseDialog> -->
            <!-- <TableDialog table-component="SamplesTable" ref="dialog"/> -->
            <!-- <TableDialog :table-component="SamplesTable" :options="{'selection': 'multiple'}" ref="dialog"/>
            <q-btn label="Samples" color="primary" @click="openDialog" /> -->
            <!-- <SamplesTable :filters="`project__id=${id}`" ref="samples"/> -->
            <!-- <JSONSchemaTable v-model="project.samples" :schema="sample_schema" v-if="project && project.samples && sample_schema" title="Samples" :modify="true"/> -->
            <!-- <aggridDialog v-model="project.samples" :schema="sample_schema" v-if="project && project.samples && sample_schema" :editable="true" :allow-examples="true" title="Samples"/> -->
            Default Sample Type: {{ default_sample_type }}
            Sample Types: {{ sample_types }}
            Sample Schema: {{ sample_schema }}
            <TypeSelect v-model="sample_grid_type" :emit_object="false" :model-filter="'sample'" :error_messages="{}" :has_error="{}"/>
              <q-tabs
                v-model="sample_sheet_tab"
              >
                <q-tab name="all" label="All types" v-if="sample_types.length > 1"/>
                <template v-for="s_type in sample_types" :key="s_type">
                  <q-tab :name="s_type" :label="s_type" v-if="s_type"/>
                </template>
              </q-tabs>
              <q-tab-panels v-model="sample_sheet_tab" animated>
                <q-tab-panel name="all" v-if="sample_types.length > 1">
                  <aggrid v-model="project.samples" :key="default_sample_type" :schema="getSampleTypeSchema(null)" v-if="project && project.samples" :editable="true" :allow-examples="true" title="Samples" :validate-url="`/server/api/projects/${id}/validate_samples/`" :save-url="`/server/api/projects/${id}/update_samples/`" :default-row="default_sample"/>
                </q-tab-panel>
                <template v-for="s_type in sample_types" :key="s_type">
                <q-tab-panel :name="s_type" v-if="s_type">
                  <q-tab-panel >
                      {{ s_type }}
                    <aggrid v-model="project.samples" :key="s_type" :schema="getSampleTypeSchema(s_type)" v-if="project && project.samples" :editable="true" :allow-examples="true" title="Samples" :validate-url="`/server/api/projects/${id}/validate_samples/`" :save-url="`/server/api/projects/${id}/update_samples/`" :default-row="default_sample"/>
                    </q-tab-panel>
                  </q-tab-panel>
                </template>
              </q-tab-panels>

            <!-- {{ sample_schema }} -->
            <!-- {{ project.samples }} -->
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
// import TableDialog from '../components/dialogs/TableDialog.vue'
import TypeSelect from '../components/TypeSelect.vue'
export default {
  name: 'ProjectPage',
  props: ['id'],
  data () {
    return {
      project: null,
      tab: 'details',
      openSampleDialog: false,
      SamplesTable,
      sample_grid_type: null,
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
    aggrid,
    TypeSelect
    // JSONSchemaTable,
    // aggridDialog
    // TableDialog
  },
  computed: {
    sample_schema () {
      // return ModelSchemas.getSchema('sample', this.default_sample_type)
      return ModelSchemas.getSchema('sample', this.sample_grid_type)
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
      return [...new Set(this.project.samples.map(s => s.type ? s.type.id : null))]
    }
  }
}
</script>
