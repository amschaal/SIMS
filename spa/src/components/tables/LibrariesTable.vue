<template>
  <BaseTable
    :columns="columns"
    :visible-columns="visibleColumns"
    api-url="/api/libraries/"
    :options="combined_options"
    :filters="filters"
    ref="table"
  >
    <template v-slot:body="{ props }">
      <q-tr :props="props">
        <q-td auto-width v-if="combined_options.selection === 'multiple'">
          <q-checkbox dense v-model="props.selected" />
        </q-td>
        <q-td key="id" :props="props"><router-link :to="{ name: 'library', params: { id: props.row.id }}">{{ props.row.id }}</router-link></q-td>
        <q-td key="sample" :props="props"><router-link :to="{ name: 'sample', params: { id: props.row.sample }}">{{ props.row.sample }}</router-link></q-td>
        <q-td key="project" :props="props"><router-link :to="{ name: 'project', params: { id: props.row.project }}">{{ props.row.project }}</router-link></q-td>
        <q-td key="barcode" :props="props">{{ props.row.barcode }}</q-td>
      </q-tr>
    </template>
  </BaseTable>
</template>

<script>
import BaseTable from './BaseTable.vue'
export default {
  name: 'SamplesTable',
  props: ['filters', 'options'],
  data () {
    return {
      columns: [
        { name: 'id', label: 'ID', field: 'id', sortable: true },
        { name: 'sample', label: 'Sample', field: 'sample', sortable: true },
        { name: 'project', label: 'Project', field: 'project', sortable: true },
        { name: 'barcode', label: 'Barcode', field: 'barcode', sortable: true }
      ],
      visibleColumns: ['id', 'sample', 'project', 'barcode'],
      combined_options: this.options ? this.options : {}
      // options: { 'title': 'Samples' }
    }
  },
  mounted: function () {
    this.combined_options = this.options ? this.options : {}
    this.combined_options.title = 'Libraries'
  },
  components: {
    BaseTable
  }
}
</script>
