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
            Mappings
          </q-tab-panel>
        </q-tab-panels>
  </q-page>
</template>

<style>
</style>

<script>
export default {
  name: 'SubmissionTypePage',
  props: ['id'],
  data () {
    return {
      type: {},
      tab: 'details'
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
  components: {
  }
}
</script>
