<template>
  <q-page class="q-pa-sm q-gutter-sm" v-if="mapper">
    <h6 class="text-center"><router-link :to="{ name: 'submission_type',  params: { id: mapper.submission_type.id } }">{{ mapper.submission_type.name }}</router-link> / Mappers / {{mapper.name}}</h6>
    <DeleteButton :url="`/api/submission_type_mappers/${id}/`"/>
    <q-tabs
        v-model="tab"
      >
        <q-tab name="details" label="Details"/>
        <q-tab name="imports" label="Imports"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="details">
            From: {{ mapper.submission_type.name }}
            To: {{mapper.model_type.name}}
    <!-- Variables: {{  schema_to_variables(submission_type.submission_schema) }} -->
            <DataMapper v-model="mapper.mapping" :submission_type="mapper.submission_type" :type="mapper.model_type"/>
            <q-btn label="Update Mapping" @click="updateMapping"/>
            <!-- {{mapper}} -->
            {{ mapper.mapping }}
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
  name: 'SubmissionTypeMapperPage',
  props: ['id'],
  data () {
    return {
      mapper: null,
      tab: 'details'
    }
  },
  mounted: function () {
    const self = this
    this.$api
      .get(`/api/submission_type_mappers/${self.id}/`)
      .then(function (response) {
        self.mapper = response.data
      })
  },
  methods: {
    updateMapping () {
      this.$api
        .put(`/api/submission_type_mappers/${this.id}/`, this.mapper)
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
