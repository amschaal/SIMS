<template>
  <q-page class="q-pa-md q-gutter-md">
    <h4 class="text-center">Projects</h4>
    <ProjectsTable/>
  </q-page>
</template>

<style>
</style>

<script>
import ProjectsTable from '../components/tables/ProjectsTable.vue'
export default {
  components: {
    ProjectsTable
  }
}
</script>
