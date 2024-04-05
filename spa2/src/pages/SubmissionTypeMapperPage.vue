<template>
  <q-page class="q-pa-sm q-gutter-sm" v-if="mapper">
    <h6 class="text-center"><router-link :to="{ name: 'submission_type',  params: { id: mapper.submission_type.id } }">{{ mapper.submission_type.name }}</router-link> / Mappers / {{mapper.name}}</h6>
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
  components: {
    DataMapper
  }
}
</script>
