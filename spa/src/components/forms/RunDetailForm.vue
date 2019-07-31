<template>
  <BaseForm
    :model="model"
    ref="form"
    api-method="put"
    :api-url="`/api/runs/${model.id}/`"
    :on-success="onSuccess"
    :on-error="onError"
    :hide-buttons="hideButtons"
  >
    <template v-slot:content="{ data, errors, has_error }">
      <q-select outlined v-model="model.machine" :options="options" label="Machine"
        :error-message="errors.machine"
        :error="has_error.machine"
        option-value="id"
        option-label="name"
        emit-value
        map-options
        />
      <q-input outlined v-model="model.name" label="Name"
        :error-message="errors.name"
        :error="has_error.name"
        />
      <q-input outlined v-model="model.description" label="Description" />
      <TableDialog :table-component="PoolsTable" :options="{'selection': 'multiple'}" ref="pools_dialog" :on-select="onSelect"/>
      <table>
        <thead><th>Index</th><th>Pool</th><th>Description</th></thead>
        <tbody>
        <tr v-for="p in pools" v-bind:key="p.id">
          <td>{{ p.index }}</td>
          <td>{{p.pool ? p.pool.name : ''}}
            <q-btn label="Select" color="primary" @click="open('libraries')" />
          </td>
          <td>
            <q-input v-model="p.description" autogrow
              />
          </td>
        </tr>
      </tbody>
      </table>
    </template>
  </BaseForm>
</template>
<script>
import BaseForm from './BaseForm.vue'
import TableDialog from '../dialogs/TableDialog.vue'
import PoolsTable from '../tables/PoolsTable.vue'
import _ from 'lodash'
export default {
  props: ['hideButtons', 'model'], // 'onSuccess', 'onError',
  data () {
    return {
      errors: {},
      data: {},
      options: [
      ],
      PoolsTable: PoolsTable
    }
  },
  methods: {
    onSuccess: function () {
      this.$q.notify('Run updated.')
    },
    onError: function () {
      this.$q.notify('Error updating run.')
    },
    open (table) {
      this.$refs.pools_dialog.open()
    }
  },
  mounted: function () {
    var self = this
    this.$axios.get('/api/machines/')
      .then(function (response) {
        self.options = response.data.results
      })
  },
  computed: {
    pools () {
      return _.orderBy(this.model.run_pools, 'index')
    }
  },
  components: {
    BaseForm,
    TableDialog
  }
}
</script>
