<template>
  <BaseDialog ref="dialog" :title="title">
    <template v-slot:content>
      <q-markup-table flat bordered v-if="importers.length > 0">
          <tbody>
            <thead>
              <tr>
                <td class="text-left field">Name</td>
                <td class="text-left">Description</td>
                <td></td>
              </tr>
            </thead>
            <tr v-for="i in importers" :key="i.id">
              <td class="text-left field">{{i.name}}</td>
              <td class="text-left">{{ i.description }}</td>
              <td><q-btn label="Import" @click="chooseImporter"/></td>
            </tr>
          </tbody>
        </q-markup-table>
        <h5 v-else>There are no importers.  Set one up for <router-link :to="{ name: 'submission_type', params: { id: submissionType }}">this submission type</router-link>.</h5>
    </template>
    <template v-slot:buttons>
      <q-btn flat label="Close" color="primary" v-close-popup />
    </template>
  </BaseDialog>
</template>
<script>
import BaseDialog from './BaseDialog.vue'
export default {
  props: ['title', 'options', 'submissionType', 'import'],
  data () {
    return {
      importers: []
    }
  },
  methods: {
    open () {
      console.log('open!', this.title)
      this.$refs.dialog.open()
    },
    chooseImporter (id) {
      this.import(id)
      this.$refs.dialog.close()
    }
  },
  mounted: function () {
    this.$api.get(`api/importers/?ordering=id&page=1&page_size=100&submission_type=${this.submissionType}`).then(response => {
      this.importers = response.data.results
    })
  },
  components: {
    BaseDialog
  }
}
</script>
