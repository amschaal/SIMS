<template>
    <BaseTable
      :columns="columns"
      :visible-columns="['id', 'submission_id', 'type', 'submitted', 'pi_name']"
      api-url="/api/projects/"
      :options="combined_options"
      :filters="filters"
      ref="table"
    >
      <template v-slot:body="p">
        <!-- <q-tr :props="p.props"><q-td :props="p.props" key="id">{{p.props.row.id}}</q-td></q-tr> -->
        <q-tr :props="p.props">
          <q-td auto-width v-if="combined_options.selection === 'multiple'">
            <q-checkbox dense v-model="p.props.selected" />
          </q-td>
          <q-td key="id" :props="p.props"><router-link :to="{ name: 'project', params: { id: p.props.row.id }}">{{ p.props.row.id }}</router-link></q-td>
          <q-td key="submission_id" :props="p.props"><a :href="p.props.row.submission_url">{{ p.props.row.submission_id }}</a></q-td>
          <q-td key="type" :props="p.props">{{ p.props.row.type.name }}</q-td>
          <q-td key="submitted" :props="p.props">{{ p.props.row.submitted | formatDate }}</q-td>
          <q-td key="name" :props="p.props">{{ p.props.row.first_name }} {{ p.props.row.last_name }}</q-td>
          <q-td key="email" :props="p.props">{{ p.props.row.email }}</q-td>
          <q-td key="pi_name" :props="p.props">{{ p.props.row.pi_first_name }} {{ p.props.row.pi_last_name }}</q-td>
          <q-td key="pi_email" :props="p.props">{{ p.props.row.pi_email }}</q-td>
          <q-td key="sample_data" :props="p.props"><span v-if="p.props.row.sample_data">{{ p.props.row.sample_data.length }}</span></q-td>
          <q-td key="biocore" :props="p.props"><q-icon size="18px" name="check_circle" v-if="p.props.row.biocore" color="green"/></q-td>
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
