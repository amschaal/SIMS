<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h6 class="text-center"><router-link :to="{ name: 'samples'}">Samples</router-link> / {{sample.id}}</h6>
    <DeleteButton :url="`/api/samples/${id}/`"/>
    <q-tabs
        v-model="tab"
      >
        <q-tab name="details" label="Details"/>
        <q-tab name="samples" label="Derivatives"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="details">
            <Sample :instance="sample" v-if="sample.id"/>
          </q-tab-panel>
          <q-tab-panel name="samples">
            <SamplesTable :filters="`samples__id=${id}`"/>
          </q-tab-panel>
        </q-tab-panels>
  </q-page>
</template>

<style>
</style>

<script>
import Sample from '../components/details/Sample.vue'
import SamplesTable from '../components/tables/SamplesTable.vue'
import DeleteButton from '../components/DeleteButton.vue'
export default {
  name: 'SamplePage',
  props: ['id'],
  data () {
    return {
      sample: {},
      tab: 'details'
    }
  },
  mounted: function () {
    const self = this
    this.$api
      .get(`/api/samples/${self.id}/`)
      .then(function (response) {
        console.log('response', response)
        self.sample = response.data
      })
  },
  components: {
    SamplesTable,
    DeleteButton,
    Sample
  }
}
</script>
