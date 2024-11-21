<template>
  <BaseTable
    :columns="columns"
    :visible-columns="visibleColumns"
    api-url="/api/machines/"
    :options="combined_options"
    :filters="filters"
    ref="table"
    model-type="machine"
    :show-type="true"
  >
    <template v-slot:columns-top="{ props }">
      <q-td auto-width v-if="combined_options.selection === 'multiple' || combined_options.selection === 'single'">
        <q-checkbox dense v-model="props.selected" />
      </q-td>
    </template>
    <template v-slot:columns="{ props }">
      <!-- <q-td key="created" :props="props">{{ props.row.created|formatDate}}</q-td> -->
      <q-td key="name" :props="props"><router-link :to="{ name: 'machine', params: { id: props.row.id }}">{{ props.row.name }}</router-link></q-td>
      <!-- <q-td key="type" :props="props"><Property :value="props.row.type" label="name"/></q-td> -->
      <q-td key="num_lanes" :props="props">{{ props.row.num_lanes }}</q-td>
      <q-td key="description" :props="props">{{ props.row.description }}</q-td>
    </template>
  </BaseTable>
</template>

<script>
import BaseTable from './BaseTypeTable.vue'
export default {
  props: ['filters', 'options'],
  data () {
    return {
      columns: [
        { name: 'name', label: 'Name', field: 'name', sortable: true },
        { name: 'num_lanes', label: '# Lanes/Cells/Partitions', field: 'num_lanes', sortable: true },
        { name: 'description', label: 'Description', field: 'description', sortable: false }
      ],
      visibleColumns: ['type', 'name', 'num_lanes', 'description'],
      combined_options: this.options ? this.options : {}
      // options: { 'title': 'Samples' }
    }
  },
  mounted: function () {
    this.combined_options = this.options ? this.options : {}
    this.combined_options.title = 'Machines'
  },
  components: {
    BaseTable
  }
}
</script>
