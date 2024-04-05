<template>
  <BaseTable
    :columns="columns"
    :visible-columns="visibleColumns"
    api-url="/api/submission_type_mappers/"
    :options="combined_options"
    :filters="filters"
    ref="table"
  >
    <template v-slot:body="{ props }">
      <q-tr :props="props">
        <q-td key="name" :props="props"><router-link :to="{ name: 'submission_type_mapper', params: { id: props.row.id }}">{{ props.row.name }}</router-link></q-td>
        <!-- <q-td key="name" :props="props">{{ props.row.name }}</q-td> -->
        <q-td key="description" :props="props">{{ props.row.description }}</q-td>
      </q-tr>
    </template>
  </BaseTable>
</template>

<script>
import BaseTable from './BaseTable.vue'
export default {
  props: ['filters', 'options'],
  data () {
    return {
      columns: [
        { name: 'name', label: 'Name', field: 'name', sortable: true },
        { name: 'description', label: 'Description', field: 'description', sortable: false }
      ],
      combined_options: this.options ? this.options : {}
    }
  },
  mounted: function () {
    this.combined_options = this.options ? this.options : {}
    this.combined_options.title = 'Submission Type Mappers'
  },
  components: {
    BaseTable
  }
}
</script>
