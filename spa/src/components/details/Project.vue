<template>
  <div>
    <div class="row">
      <div class="col-md-4 col-sm-6"><b>Project ID: </b>{{project.id}}</div>
      <div class="col"><b>Submission ID: </b><a :href="project.submission_id">{{project.submission_id}}</a></div>
    </div>
    <div class="row">
      <div class="col-md-4 col-sm-6"><b>PI: </b>{{project.pi_first_name}} {{project.pi_last_name}} ({{project.pi_email}})</div>
      <div class="col"><b>Submitter: </b>{{project.first_name}} {{project.last_name}} ({{project.email}})</div>
    </div>
  </div>
</template>

<style>
</style>

<script>
import Vue from 'vue'
export default {
  name: 'project',
  props: ['id', 'project'],
  data () {
    return {
      // project: this.instance
    }
  },
  mounted: function () {
    if (!this.project) {
      var self = this
      this.$axios
        .get(`/api/projects/${self.id}/`)
        .then(function (response) {
          console.log('response', response)
          Vue.set(self, 'project', response.data)
        })
    }
  }
}
</script>
