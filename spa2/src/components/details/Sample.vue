<template>
  <div>
    <div class="row">
      <div class="col-md-4 col-sm-12"><b>ID: </b>{{sample.id}}</div>
      <div class="col-md-4 col-sm-12"><b>Project: </b><router-link :to="{ name: 'project', params: { id: sample.project }}">{{sample.project}}</router-link></div>
    </div>
    <div class="row">
      <div class="col-md-4 col-sm-12"><b>Name: </b>{{sample.name}}</div>
      <div class="col-md-4 col-sm-12"><b>Imported: </b>{{$filters.formatDate(sample.imported)}}</div>
    </div>
    <!-- <div class="row">
      <div class="col-12" v-for="(v, k) in sample.data" :key="k"><b>{{k}}: </b>{{v}}</div>
    </div> -->
  </div>
</template>

<style>
</style>

<script>
export default {
  name: 'SampleDetail',
  props: ['id', 'instance'],
  data () {
    return {
      data: this.instance
    }
  },
  mounted: function () {
    if (!this.instance) {
      const self = this
      this.$api
        .get(`/api/sample/${self.id}/`)
        .then(function (response) {
          console.log('response', response)
          self.data = response.data
        })
    }
  },
  computed: {
    sample () {
      return this.instance || this.data
    }
  }
}

// import { defineComponent, ref } from 'vue'

// export default defineComponent({
//   name: 'sample',
//   props: ['id', 'sample'],
//   components: {
//   },

//   setup () {
//     if (!this.project) {
//       var self = this
//       this.$api
//         .get(`/api/sample/${self.id}/`)
//         .then(function (response) {
//           console.log('response', response)
//           Vue.set(self, 'sample', response.data)
//         })
//     }
//   }
// })

</script>
