<template>
  <BaseTable
    :columns="columns"
    :visible-columns="visibleColumns"
    api-url="/api/runs/"
    :options="combined_options"
    :filters="filters"
    ref="table"
    model-type="run"
    :show-type="true"
  >
    <template v-slot:columns-top="{ props }">
      <q-td auto-width>
          <q-btn size="sm" v-if="props.row.schema" color="primary" round dense @click="props.expand = !props.expand" :icon="props.expand ? 'remove' : 'add'" />
      </q-td>
      <q-td auto-width v-if="combined_options.selection === 'multiple' || combined_options.selection === 'single'">
        <q-checkbox dense v-model="props.selected" />
      </q-td>
    </template>
    <template v-slot:columns="{ props }">
      <q-td key="created" :props="props">{{ props.row.created }}</q-td>
      <!-- <q-td key="type" :props="props"><Property :value="props.row.type" label="name"/></q-td> -->
      <q-td key="machine__name" :props="props">{{ props.row.machine_name }}</q-td>
      <q-td key="name" :props="props"><router-link :to="{ name: 'run', params: { id: props.row.id }}">{{ props.row.name }}</router-link></q-td>
      <q-td key="description" :props="props">{{ props.row.description }}</q-td>
    </template>
    <template v-slot:body-bottom="{ props }">
      <q-tr v-show="props.expand" :props="props">
        <q-td colspan="100%">
          <DisplayFields v-model="props.row.data" :schema="props.row.schema" v-if="props.row.id"/>
        </q-td>
      </q-tr>
    </template>
  </BaseTable>
</template>

<script>
import DisplayFields from 'src/assets/jsonschema/components/display/displayFields.vue'
import BaseTable from './BaseTypeTable.vue'
import _ from 'lodash'
// import Property from '../details/Property.vue'
export default {
  name: 'RunsTable',
  props: ['filters', 'options'],
  data () {
    const options = {
      title: 'Runs',
      controlColumn: true,
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
        // { name: 'type', label: 'Type', field: 'type', sortable: true },
        { name: 'machine__name', label: 'Machine', field: 'machine__name', sortable: true },
        { name: 'name', label: 'Name', field: 'name', sortable: true },
        { name: 'description', label: 'Description', field: 'description', sortable: false }
      ],
      visibleColumns: ['type', 'created', 'machine__name', 'name', 'description'],
      combined_options: _.merge(options, this.options)
      // options: { 'title': 'Samples' }
    }
  },
  mounted: function () {
  },
  components: {
    BaseTable,
    DisplayFields
  }
}
</script>
