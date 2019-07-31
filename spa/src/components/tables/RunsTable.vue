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
        <q-td auto-width v-if="combined_options.selection === 'multiple'">
          <q-checkbox dense v-model="props.selected" />
        </q-td>
        <q-td key="created" :props="props">{{ props.row.created }}</q-td>
        <q-td key="machine__name" :props="props">{{ props.row.machine_name }}</q-td>
        <q-td key="id" :props="props"><router-link replace :to="{ name: 'run', params: { id: props.row.id }}">{{ props.row.name }}</router-link></q-td>
        <q-td key="description" :props="props">{{ props.row.description }}</q-td>
      </q-tr>
    </template>
  </BaseTable>
</template>

<script>
import BaseTable from './BaseTable.vue'
export default {
  name: 'RunsTable',
  props: ['filters', 'options'],
  data () {
    return {
      columns: [
        { name: 'created', label: 'Created', field: 'created', sortable: true },
        { name: 'machine__name', label: 'Machine', field: 'machine__name', sortable: true },
        { name: 'id', label: 'ID', field: 'id', sortable: true },
        { name: 'description', label: 'Description', field: 'description', sortable: false }
      ],
      // visibleColumns: ['id', 'project'],
      combined_options: this.options ? this.options : {}
      // options: { 'title': 'Samples' }
    }
  },
  mounted: function () {
    this.combined_options = this.options ? this.options : {}
    this.combined_options.title = 'Runs'
  },
  components: {
    BaseTable
  }
}
</script>
