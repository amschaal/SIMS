<template>
  <q-dialog ref="dialog" @hide="onDialogHide">
    <q-card class="q-dialog-plugin" style="min-width: 800px;">
      <q-toolbar>
        <q-toolbar-title>Barcode conflicts for pool <router-link :to="{ name: 'pool', params: { id: pool.id }}">{{ pool.name }}</router-link></q-toolbar-title>
      </q-toolbar>
      <q-markup-table v-if="Object.keys(conflicts).length">
        <thead>
          <tr><th>Sample</th><th>i5 Conflicts</th><th>i7 Conflicts</th></tr>
        </thead>
        <tbody>
          <tr v-for="(sample_conflicts, sample) in conflicts" :key="sample">
            <td>
                <router-link :to="{ name: 'sample', params: { id: sample }}">{{ sample }}</router-link>
            </td>
            <td>
              <span v-if="sample_conflicts.i5">
                <router-link :to="{ name: 'sample', params: { id: sample_id }}" v-for="sample_id in sample_conflicts.i5" :key="sample_id" style="margin-right:5px;">{{ sample_id }}</router-link>
              </span>
            </td>
            <td>
              <span v-if="sample_conflicts.i7">
                <router-link :to="{ name: 'sample', params: { id: sample_id }}" v-for="sample_id in sample_conflicts.i7" :key="sample_id" style="margin-right:5px;">{{ sample_id }}</router-link>
              </span>
            </td>
          </tr>
        </tbody>
      </q-markup-table>
      <b v-else>No conflicts found.</b>
      <q-card-actions>
        <!-- <q-btn color="primary" label="OK" @click="onOKClick" /> -->
        <q-btn color="primary" label="Dismiss" @click="onCancelClick" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
export default {
  props: ['pool'],

  emits: [
    // REQUIRED
    'ok', 'hide'
  ],

  data () {
    return {
      conflicts: {}
    }
  },

  methods: {
    // following method is REQUIRED
    // (don't change its name --> "show")
    show () {
      this.$api.get(`/api/pools/${this.pool.id}/check_barcodes/`).then(response => {
        this.$refs.dialog.show()
        this.conflicts = response.data.conflicts
      }).catch(error => {
        this.$q.notify({ color: 'negative', message: 'There was an error checking barcodes.  Please check them manually. Exception: ' + error.message })
        this.hide()
      })
    },

    // following method is REQUIRED
    // (don't change its name --> "hide")
    hide () {
      this.$refs.dialog.hide()
    },

    onDialogHide () {
      // required to be emitted
      // when QDialog emits "hide" event
      this.$emit('hide')
    },

    onOKClick () {
      // on OK, it is REQUIRED to
      // emit "ok" event (with optional payload)
      // before hiding the QDialog
      this.$emit('ok')
      // or with payload: this.$emit('ok', { ... })

      // then hiding dialog
      this.hide()
    },

    onCancelClick () {
      // we just need to hide the dialog
      this.hide()
    }
  }
}
</script>
