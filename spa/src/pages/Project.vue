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
            <BaseDialog ref="dialog" title="Samples">
              <template v-slot:content>
                <SamplesTable :filters="`project__id=${id}`" :options="{'selection': 'multiple'}"/>
              </template>
            </BaseDialog>
            <q-btn label="Samples" color="primary" @click="openDialog" />
            <SamplesTable :filters="`project__id=${id}`"/>
          </q-tab-panel>
        </q-tab-panels>
  </q-page>
</template>

<style>
</style>

<script>
import Vue from 'vue'
import SamplesTable from '../components/SamplesTable.vue'
import BaseDialog from '../components/dialogs/BaseDialog.vue'
export default {
  name: 'project',
  props: ['id'],
  data () {
    return {
      project: {},
      tab: 'details',
      openSampleDialog: false
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
  },
  methods: {
    openDialog () {
      console.log('dialog', this.$refs.dialog)
      this.$refs.dialog.open()
    }
  },
  components: {
    SamplesTable,
    BaseDialog
  }
}
</script>
