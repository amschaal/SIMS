<template>
  <BaseTable
    :columns="columns"
    :visible-columns="visibleColumns"
    api-url="/api/pools/"
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
        <q-td key="id" :props="props"><router-link :to="{ name: 'pool', params: { id: props.row.id }}">{{ props.row.name }}</router-link></q-td>
        <q-td key="pools" :props="props">{{ props.row.pools.length }}
          <q-tooltip v-if="props.row.pools.length > 0">
            {{props.row.pools.map(p => p.name).join(', ')}}
          </q-tooltip>
        </q-td>
        <q-td key="libraries" :props="props">{{ props.row.libraries.length }}
          <q-tooltip v-if="props.row.libraries.length > 0">
            {{props.row.libraries.map(p => p.id).join(', ')}}
          </q-tooltip>
        </q-td>
        <q-td key="description" :props="props">{{ props.row.description }}</q-td>
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
        { name: 'pools', label: 'Pools', field: 'pools', sortable: false },
        { name: 'libraries', label: 'Libraries', field: 'libraries', sortable: false },
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
