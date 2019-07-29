<template>
  <q-page class="flex flex-center">
    <TableDialog :table-component="LibrariesTable" :options="{'selection': 'multiple'}" ref="libraries" :on-select="onSelect"/>
    <q-btn label="Libraries" color="primary" @click="open('libraries')" />
    <TableDialog :table-component="SamplesTable" :options="{'selection': 'multiple'}" ref="samples" :on-select="onSelect"/>
    <q-btn label="Samples" color="primary" @click="open('samples')" />
    <TableDialog :table-component="ProjectsTable" :options="{'selection': 'multiple'}" ref="projects" :on-select="onSelect"/>
    <q-btn label="Projects" color="primary" @click="open('projects')" />
  </q-page>
</template>

<style>
</style>

<script>
import LibrariesTable from '../components/tables/LibrariesTable.vue'
import SamplesTable from '../components/tables/SamplesTable.vue'
import ProjectsTable from '../components/tables/ProjectsTable.vue'
import TableDialog from '../components/dialogs/TableDialog.vue'
export default {
  data () {
    return {
      SamplesTable: SamplesTable,
      ProjectsTable: ProjectsTable,
      LibrariesTable: LibrariesTable
    }
  },
  methods: {
    open (table) {
      this.$refs[table].open()
    },
    onSelect (selected) {
      console.log('onSelect', selected)
    }
  },
  name: 'PageIndex',
  components: { TableDialog }
}
</script>
