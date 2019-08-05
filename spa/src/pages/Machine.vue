<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h6 class="text-center"><router-link :to="{ name: 'machines'}">Machines</router-link> / {{machine.name}}</h6>
    <DeleteButton :url="`/api/machines/${id}/`"/>
    <q-tabs
        v-model="tab"
      >
        <q-tab name="details" label="Details"/>
        <q-tab name="runs" label="Runs"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="details">
            {{machine.name}}
          </q-tab-panel>
          <q-tab-panel name="runs">
            <RunsTable :filters="`machine__id=${id}`"/>
          </q-tab-panel>
        </q-tab-panels>
  </q-page>
</template>

<style>
</style>

<script>
import Vue from 'vue'
import RunsTable from '../components/tables/RunsTable.vue'
import DeleteButton from '../components/DeleteButton.vue'
export default {
  name: 'machine',
  props: ['id'],
  data () {
    return {
      machine: {},
      tab: 'details'
    }
  },
  mounted: function () {
    var self = this
    this.$axios
      .get(`/api/machines/${self.id}/`)
      .then(function (response) {
        Vue.set(self, 'machine', response.data)
      })
  },
  components: {
    RunsTable,
    DeleteButton
  }
}
</script>
