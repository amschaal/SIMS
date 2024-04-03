<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h4 class="text-center">Submission Types</h4>
    <SubmissionTypesTable/>
  </q-page>
</template>

<style>
</style>

<script>
import SubmissionTypesTable from '../components/tables/SubmissionTypesTable.vue'
export default {
  data () {
    return {
    }
  },
  methods: {
  },
  components: {
    SubmissionTypesTable
  }
}
</script>
