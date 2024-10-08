<template>
    <q-table
      :title="options.title"
      :rows="data"
      :columns="columns"
      row-key="id"
      v-model:pagination="pagination"
      :loading="loading"
      :filter="filter"
      @request="onRequest"
      binary-state-sort
      :visible-columns="tableColumns"
      :selected-rows-label="getSelectedString"
      :selection="selection"
      v-model:selected="selected"
    >
      <template v-slot:top-left>
        <q-input borderless dense debounce="300" v-model="filter" placeholder="Search">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
        <slot name="top-left"/>
      </template>
      <template v-slot:top-right>
       <q-select
         v-model="tableColumns"
         @update:model-value="updatedVisibleColumns"
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
     <template v-slot:header="props">
      <q-tr :props="props">
        <q-th auto-width v-if="options.controlColumn || selection"/>
        <q-th
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
        >
          {{ col.label }}
        </q-th>
      </q-tr>
    </template>
     <template v-slot:body="props">
        <slot name="body" v-bind:props="props">
          <q-tr :props="props">
            <q-td :props="props" key="id">{{props.row.id}}</q-td>
          </q-tr>
        </slot>
      </template>
     <!-- <template slot="body" slot-scope="props">
       <slot name="body" v-bind:props="props">
          Example
         <template v-slot:body="p">
         <q-tr :props="p.props"><q-td :props="p.props" key="id">{{p.props.row.id}}</q-td></q-tr>
       </template>
       </slot>
     </template> -->
    </q-table>
</template>

<style>
</style>

<script>
import _ from 'lodash'

export default {
  name: 'BaseTable',
  props: ['apiUrl', 'columns', 'visibleColumns', 'options', 'filters'],
  emits: ['update:visibleColumns'],
  data () {
    const options = {
      pagination: this.options && this.options.pagination ? this.options.pagination : {
        sortBy: 'id',
        descending: false,
        page: 1,
        rowsPerPage: 10,
        rowsNumber: 10
      }
    }
    return {
      selected: [],
      selection: this.options && this.options.selection ? this.options.selection : '',
      filter: '',
      loading: false,
      tableColumns: this.visibleColumns,
      pagination: _.merge(options.pagination, this.options.pagination),
      // columns: [
      //   // {
      //   //   name: 'desc',
      //   //   required: true,
      //   //   label: 'Dessert (100g serving)',
      //   //   field: row => row.name,
      //   //   format: val => `${val}`,
      //   //   sortable: true
      //   // },
      //   { name: 'id', label: 'ID', field: 'id', sortable: true },
      //   { name: 'submission_id', label: 'Submission ID', field: 'id', sortable: true },
      //   { name: 'type', label: 'Type', field: `row.type.name`, sortable: false },
      //   { name: 'submitted', label: 'Submitted', field: 'submitted', sortable: true },
      //   { name: 'name', label: 'Submitter', field: 'name' },
      //   { name: 'email', label: 'Email', field: 'email', sortable: true },
      //   { name: 'pi_name', label: 'PI', field: 'pi_name' },
      //   { name: 'pi_email', label: 'PI Email', field: 'pi_email', sortable: true },
      //   { name: 'sample_data', label: 'Samples', field: 'sample_data', sortable: false },
      //   { name: 'biocore', label: 'Biocore', field: 'biocore', sortable: true }
      // ],
      // visibleColumns: ['id', 'submission_id', 'type', 'submitted', 'pi_name'],
      data: []
    }
  },
  mounted () {
    // get initial data from server (1st page)
    this.refresh()
  },
  methods: {
    onRequest ({ pagination, filter }) {
      console.log('onRequest', pagination, filter, this)
      const self = this
      // we set QTable to "loading" state
      this.loading = true

      // we do the server data fetch, based on pagination and filter received
      // (using Axios here, but can be anything; parameters vary based on backend implementation)
      console.log('request', pagination, filter)
      let sortBy = pagination.sortBy
      if (pagination.descending) {
        sortBy = '-' + sortBy
      }
      const search = this.filter !== '' ? `&search=${this.filter}` : ''
      // var cancelled = !this.showCancelled ? '&cancelled__isnull=true' : ''
      // var completed = !this.showCompleted ? '&status__iexact!=completed' : ''
      const pageSize = pagination.rowsPerPage ? pagination.rowsPerPage : 1000000 // HACKY
      // var type = this.$route.query.type ? `&type__name__icontains=${this.$route.query.type}` : ''
      this.$api
        .get(`${this.apiUrl}?ordering=${sortBy}&page=${pagination.page}&page_size=${pageSize}${search}&${this.filters}`)// ${pagination.descending}&filter=${filter}
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
          // self.$q.notify({ color: 'negative', message: 'There was an error retrieving data.' })
        })
    },
    refresh () {
      this.onRequest({
        pagination: this.pagination,
        filter: this.filter
      })
    },
    getSelectedString () {
      return this.selected.length === 0 ? '' : `${this.selected.length} record${this.selected.length > 1 ? 's' : ''} selected of ${this.data.length}`
    },
    getSelected () {
      return this.selected
    },
    updatedVisibleColumns (v) {
      this.$emit('update:visibleColumns', v)
    }
  },
  watch: {
    filters (val, old) {
      this.refresh()
    },
    selected (val, old) {
      this.$emit('selected', val)
      this.$emit('update:selection', val)
    }
  }
}
</script>
