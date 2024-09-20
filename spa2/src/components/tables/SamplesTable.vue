<template>
  <BaseTable
    :columns="columns"
    :visible-columns="visibleColumns"
    api-url="/api/samples/"
    :options="combined_options"
    :filters="filters"
    ref="table"
    model-type="sample"
    :show-type="true"
  >
    <template v-slot:columns-top="{ props }">
      <q-td auto-width v-if="combined_options.selection === 'multiple' || combined_options.selection === 'single'">
        <q-checkbox dense v-model="props.selected" />
      </q-td>
    </template>
    <template v-slot:columns="{ props }">
      <!-- <q-tr :props="props"> -->
        <!-- <q-td key="type" :props="props"><Property :value="props.row.type" label="name"/></q-td> -->
        <q-td key="id" :props="props"><router-link :to="{ name: 'sample', params: { id: props.row.id }}">{{ props.row.id }}</router-link></q-td>
        <q-td key="project" :props="props"><router-link :to="{ name: 'project', params: { id: props.row.project }}">{{ props.row.project }}</router-link></q-td>
      <!-- </q-tr> -->
    </template>
  </BaseTable>
</template>

<script>

// import Property from '../details/Property.vue'
import BaseTable from './BaseTypeTable.vue'

export default {
  name: 'SamplesTable',
  props: ['filters', 'options'],
  data () {
    return {
      columns: [
        { name: 'id', label: 'ID', field: 'id', sortable: true },
        { name: 'project', label: 'Project', field: 'project', sortable: true }
      ],
      visibleColumns: ['type', 'id', 'project'],
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
    // Property
  }
}

// import { defineComponent } from 'vue'

// export default defineComponent({
//   name: 'SamplesTable',
//   props: ['filters', 'options']
// })
</script>
