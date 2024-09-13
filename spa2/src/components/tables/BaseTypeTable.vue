<template>
  <BaseTable
    :columns="combined_columns"
    v-model:visible-columns="tableColumns"
    :api-url="apiUrl"
    :options="options"
    :filters="combined_filters"
    ref="table"
  >
    <template v-slot:top-left>
      <TypeSelect :dense="true" :error_messages="{}" :has_error="false" v-model="type" :emit_object="true"  :model-filter="modelType"/>
      <!-- {{ type }} -->
      <!-- {{ showType }} -->
      <!-- {{ combined_columns }} -->
      <!-- {{ type_columns }} -->
      <!-- {{ tableColumns }} -->
      <!-- {{ visible_type_columns }} -->
      <!-- <TypeSelect :dense="true" :modelValue="mapping[variable].model_type" @update:model-value="val => selectedModelType(val, variable)" :emit_object="true" v-if="mapping[variable] && mapping[variable].mapping_type === 'model'" :model-filter="mapping[variable].model"/> -->
    </template>
    <template v-slot:body="{ props }">
      <q-tr :props="props">
        <q-td key="type" :props="props" v-if="showType"><Property :value="props.row.type" label="name"/></q-td>
        <slot name="columns" v-bind="{ props }"/>
        <q-td :key="col.name" v-for="col in visible_type_columns" :label="col.label" class="text-right">{{ props.row.data[col.name] }}</q-td>
      </q-tr>
    </template>
  </BaseTable>
</template>

<script>

import Property from '../details/Property.vue'
import BaseTable from './BaseTable.vue'
import TypeSelect from 'src/components/TypeSelect.vue'

export default {
  name: 'SamplesTable',
  props: ['filters', 'options', 'columns', 'visibleColumns', 'apiUrl', 'showType', 'modelType'],
  data () {
    return {
      combined_options: this.options ? this.options : {},
      type: null,
      tableColumns: this.visibleColumns,
      typeColumn: { name: 'type', label: 'Type', field: 'type', sortable: true },
      initialFilters: this.filters
    }
  },
  computed: {
    type_columns () {
      if (!this.type || !this.type.schema || !this.type.schema.order) {
        return []
      } else {
        return this.type.schema.order.map(v => ({ name: v, label: v, field: `data.${v}`, sortable: false })) // this.type.schema.properties[v].title
      }
      // return [{ name: 'sample_name', label: 'Sample Name', field: 'data.sample_name', sortable: true }]
    },
    visible_type_columns () {
      console.log('compute visible type columns', this.visibleColumns)
      return this.type_columns.filter(c => this.tableColumns.indexOf(c.name) !== -1)
    },
    combined_columns () {
      return this.showType ? [this.typeColumn].concat(this.columns).concat(this.type_columns) : this.columns.concat(this.type_columns)
    },
    combined_filters () {
      return this.type ? this.initialFilters + '&type__id=' + this.type.id : this.initialFilters
    }
  },
  components: {
    BaseTable,
    Property,
    TypeSelect
  }
}

</script>
