<template>
  <BaseTable
    :columns="columns"
    :visible-columns="visibleColumns"
    api-url="/api/adapters/"
    :options="combined_options"
    :filters="filters"
    ref="table"
  >
    <template v-slot:body="{ props }">
      <q-tr :props="props">
        <q-td auto-width v-if="combined_options.selection === 'multiple' || combined_options.selection === 'single'">
          <q-checkbox dense v-model="props.selected" />
        </q-td>
        <!-- <q-td key="created" :props="props">{{ props.row.created|formatDate}}</q-td> -->
        <q-td key="name" :props="props">{{ props.row.name }}</q-td>
        <q-td key="barcode" :props="props">{{ props.row.barcode }}</q-td>
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
        { name: 'name', label: 'Name', field: 'name', sortable: true },
        { name: 'barcode', label: 'Barcode', field: 'barcode', sortable: false },
        { name: 'description', label: 'Description', field: 'description', sortable: false }
      ],
      // visibleColumns: ['id', 'project'],
      combined_options: this.options ? this.options : {}
      // options: { 'title': 'Samples' }
    }
  },
  mounted: function () {
    this.combined_options = this.options ? this.options : {}
    this.combined_options.title = 'Adapters'
  },
  components: {
    BaseTable
  }
}
</script>
