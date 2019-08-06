<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h6 class="text-center"><router-link :to="{ name: 'samples'}">Samples</router-link> / {{sample.id}}</h6>
    <DeleteButton :url="`/api/samples/${id}/`"/>
    <q-tabs
        v-model="tab"
      >
        <q-tab name="details" label="Details"/>
        <q-tab name="libraries" label="Libraries"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="details">
            <Sample :sample="sample"/>
          </q-tab-panel>
          <q-tab-panel name="libraries">
            <LibrariesTable :filters="`sample__id=${id}`"/>
          </q-tab-panel>
        </q-tab-panels>
  </q-page>
</template>

<style>
</style>

<script>
import Vue from 'vue'
import Sample from '../components/details/Sample.vue'
import LibrariesTable from '../components/tables/LibrariesTable.vue'
import DeleteButton from '../components/DeleteButton.vue'
export default {
  name: 'sample',
  props: ['id'],
  data () {
    return {
      sample: {},
      tab: 'details'
    }
  },
  mounted: function () {
    var self = this
    this.$axios
      .get(`/api/samples/${self.id}/`)
      .then(function (response) {
        console.log('response', response)
        Vue.set(self, 'sample', response.data)
      })
  },
  components: {
    LibrariesTable,
    DeleteButton,
    Sample
  }
}
</script>
