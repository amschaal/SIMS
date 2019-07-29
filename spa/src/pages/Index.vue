<template>
  <q-page class="flex flex-center">
    <TableDialog :table-component="SamplesTable" :options="{'selection': 'multiple'}" ref="samples"/>
    <q-btn label="Samples" color="primary" @click="open('samples')" />
    <TableDialog :table-component="ProjectsTable" :options="{'selection': 'multiple'}" ref="projects"/>
    <q-btn label="Projects" color="primary" @click="open('projects')" />
  </q-page>
</template>

<style>
</style>

<script>
import SamplesTable from '../components/tables/SamplesTable.vue'
import ProjectsTable from '../components/tables/ProjectsTable.vue'
import TableDialog from '../components/dialogs/TableDialog.vue'
export default {
  data () {
    return {
      SamplesTable: SamplesTable,
      ProjectsTable: ProjectsTable
    }
  },
  methods: {
    open (table) {
      this.$refs[table].open()
    }
  },
  name: 'PageIndex',
  components: { TableDialog }
}
</script>
