<template>
  <div>
    <div v-if="project">
      <!-- {{ project }} -->
      <div class="row">
        <div class="col-md-4 col-sm-12"><b>Project ID: </b>{{project.id}}</div>
        <div class="col-md-4 col-sm-12"><b>Submission ID: </b><a :href="project.submission_id">{{project.submission_id}}</a></div>
        <div class="col-md-4 col-sm-12"><b>Type: </b>{{project.type.name}}</div>
      </div>
      <div class="row">
        <div class="col-md-4 col-sm-12"><b>PI: </b>{{project.pi_first_name}} {{project.pi_last_name}} ({{project.pi_email}})</div>
        <div class="col-md-4 col-sm-12"><b>Submitter: </b>{{project.first_name}} {{project.last_name}} ({{project.email}})</div>
        <div class="col-md-4 col-sm-12"><b>Institute: </b>{{project.institute}}</div>
        <!-- <div class="col-12"><b># Samples: </b>{{project.sample_data.length}}</div> -->
        <div class="col-12"><b>Comments: </b>{{project.comments}}</div>
      </div>
    </div>
  </div>
</template>

<style>
</style>

<script>
export default {
  name: 'ProjectDetails',
  props: ['id', 'project_data'],
  data () {
    return {
      project: null
    }
  },
  mounted: function () {
    console.log('project mounting', this.id)
    if (!this.project) {
      const self = this
      this.$api
        .get(`/api/projects/${self.id}/`)
        .then(function (response) {
          console.log('project response', response)
          // Vue.set(self, 'project', response.data)
          self.project = response.data
        })
    }
  }
}
</script>
