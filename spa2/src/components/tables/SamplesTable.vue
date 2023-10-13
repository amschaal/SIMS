<template>
  <div>Samples</div>
  <BaseTable
    :columns="columns"
    :visible-columns="visibleColumns"
    api-url="/api/samples/"
    :options="combined_options"
    :filters="filters"
    ref="table"
  >
    <template v-slot:body="{ props }">
      <q-tr :props="props">
        <q-td auto-width v-if="combined_options.selection === 'multiple' || combined_options.selection === 'single'">
          <q-checkbox dense v-model="props.selected" />
        </q-td>
        <q-td key="id" :props="props"><router-link :to="{ name: 'sample', params: { id: props.row.id }}">{{ props.row.id }}</router-link></q-td>
        <q-td key="project" :props="props"><router-link :to="{ name: 'project', params: { id: props.row.project }}">{{ props.row.project }}</router-link></q-td>
      </q-tr>
    </template>
  </BaseTable>
</template>

<script>

import BaseTable from './BaseTable.vue'
export default {
  name: 'SamplesTable',
  props: ['filters', 'options'],
  data () {
    return {
      columns: [
        { name: 'id', label: 'ID', field: 'id', sortable: true },
        { name: 'project', label: 'Project', field: 'project', sortable: true }
      ],
      visibleColumns: ['id', 'project'],
      combined_options: this.options ? this.options : {}
      // options: { 'title': 'Samples' }
    }
  },
  mounted: function () {
    this.combined_options = this.options ? this.options : {}
    this.combined_options.title = 'Samples'
  },
  components: {
    BaseTable
  }
}

// import { defineComponent } from 'vue'

// export default defineComponent({
//   name: 'SamplesTable',
//   props: ['filters', 'options']
// })
</script>
