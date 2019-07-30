<template>
    <BaseTable
      :columns="columns"
      :visible-columns="['id', 'submission_id', 'type', 'submitted', 'pi_name']"
      api-url="/api/projects/"
      :options="combined_options"
      :filters="filters"
      ref="table"
    >
      <template v-slot:body="{ props }">
        <!-- <q-tr :props="props"><q-td :props="props" key="id">{{props.row.id}}</q-td></q-tr> -->
        <q-tr :props="props">
          <q-td auto-width v-if="combined_options.selection === 'multiple'">
            <q-checkbox dense v-model="props.selected" />
          </q-td>
          <q-td key="id" :props="props"><router-link :to="{ name: 'project', params: { id: props.row.id }}">{{ props.row.id }}</router-link></q-td>
          <q-td key="submission_id" :props="props"><a :href="props.row.submission_url">{{ props.row.submission_id }}</a></q-td>
          <q-td key="type" :props="props">{{ props.row.type.name }}</q-td>
          <q-td key="submitted" :props="props">{{ props.row.submitted | formatDate }}</q-td>
          <q-td key="name" :props="props">{{ props.row.first_name }} {{ props.row.last_name }}</q-td>
          <q-td key="email" :props="props">{{ props.row.email }}</q-td>
          <q-td key="pi_name" :props="props">{{ props.row.pi_first_name }} {{ props.row.pi_last_name }}</q-td>
          <q-td key="pi_email" :props="props">{{ props.row.pi_email }}</q-td>
          <q-td key="sample_data" :props="props"><span v-if="props.row.sample_data">{{ props.row.sample_data.length }}</span></q-td>
          <q-td key="biocore" :props="props"><q-icon size="18px" name="check_circle" v-if="props.row.biocore" color="green"/></q-td>
        </q-tr>
      </template>
    </BaseTable>
</template>

<style>
</style>

<script>
import BaseTable from './BaseTable.vue'
export default {
  name: 'ProjectsTable',
  props: ['filters', 'options'],
  data () {
    return {
      columns: [
        { name: 'id', label: 'ID', field: 'id', sortable: true },
        { name: 'submission_id', label: 'Submission ID', field: 'id', sortable: true },
        { name: 'type', label: 'Type', field: `row.type.name`, sortable: false },
        { name: 'submitted', label: 'Submitted', field: 'submitted', sortable: true },
        { name: 'name', label: 'Submitter', field: 'name' },
        { name: 'email', label: 'Email', field: 'email', sortable: true },
        { name: 'pi_name', label: 'PI', field: 'pi_name' },
        { name: 'pi_email', label: 'PI Email', field: 'pi_email', sortable: true },
        { name: 'sample_data', label: 'Samples', field: 'sample_data', sortable: false },
        { name: 'biocore', label: 'Biocore', field: 'biocore', sortable: true }
      ],
      combined_options: this.options ? this.options : {}
      // visibleColumns: ['id', 'submission_id', 'type', 'submitted', 'pi_name'],
      // options: { 'title': 'Projects' }
    }
  },
  mounted: function () {
    // this.combined_options = this.options ? this.options : {}
    this.combined_options.title = 'Projects'
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
