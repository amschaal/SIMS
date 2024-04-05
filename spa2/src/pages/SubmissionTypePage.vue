<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h6 class="text-center"><router-link :to="{ name: 'submission_types'}">Submission Types</router-link> / {{type.name}}</h6>
    <q-tabs
        v-model="tab"
      >
        <q-tab name="details" label="Details"/>
        <q-tab name="mappings" label="Mappings"/>
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
          <q-tab-panel name="mappings">
            <SubmissionTypeMapperTable :filters="`submission_type=${id}`"/>
            <fieldset>
              <legend>Create a new mapper</legend>
              <SubmissionTypeMapperForm v-model="foo" :on-success="mapperCreated"/>
            </fieldset>
          </q-tab-panel>
        </q-tab-panels>
  </q-page>
</template>

<style>
</style>

<script>
import SubmissionTypeMapperTable from 'src/components/tables/SubmissionTypeMapperTable.vue'
import SubmissionTypeMapperForm from 'src/components/forms/SubmissionTypeMapperForm.vue'
export default {
  name: 'SubmissionTypePage',
  props: ['id'],
  data () {
    return {
      type: {},
      tab: 'details',
      SubmissionTypeMapperForm,
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
      this.$refs.mapper_form.open()
    },
    mapperCreated (request) {
      this.$q.notify('Mapper created.')
      this.$router.push({ name: 'submission_type_mapper', params: { id: request.data.id } })
      this.$refs.mapper_form.$refs.dialog.close()
    }
  },
  components: {
    SubmissionTypeMapperTable,
    SubmissionTypeMapperForm
  }
}
</script>
