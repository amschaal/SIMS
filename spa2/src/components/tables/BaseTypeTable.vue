<template>
  <BaseTable
    :columns="combined_columns"
    :visible-columns="visibleColumns"
    :api-url="apiUrl"
    :options="options"
    :filters="filters"
    ref="table"
  >
    <template v-slot:top-left>
      <TypeSelect :dense="true" :error_messages="{}" :has_error="false" v-model="type" :emit_object="true"  :model-filter="'sample'"/>
      {{ type_columns }}
      <!-- <TypeSelect :dense="true" :modelValue="mapping[variable].model_type" @update:model-value="val => selectedModelType(val, variable)" :emit_object="true" v-if="mapping[variable] && mapping[variable].mapping_type === 'model'" :model-filter="mapping[variable].model"/> -->
    </template>
    <template v-slot:body="{ props }">
      <q-tr :props="props">
        <slot name="columns" v-bind="{ props }"/>
        <q-td key="type" :props="props"><Property :value="props.row.type" label="name"/></q-td>
        <q-td :key="col.name" v-for="col in type_columns" :label="col.label">{{ props.row.data[col.name] }}</q-td>
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
  props: ['filters', 'options', 'columns', 'visibleColumns', 'apiUrl'],
  data () {
    return {
      combined_options: this.options ? this.options : {},
      type: null
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
    combined_columns () {
      return this.columns.concat(this.type_columns)
    }
  },
  components: {
    BaseTable,
    Property,
    TypeSelect
  }
}

</script>
