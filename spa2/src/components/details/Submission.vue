<template>
  <div>
    <div v-if="submission">
      <div class="row">
        <div class="col-md-4 col-sm-12"><b>System ID: </b>{{submission.id}}</div>
        <div class="col-md-4 col-sm-12">
          <b>Project: </b>
          <router-link :to="{ name: 'project', params: { id: submission.project }}" v-if="submission.project">{{ submission.project }}</router-link>
          <span v-else>None</span>
          <span v-if="submission.importer"> Imported using importer "{{ submission.importer.name }}" at {{ $filters.formatDate(submission.imported) }}</span>
        </div>
        <div class="col-md-4 col-sm-12"><b>ID: </b>{{submission.submission_id}}</div>
        <div class="col-md-4 col-sm-12"><b>Type: </b><router-link :to="{ name: 'submission_type', params: { id: submission.type.id }}">{{submission.type.name}}</router-link></div>
      </div>
      <div class="row">
        <div class="col-md-4 col-sm-12"><b>PI: </b>{{submission.pi_first_name}} {{submission.pi_last_name}} ({{submission.pi_email}})</div>
        <div class="col-md-4 col-sm-12"><b>Submitter: </b>{{submission.first_name}} {{submission.last_name}} ({{submission.email}})</div>
        <div class="col-md-4 col-sm-12"><b>Institute: </b>{{submission.institute}}</div>
        <div class="col-12"><b>Comments: </b>{{submission.comments}}</div>
      </div>
      <fieldset>
        <legend>{{submission.type.name}} Fields</legend>
        <CustomFields v-model="submission.data" :schema="submission.schema" ref="submission_fields" v-if="submission.schema && submission.data" :modify="false" :warnings="{}"/>
      </fieldset>
    </div>
  </div>
</template>

<style>
</style>

<script>
import CustomFields from 'src/assets/jsonschema/forms/customFields.vue'
export default {
  name: 'ProjectDetails',
  props: ['id', 'instance'],
  data () {
    return {
      data: null
    }
  },
  mounted: function () {
    if (!this.submission) {
      const self = this
      this.$api
        .get(`/api/submissions/${self.id}/`)
        .then(function (response) {
          self.data = response.data
        })
    }
  },
  computed: {
    submission () {
      return this.instance || this.data
    }
  },
  components: {
    CustomFields
  }
}
</script>
