<template>
  <BaseTable
    :columns="columns"
    :visible-columns="visibleColumns"
    api-url="/api/samples/"
    :options="options"
    :filters="filters"
  >
    <template v-slot:body="p">
      <q-tr :props="p.props">
        <q-td key="id" :props="p.props"><router-link :to="{ name: 'sample', params: { id: p.props.row.id }}">{{ p.props.row.id }}</router-link></q-td>
        <q-td key="project" :props="p.props"><router-link :to="{ name: 'project', params: { id: p.props.row.project }}">{{ p.props.row.project }}</router-link></q-td>
      </q-tr>
    </template>
  </BaseTable>
</template>

<script>
import BaseTable from './tables/BaseTable.vue'
export default {
  name: 'SamplesTable',
  props: ['filters'],
  data () {
    return {
      columns: [
        { name: 'id', label: 'ID', field: 'id', sortable: true },
        { name: 'project', label: 'Project', field: 'project', sortable: true }
      ],
      visibleColumns: ['id', 'project'],
      options: { 'title': 'Samples' }
    }
  },
  components: {
    BaseTable
  }
}
</script>
