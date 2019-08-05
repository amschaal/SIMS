<template>
  <q-btn :color="button_color" :label="button_label" @click="deleteResource"/>
</template>
<script>
export default {
  props: ['url', 'label', 'color', 'redirect'],
  data () {
    return {
      button_color: this.color ? this.color : 'negative',
      button_label: this.label ? this.label : 'Delete'
    }
  },
  methods: {
    deleteResource () {
      var self = this
      this.$axios.delete(this.url)
        .then(function (response) {
          self.$q.notify('Successfully deleted')
          if (self.redirect) {
            self.$router.push(self.redirect)
          } else {
            self.$router.go(-1)
          }
        })
        .catch(function (error) {
          if (error.response.message) {
            this.$q.notify({ color: 'negative', message: error.response.message })
          } else {
            self.$q.notify({ color: 'negative', message: 'There was an error attempting to delete this resource.  Other resources may depend on it.' })
          }
        })
    }
  }
}
</script>
