<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h6 class="text-center"><router-link :to="{ name: 'libraries'}">Libraries</router-link> / {{library.id}}</h6>
    <DeleteButton :url="`/api/libraries/${id}/`"/>
    <q-tabs
        v-model="tab"
      >
        <q-tab name="details" label="Details"/>
        <q-tab name="pools" label="Pools"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="details">
            <Library :library="library"/>
          </q-tab-panel>
          <q-tab-panel name="pools">
            <PoolsTable :filters="`libraries__id=${id}`"/>
          </q-tab-panel>
        </q-tab-panels>
  </q-page>
</template>

<style>
</style>

<script>
import Vue from 'vue'
import Library from '../components/details/Library.vue'
import PoolsTable from '../components/tables/PoolsTable.vue'
import DeleteButton from '../components/DeleteButton.vue'
export default {
  name: 'library',
  props: ['id'],
  data () {
    return {
      library: {},
      tab: 'details'
    }
  },
  mounted: function () {
    var self = this
    this.$axios
      .get(`/api/libraries/${self.id}/`)
      .then(function (response) {
        Vue.set(self, 'library', response.data)
      })
  },
  components: {
    Library,
    PoolsTable,
    DeleteButton
  }
}
</script>
