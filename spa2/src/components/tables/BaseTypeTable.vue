<template>
  <BaseTable
    :columns="combined_columns"
    :visible-columns="visibleColumns"
    :api-url="apiUrl"
    :options="options"
    :filters="filters"
    ref="table"
  >
    <template v-slot:body="{ props }">
      <q-tr :props="props">
        <slot name="columns" v-bind="{ props }"/>
        <q-td key="type" :props="props"><Property :value="props.row.type" label="name"/></q-td>
        <q-td :key="col.id" v-for="col in type_columns" :label="col.label">{{ props.row.data[col.name] }}</q-td>
      </q-tr>
    </template>
  </BaseTable>
</template>

<script>

import Property from '../details/Property.vue'
import BaseTable from './BaseTable.vue'

export default {
  name: 'SamplesTable',
  props: ['filters', 'options', 'columns', 'visibleColumns', 'apiUrl', 'type'],
  data () {
    return {
      combined_options: this.options ? this.options : {}
    }
  },
  computed: {
    type_columns () {
      return [{ name: 'sample_name', label: 'Sample Name', field: 'data.sample_name', sortable: true }]
    },
    combined_columns () {
      return this.columns.concat(this.type_columns)
    }
  },
  components: {
    BaseTable,
    Property
  }
}

</script>
