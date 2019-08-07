<template>
  <div>
    <div class="row">
      <div class="col-md-4 col-sm-12"><b>Project ID: </b>{{project.id}}</div>
      <div class="col-md-4 col-sm-12"><b>Submission ID: </b><a :href="project.submission_id">{{project.submission_id}}</a></div>
      <div class="col-md-4 col-sm-12"><b>Type: </b>{{project.type.name}}</div>
    </div>
    <div class="row">
      <div class="col-md-4 col-sm-12"><b>PI: </b>{{project.pi_first_name}} {{project.pi_last_name}} ({{project.pi_email}})</div>
      <div class="col-md-4 col-sm-12"><b>Submitter: </b>{{project.first_name}} {{project.last_name}} ({{project.email}})</div>
      <div class="col-md-4 col-sm-12"><b>Institute: </b>{{project.institute}})</div>
      <div class="col-12"><b># Samples: </b>{{project.sample_data.length}}</div>
      <div class="col-12"><b>Comments: </b>{{project.comments}})</div>
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
