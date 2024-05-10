<template>
    <BaseTable
      :columns="columns"
      :visible-columns="['id', 'submission_id', 'project', 'type', 'created', 'submitted', 'pi_name']"
      api-url="/api/submissions/"
      :options="combined_options"
      :filters="filters"
      ref="table"
    >
      <template v-slot:body="{ props }">
        <!-- <q-tr :props="props"><q-td :props="props" key="id">{{props.row.id}}</q-td></q-tr> -->
        <q-tr :props="props">
          <q-td auto-width v-if="combined_options.selection === 'multiple' || combined_options.selection === 'single'">
            <q-checkbox dense v-model="props.selected" />
          </q-td>
          <q-td key="imported" :props="props">{{ $filters.formatDate(props.row.imported) }}</q-td>
          <q-td key="id" :props="props"><router-link :to="{ name: 'submission', params: { id: props.row.id }}">{{ props.row.id }}</router-link></q-td>
          <!-- <q-td key="id" :props="props">{{ props.row.id }}</q-td> -->
          <q-td key="submission_id" :props="props"><a :href="props.row.submission_url">{{ props.row.submission_id }}</a></q-td>
          <q-td key="project" :props="props"><router-link :to="{ name: 'project', params: { id: props.row.project }}" v-if="props.row.project">{{ props.row.project }}</router-link><span v-else>None</span></q-td>
          <q-td key="type" :props="props"><router-link v-if="props.row.type && props.row.type.id" :to="{ name: 'submission_type', params: { id: props.row.type.id }}">{{ props.row.type.name }}</router-link></q-td>
          <q-td key="submitted" :props="props">{{ $filters.formatDate(props.row.submitted) }}</q-td>
          <q-td key="name" :props="props">{{ props.row.first_name }} {{ props.row.last_name }}</q-td>
          <q-td key="email" :props="props">{{ props.row.email }}</q-td>
          <q-td key="pi_name" :props="props">{{ props.row.pi_first_name }} {{ props.row.pi_last_name }}</q-td>
          <q-td key="pi_email" :props="props">{{ props.row.pi_email }}</q-td>
        </q-tr>
      </template>
    </BaseTable>
</template>

<style>
</style>

<script>
import BaseTable from './BaseTable.vue'
import _ from 'lodash'
export default {
  name: 'SubmissionsTable',
  props: ['filters', 'options'],
  data () {
    const options = {
      title: 'Submissions',
      pagination: {
        sortBy: 'imported',
        descending: true,
        page: 1,
        rowsPerPage: 10,
        rowsNumber: 10
      }
    }
    return {
      columns: [
        { name: 'imported', label: 'Imported', field: 'imported', sortable: true },
        { name: 'id', label: 'ID', field: 'id', sortable: true },
        { name: 'submission_id', label: 'Submission ID', field: 'id', sortable: true },
        { name: 'project', label: 'Project', field: 'project', sortable: false },
        { name: 'type', label: 'Type', field: 'row.type.name', sortable: false },
        { name: 'submitted', label: 'Submitted', field: 'submitted', sortable: true },
        { name: 'name', label: 'Submitter', field: 'name' },
        { name: 'email', label: 'Email', field: 'email', sortable: true },
        { name: 'pi_name', label: 'PI', field: 'pi_name' },
        { name: 'pi_email', label: 'PI Email', field: 'pi_email', sortable: true }
      ],
      combined_options: _.merge(options, this.options)
    }
  },
  mounted: function () {
  },
  components: {
    BaseTable
  }
}
</script>
