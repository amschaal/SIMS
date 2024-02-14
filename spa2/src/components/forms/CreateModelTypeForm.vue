<template>
    <div>
      {{ content_types }}
      <q-select label="Model" :options="content_types"
        option-value="id"
        option-label="model"
        emit-value
        map-options
        v-model="model.content_type"
      />
      <q-input outlined v-model="model.id" label="Unique ID"
        :error-message="error_messages.id"
        :error="has_error.id"
        />
      <q-input outlined v-model="model.name" label="Name"
        :error-message="error_messages.name"
        :error="has_error.name"
        />
      <q-input outlined v-model="model.description" label="Description" />
      {{ model }}
    </div>
</template>
<script>
import _ from 'lodash'
export default {
  data () {
    return {
      errors: {},
      model: {},
      content_types: [],
      schema: {}
    }
  },
  mounted () {
    this.model = {}
    this.$api.get('/api/content_types/?model__in=machine,project,sample,pool,run')
      .then(response => {
        this.content_types = response.data.results
      })
      .catch(error => {
        this.$q.notify({ message: 'Unable to fetch model content types' })
        console.log(error)
      })
  },
  methods: {
    submit () {
      const self = this
      this.$api.post('/api/model_types/', this.model)
        .then(response => {
          this.$router.push({ name: 'model_type', params: { id: response.data.id } })
        })
        .catch(error => {
          if (error.response && error.response.data) {
            this.errors = error.response.data
            console.log('errors', error.response.data, self.errors)
          }
        })
    }
  },
  computed: {
    error_messages: function () {
      return _.mapValues(this.errors, function (e) { return Array.isArray(e) ? e.join(',') : '' })
    },
    has_error: function () {
      return _.mapValues(this.errors, function (e) { return e !== undefined })
      // return _.mapValues(this.errors, function (e) { return Array.isArray(e) })
    }
  },
  components: {
  }
}
</script>
