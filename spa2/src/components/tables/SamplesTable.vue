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
        <q-td key="alias" :props="props"><router-link :to="{ name: 'sample', params: { id: props.row.id }}" v-if="props.row.alias">{{ props.row.alias }}</router-link></q-td>
        <q-td key="project" :props="props"><router-link :to="{ name: 'project', params: { id: props.row.project }}">{{ props.row.project }}</router-link></q-td>
        <q-td key="barcodes.i5" :props="props">{{ props.row.barcodes.i5 }}</q-td>
        <q-td key="barcodes.i7" :props="props">{{ props.row.barcodes.i7 }}</q-td>
        <q-td key="barcodes.adapter_db" :props="props">{{ props.row.barcodes.adapter_db }}</q-td>
        <q-td key="barcodes.adapter" :props="props">{{ props.row.barcodes.adapter }}</q-td>
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
        { name: 'alias', label: 'Alias', field: 'alias', sortable: true },
        { name: 'project', label: 'Project', field: 'project', sortable: true },
        { name: 'barcodes.i5', label: 'i5 Barcode', field: 'barcodes', sortable: false },
        { name: 'barcodes.i7', label: 'i7 Barcode', field: 'barcodes', sortable: false },
        { name: 'barcodes.adapter_db', label: 'Adapter DB', field: 'barcodes', sortable: false },
        { name: 'barcodes.adapter', label: 'Adapter', field: 'barcodes', sortable: false }
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
