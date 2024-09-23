<template>
    <BaseTable
      :columns="columns"
      :visible-columns="['type', 'id', 'submission_id', 'created', 'submitted', 'pi_name']"
      api-url="/api/projects/"
      :options="combined_options"
      :filters="filters"
      ref="table"
      model-type="project"
      :show-type="true"
    >
      <template v-slot:columns-top="{ props }">
        <q-td auto-width v-if="combined_options.selection === 'multiple' || combined_options.selection === 'single'">
          <q-checkbox dense v-model="props.selected" />
        </q-td>
      </template>
      <template v-slot:columns="{ props }">
        <!-- <q-tr :props="props"><q-td :props="props" key="id">{{props.row.id}}</q-td></q-tr> -->
          <q-td key="created" :props="props">{{ $filters.formatDate(props.row.created) }}</q-td>
          <q-td key="id" :props="props"><router-link :to="{ name: 'project', params: { id: props.row.id }}">{{ props.row.id }}</router-link></q-td>
          <q-td key="submission" :props="props"><router-link :to="{ name: 'submission', params: { id: props.row.submission.id }}" v-if="props.row.submission">{{ props.row.submission.id }}</router-link></q-td>
          <!-- <q-td key="submission" :props="props">foo</q-td> -->
          <!-- <q-td key="type" :props="props"><Property :value="props.row.type" label="name"/></q-td> -->
          <q-td key="submitted" :props="props">{{ $filters.formatDate(props.row.submitted) }}</q-td>
          <q-td key="name" :props="props">{{ props.row.first_name }} {{ props.row.last_name }}</q-td>
          <q-td key="email" :props="props">{{ props.row.email }}</q-td>
          <q-td key="pi_name" :props="props">{{ props.row.pi_first_name }} {{ props.row.pi_last_name }}</q-td>
          <q-td key="pi_email" :props="props">{{ props.row.pi_email }}</q-td>
          <!-- <q-td key="num_samples" :props="props"><span v-if="props.row.num_samples">{{ props.row.num_samples }}</span></q-td> -->
      </template>
    </BaseTable>
</template>

<style>
</style>

<script>
// import Property from '../details/Property.vue'
import BaseTable from './BaseTypeTable.vue'

import _ from 'lodash'
export default {
  name: 'ProjectsTable',
  props: ['filters', 'options'],
  data () {
    const options = {
      title: 'Projects',
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
        { name: 'id', label: 'ID', field: 'id', sortable: true },
        { name: 'submission', label: 'Submission', field: 'submission', sortable: false },
        { name: 'submitted', label: 'Submitted', field: 'submitted', sortable: true },
        { name: 'name', label: 'Submitter', field: 'name' },
        { name: 'email', label: 'Email', field: 'email', sortable: true },
        { name: 'pi_name', label: 'PI', field: 'pi_name' },
        { name: 'pi_email', label: 'PI Email', field: 'pi_email', sortable: true }
        // { name: 'num_samples', label: 'Samples', field: 'num_samples', sortable: false }
      ],
      combined_options: _.merge(options, this.options)
      // visibleColumns: ['id', 'submission_id', 'type', 'submitted', 'pi_name'],
      // options: { 'title': 'Projects' }
    }
  },
  mounted: function () {
    // this.combined_options = this.options ? this.options : {}
    // this.combined_options.title = 'Projects'
    // this.combined_options.pagination = {
    //   sortBy: 'created',
    //   descending: true,
    //   page: 1,
    //   rowsPerPage: 10,
    //   rowsNumber: 10
    // }
  },
  // mounted () {
  //   // get initial data from server (1st page)
  //   this.refresh()
  // },
  // methods: {
  // },
  components: {
    BaseTable
  }
}
</script>
