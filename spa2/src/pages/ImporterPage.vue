<template>
  <q-page class="q-pa-sm q-gutter-sm" v-if="importer">
    <h6 class="text-center"><router-link :to="{ name: 'submission_type',  params: { id: importer.submission_type.id } }">{{ importer.submission_type.name }}</router-link> / Importers / {{importer.name}}</h6>
    <DeleteButton :url="`/api/importers/${id}/`"/>
    <q-tabs
        v-model="tab"
      >
        <q-tab name="details" label="Details"/>
        <q-tab name="imports" label="Imports"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="details">
            From: {{ importer.submission_type.name }}
            <!-- To: {{importer.model_type.name}} -->
    <!-- Variables: {{  schema_to_variables(submission_type.submission_schema) }} -->
            <DataMapper v-model="importer.config" :submission_type="importer.submission_type"/>
            <q-btn label="Update Mapping" @click="updateMapping"/>
            <!-- {{importer}} -->
            <!-- {{ importer.config }} -->
          </q-tab-panel>
          <q-tab-panel name="imports">
          </q-tab-panel>
        </q-tab-panels>
  </q-page>
</template>

<style>
</style>

<script>
import DataMapper from 'src/components/DataMapper.vue'
import DeleteButton from 'src/components/DeleteButton.vue'
export default {
  name: 'ImporterPage',
  props: ['id'],
  data () {
    return {
      importer: null,
      tab: 'details'
    }
  },
  mounted: function () {
    const self = this
    this.$api
      .get(`/api/importers/${self.id}/`)
      .then(function (response) {
        self.importer = response.data
      })
  },
  methods: {
    updateMapping () {
      this.$api
        .put(`/api/importers/${this.id}/`, this.importer)
        .then(response => {
          this.$q.notify({ message: 'Mapper updated.', type: 'positive' })
          // this.options = response.data.results
          // this.submission_type.mapping = this.mapping
        })
    }
  },
  components: {
    DataMapper,
    DeleteButton
  }
}
</script>
