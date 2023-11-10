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
        <q-td key="samples" :props="props">{{ props.row.samples.length }}
          <q-tooltip v-if="props.row.samples.length > 0">
            {{props.row.samples.map(p => p.id).join(', ')}}
          </q-tooltip>
        </q-td>
        <q-td key="description" :props="props">{{ props.row.description }}</q-td>
      </q-tr>
    </template>
  </BaseTable>
</template>

<script>
import BaseTable from './BaseTable.vue'
import _ from 'lodash'
export default {
  name: 'PoolsTable',
  props: ['filters', 'options'],
  data () {
    const options = {
      title: 'Pools',
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
        { name: 'id', label: 'ID', field: 'id', sortable: true },
        { name: 'pools', label: 'Pools', field: 'pools', sortable: false },
        { name: 'samples', label: 'Samples', field: 'samples', sortable: false },
        { name: 'description', label: 'Description', field: 'description', sortable: false }
      ],
      // visibleColumns: ['id', 'project'],
      combined_options: _.merge(options, this.options)
      // options: { 'title': 'Samples' }
    }
  },
  mounted: function () {
    // this.combined_options = this.options ? this.options : {}
    // this.combined_options.title = 'Pools'
  },
  components: {
    BaseTable
  }
}
</script>
