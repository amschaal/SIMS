<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h4 class="text-center">Projects</h4>
    <ProjectsTable/>
  </q-page>
</template>

<style>
</style>

<script>
import ProjectsTable from '../components/tables/ProjectsTable.vue'
export default {
  data () {
    return {
    }
  },
  methods: {
  },
  components: {
    ProjectsTable
  }
}
</script>
