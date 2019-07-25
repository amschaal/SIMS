<template>
  <q-page class="flex flex-center">
    <q-table
      title="Projects"
      :data="data"
      :columns="columns"
      row-key="id"
      :pagination.sync="pagination"
      :loading="loading"
      :filter="filter"
      @request="onRequest"
      binary-state-sort
      :visible-columns="visibleColumns"
    >
      <template v-slot:top-right>
        <q-input borderless dense debounce="300" v-model="filter" placeholder="Search">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
      </template>
      <template v-slot:top="props">
       <q-select
         v-model="visibleColumns"
         multiple
         borderless
         dense
         options-dense
         :display-value="$q.lang.table.columns"
         emit-value
         map-options
         :options="columns"
         option-value="name"
         style="min-width: 150px"
       />
     </template>
      <template slot="body" slot-scope="props">
        <q-tr :props="props">
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
    </q-table>
  </q-page>
</template>

<style>
</style>

<script>
export default {
  data () {
    return {
      filter: '',
      loading: false,
      pagination: {
        sortBy: 'id',
        descending: false,
        page: 1,
        rowsPerPage: 10,
        rowsNumber: 10
      },
      columns: [
        // {
        //   name: 'desc',
        //   required: true,
        //   label: 'Dessert (100g serving)',
        //   field: row => row.name,
        //   format: val => `${val}`,
        //   sortable: true
        // },
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
      visibleColumns: ['id', 'submission_id', 'type', 'submitted', 'pi_name'],
      data: []
    }
  },
  name: 'Projects',
  mounted () {
    // get initial data from server (1st page)
    this.refresh()
  },
  methods: {
    onRequest ({ pagination, filter }) {
      var self = this
      // we set QTable to "loading" state
      this.loading = true

      // we do the server data fetch, based on pagination and filter received
      // (using Axios here, but can be anything; parameters vary based on backend implementation)
      console.log('request', pagination, filter)
      var sortBy = pagination.sortBy
      if (pagination.descending) {
        sortBy = '-' + sortBy
      }
      var search = this.filter !== '' ? `&search=${this.filter}` : ''
      // var cancelled = !this.showCancelled ? '&cancelled__isnull=true' : ''
      // var completed = !this.showCompleted ? '&status__iexact!=completed' : ''
      var pageSize = pagination.rowsPerPage ? pagination.rowsPerPage : 1000000 // HACKY
      // var type = this.$route.query.type ? `&type__name__icontains=${this.$route.query.type}` : ''
      this.$axios
        .get(`/api/projects/?ordering=${sortBy}&page=${pagination.page}&page_size=${pageSize}${search}`)// ${pagination.descending}&filter=${filter}
        .then(({ data }) => {
          console.log('data', data)
          // updating pagination to reflect in the UI
          self.pagination = pagination

          // we also set (or update) rowsNumber
          self.pagination.rowsNumber = data.count

          // then we update the rows with the fetched ones
          self.data = data.results

          // finally we tell QTable to exit the "loading" state
          self.loading = false
        })
        .catch(error => {
          // there's an error... do SOMETHING
          console.log(error)
          // we tell QTable to exit the "loading" state
          self.loading = false
        })
    },
    refresh () {
      this.onRequest({
        pagination: this.pagination,
        filter: this.filter
      })
    }
  }
}
</script>
