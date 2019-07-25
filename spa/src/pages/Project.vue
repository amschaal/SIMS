<template>
  <q-page class="flex flex-center">

    <q-tabs
        v-model="tab"
      >
        <q-tab name="details" label="Details"/>
        <q-tab name="samples" label="Samples"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="details">
            <div class="text-h6">Project</div>
            Project {{project}}
          </q-tab-panel>
          <q-tab-panel name="samples">
            <div class="text-h6">Samples</div>
            {{project.sample_data}}
          </q-tab-panel>
        </q-tab-panels>
  </q-page>
</template>

<style>
</style>

<script>
import Vue from 'vue'
export default {
  name: 'project',
  props: ['id'],
  data () {
    return {
      project: {},
      tab: 'details'
    }
  },
  mounted: function () {
    var self = this
    this.$axios
      .get(`/api/projects/${self.id}/`)
      .then(function (response) {
        console.log('response', response)
        Vue.set(self, 'project', response.data)
      })
  }
}
</script>
