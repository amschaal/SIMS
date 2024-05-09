<template>
  <BaseTable
    :columns="columns"
    :visible-columns="visibleColumns"
    api-url="/api/pools/"
    :options="combined_options"
    :filters="combined_filters"
    ref="table"
  >
    <template v-slot:top-left>
      <q-radio label="All pools" v-model="locked" val="all" :disable="options && options.locked_only"/>
      <q-radio label="Locked pools" v-model="locked" val="locked" :disable="options && options.locked_only"/>
      <q-radio label="Unlocked pools" v-model="locked" val="unlocked" :disable="options && options.locked_only"/>
    </template>
    <template v-slot:body="{ props }">
      <q-tr :props="props">
        <q-td auto-width v-if="combined_options.selection === 'multiple' || combined_options.selection === 'single'">
          <q-checkbox dense v-model="props.selected" />
        </q-td>
        <q-td key="locked" :props="props"><q-icon name="lock" color="negative" v-if="props.row.locked" :title="props.row.locked"/><q-icon v-else name="lock_open" color="positive"/></q-td>
        <q-td key="created" :props="props">{{ props.row.created }}</q-td>
        <q-td key="type" :props="props"><Property :value="props.row.type" label="name"/></q-td>
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
import Property from '../details/Property.vue'
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
        { name: 'locked', label: 'Locked', field: 'locked', sortable: true },
        { name: 'created', label: 'Created', field: 'created', sortable: true },
        { name: 'type', label: 'Type', field: 'type', sortable: true },
        { name: 'id', label: 'ID', field: 'id', sortable: true },
        { name: 'pools', label: 'Pools', field: 'pools', sortable: false },
        { name: 'samples', label: 'Samples', field: 'samples', sortable: false },
        { name: 'description', label: 'Description', field: 'description', sortable: false }
      ],
      // visibleColumns: ['id', 'project'],
      combined_options: _.merge(options, this.options),
      locked: this.options && this.options.locked_only ? 'locked' : 'all',
      locked_options: [{ label: 'All pools', value: '' }, { label: 'Locked pools', value: 'locked' }, { label: 'Unlocked pools', value: 'unlocked' }]
      // options: { 'title': 'Samples' }
    }
  },
  computed: {
    combined_filters () {
      let filter = ''
      if (this.locked === 'locked') {
        filter = '&locked__isnull=False'
      } else if (this.locked === 'unlocked') {
        filter = '&locked__isnull=True'
      }
      return this.filters + filter
    }
  },
  mounted: function () {
    // this.combined_options = this.options ? this.options : {}
    // this.combined_options.title = 'Pools'
  },
  components: {
    BaseTable,
    Property
  }
}
</script>
