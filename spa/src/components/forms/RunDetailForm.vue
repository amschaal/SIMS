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
    <template v-slot:content="{ data, errors, has_error, _errors }">
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
      <TableDialog :table-component="PoolsTable" :options="{'selection': 'single'}" ref="pools_dialog" :on-select="onSelect"/>
      <table class="full-width">
        <thead><th>Index</th><th>Pool</th><th>Description</th></thead>
        <tbody>
        <tr v-for="(p, ind)  in pools" v-bind:key="p.id">
          <td>{{ p.index }}</td>
          <td>
            <span v-if="p.pool">
              <q-btn label="Clear" size="sm" color="negative" @click="clearLane(p)" class="on-left"/>
              <router-link :to="{ name: 'pool', params: { id: p.pool.id }}">{{p.pool.name}}</router-link>
              <span v-if="p.pool.libraries.length > 0"> ({{p.pool.libraries.length}} libraries)
                <q-tooltip>
                  {{p.pool.libraries.map(l => l.id).join(', ')}}
                </q-tooltip>
              </span>
              <span v-if="p.pool.pools.length > 0"> ({{p.pool.pools.length}} pools)
                <q-tooltip>
                  {{p.pool.pools.map(p => p.name).join(', ')}}
                </q-tooltip>
              </span>
            </span>
            <q-btn v-else label="Select" size="sm" color="primary" @click="open(p)" class="on-left"/>
            <span class="q-field--error" v-if="_errors.run_pools && _errors.run_pools[ind].pool">
              <span class="q-field__bottom">{{_errors.run_pools[ind].pool.join(', ')}}</span>
            </span>
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
      currentLane: null,
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
    open (lane) {
      this.currentLane = lane
      this.$refs.pools_dialog.open()
    },
    onSelect (selected) {
      console.log('selected', this.currentLane, selected)
      if (selected.length === 1) {
        this.currentLane.pool = selected[0]
      }
    },
    clearLane (lane) {
      lane.pool = null
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
