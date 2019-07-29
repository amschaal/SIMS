<template>
  <BaseTable
    :columns="columns"
    :visible-columns="visibleColumns"
    api-url="/api/pools/"
    :options="combined_options"
    :filters="filters"
    ref="table"
  >
    <template v-slot:body="p">
      <q-tr :props="p">
        <q-td auto-width v-if="combined_options.selection === 'multiple'">
          <q-checkbox dense v-model="p.props.selected" />
        </q-td>
        <q-td key="created" :props="p.props">{{ p.props.row.created }}</q-td>
        <q-td key="id" :props="p.props"><router-link :to="{ name: 'pool', params: { id: p.props.row.id }}">{{ p.props.row.name }}</router-link></q-td>
        <q-td key="description" :props="p.props">{{ p.props.row.description }}</q-td>
      </q-tr>
    </template>
  </BaseTable>
</template>

<script>
import BaseTable from './BaseTable.vue'
export default {
  name: 'PoolsTable',
  props: ['filters', 'options'],
  data () {
    return {
      columns: [
        { name: 'created', label: 'Created', field: 'created', sortable: true },
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
    this.combined_options.title = 'Pools'
  },
  components: {
    BaseTable
  }
}
</script>
