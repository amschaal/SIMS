<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h4 class="text-center">Projects</h4>
    <q-btn label="New Project" color="primary" @click="createProject"/>
    <FormDialog ref="form_dialog" title="Create Project" :on-success="projectCreated" api-method="post" :api-url="`/api/projects/`" v-if="project_schema">
      <template #form="props">
        <JSONModelTypeForm v-model="props.data" :schema="project_schema" :errors="props.errors" model-filter="project" :ui="ui">
        <!-- <JSONModelTypeForm v-model="props.data" :schema-url="`/api/projects/jsonschema/`" :errors="props.errors" model-filter="project" :ui="ui"> -->
          <!-- <template #field_id="{ v, data, form }">
          <div>
            <q-input type="textarea" v-model="data[v.variable]" label="OVERRIDDEN!!"/>
          </div>
        </template> -->
        </JSONModelTypeForm>
      </template>
    </FormDialog>
    <ProjectsTable/>
  </q-page>
</template>

<style>
</style>

<script>
import ProjectsTable from '../components/tables/ProjectsTable.vue'
import JSONModelTypeForm from 'src/components/forms/JSONModelTypeForm.vue'
import FormDialog from 'src/components/dialogs/FormDialog.vue'
import ModelSchemas from 'src/model_schemas/schemas'
export default {
  data () {
    return {
      project_schema: ModelSchemas.getSchema('project', null),
      ui: ModelSchemas.layouts.project
    }
  },
  methods: {
    projectCreated (response) {
      this.$q.notify('Project created.')
      this.$router.push({ name: 'project', params: { id: response.data.id } })
    },
    createProject () {
      this.$refs.form_dialog.open({})
    }
  },
  components: {
    ProjectsTable,
    JSONModelTypeForm,
    FormDialog
  }
}
</script>
