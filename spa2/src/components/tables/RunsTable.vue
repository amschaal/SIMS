<template>
  <BaseTable
    :columns="columns"
    :visible-columns="visibleColumns"
    api-url="/api/runs/"
    :options="combined_options"
    :filters="filters"
    ref="table"
  >
    <template v-slot:body="{ props }">
      <q-tr :props="props">
        <q-td auto-width v-if="combined_options.selection === 'multiple' || combined_options.selection === 'single'">
          <q-checkbox dense v-model="props.selected" />
        </q-td>
        <q-td key="created" :props="props">{{ props.row.created }}</q-td>
        <q-td key="type" :props="props">{{ props.row.type }}</q-td>
        <q-td key="machine__name" :props="props">{{ props.row.machine_name }}</q-td>
        <q-td key="name" :props="props"><router-link :to="{ name: 'run', params: { id: props.row.id }}">{{ props.row.name }}</router-link></q-td>
        <q-td key="description" :props="props">{{ props.row.description }}</q-td>
      </q-tr>
    </template>
  </BaseTable>
</template>

<script>
import BaseTable from './BaseTable.vue'
import _ from 'lodash'
export default {
  name: 'RunsTable',
  props: ['filters', 'options'],
  data () {
    const options = {
      title: 'Runs',
      pagination: {
        sortBy: 'created',
        descending: true,
        page: 1,
        rowsPerPage: 10,
        rowsNumber: 10
      }
    }
    return {
      columns: [
        { name: 'created', label: 'Created', field: 'created', sortable: true },
        { name: 'type', label: 'Type', field: 'type', sortable: true },
        { name: 'machine__name', label: 'Machine', field: 'machine__name', sortable: true },
        { name: 'name', label: 'Name', field: 'name', sortable: true },
        { name: 'description', label: 'Description', field: 'description', sortable: false }
      ],
      // visibleColumns: ['id', 'project'],
      combined_options: _.merge(options, this.options)
      // options: { 'title': 'Samples' }
    }
  },
  mounted: function () {
  },
  components: {
    BaseTable
  }
}
</script>
