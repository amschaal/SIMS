<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h6 class="text-center"><router-link :to="{ name: 'samples'}">Samples</router-link> / {{sample.id}}</h6>
    <DeleteButton :url="`/api/samples/${id}/`"/>
    <q-tabs
        v-model="tab"
      >
        <q-tab name="details" label="Details"/>
        <q-tab name="samples" label="Derivatives"/>
        <q-tab name="pools" label="Pools"/>
        <q-tab name="runs" label="Runs"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="details">
            <Sample :instance="sample" v-if="sample.id"/>
            <SubmissionData v-if="sample.submission_data" :data="sample.submission_data"/>
            <FormDialog ref="form_dialog" title="Modify Sample" api-method="put" :api-url="`/api/samples/${this.id}/`" v-model="sample">
              <template #form="props">
                <JSONModelTypeForm v-model="props.data" :schema-url="`/api/samples/${this.id}/jsonschema/`" :errors="props.errors" v-if="sample">
                  <!-- <template #field_id="{ v, data, form }">
                  <div>
                    <q-input type="textarea" v-model="data[v.variable]" label="OVERRIDDEN!!"/>
                  </div>
                </template> -->
                </JSONModelTypeForm>
              </template>
            </FormDialog>
            <q-btn label="Modify" color="primary" @click="modify"/>
            jsonschema: {{ jsonschema }}
          </q-tab-panel>
          <q-tab-panel name="samples">
            <SamplesTable :filters="`samples__id=${id}`"/>
          </q-tab-panel>
          <q-tab-panel name="pools">
            <PoolsTable :filters="`samples__id=${id}`"/>
          </q-tab-panel>
          <q-tab-panel name="runs">
            <RunsTable :filters="`run_pools__pool__samples__id=${id}`"/>
          </q-tab-panel>
        </q-tab-panels>
  </q-page>
</template>

<style>
</style>

<script>
import Sample from '../components/details/Sample.vue'
import SamplesTable from '../components/tables/SamplesTable.vue'
import PoolsTable from '../components/tables/PoolsTable.vue'
import DeleteButton from '../components/DeleteButton.vue'
import RunsTable from 'src/components/tables/RunsTable.vue'
import SubmissionData from 'src/components/details/SubmissionData.vue'
import JSONModelTypeForm from 'src/components/forms/JSONModelTypeForm.vue'
import FormDialog from 'src/components/dialogs/FormDialog.vue'

export default {
  name: 'SamplePage',
  props: ['id'],
  data () {
    return {
      sample: {},
      jsonschema: null,
      tab: 'details'
    }
  },
  mounted: function () {
    this.$api
      .get(`/api/samples/${this.id}/`)
      .then(response => {
        console.log('response', response)
        this.sample = response.data
      })
    // this.$api
    //   .get(`/api/samples/${this.id}/jsonschema`)
    //   .then(response => {
    //     this.jsonschema = response.data
    //   })
  },
  methods: {
    modify () {
      this.$refs.form_dialog.open(this.sample)
    }
  },
  components: {
    SamplesTable,
    PoolsTable,
    DeleteButton,
    Sample,
    RunsTable,
    SubmissionData,
    JSONModelTypeForm,
    FormDialog
  }
}
</script>
