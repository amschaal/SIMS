<template>
  <BaseDialog ref="dialog" :title="title">
    <template v-slot:title>
      {{ title }}
    </template>
    <template v-slot:content>
      <slot name="form" v-bind="{ data: data, dialog: this, errors }">
        *** OVERRIDE: 'Form' slot ***
        <!--data: {{ data }}
        errors: {{ errors }} -->
      </slot>
    </template>
    <template v-slot:buttons>
      <slot :name="buttons" v-bind="{ modal: this }">
        <q-btn label="Submit" color="primary" @click="submit"/>
        <q-btn label="Cancel" color="negative" @click="close" />
      </slot>
    </template>
  </BaseDialog>
</template>

<script>
import BaseDialog from './BaseDialog.vue'
// import Vue from 'vue'
import _ from 'lodash'
export default {
  // props: ['title', 'onSuccess', 'onError', 'modelValue', 'apiUrl', 'apiMethod'],
  props: {
    title: String, apiUrl: String, apiMethod: String, onSuccess: Function, onError: Function, modelValue: { type: Object, default () { return {} } }
  },
  emits: ['update:modelValue'],
  data () {
    return {
      errors: {},
      data: this.modelValue
    }
  },
  methods: {
    open (data) {
      this.data = _.cloneDeep(data || this.modelValue)
      this.$refs.dialog.open()
    },
    close () {
      this.errors = {}
      this.$refs.dialog.close()
    },
    success (data) {
      if (this.onSuccess) {
        this.onSuccess(data)
      }
      this.close()
    },
    submit () {
      console.log('FormDialog submit', this.data, this.modelValue)
      this.$api[this.apiMethod.toLowerCase()](this.apiUrl, this.data)
        .then(response => {
          console.log('form dialog success', response.data)
          this.$emit('update:modelValue', response.data)
          this.errors = {}
          if (this.onSuccess) {
            this.onSuccess(response)
          }
          this.$refs.dialog.close()
        })
        .catch(error => {
          if (error.response && error.response.data) {
            this.errors = error.response.data
            console.log('errors', error.response.data, this.errors)
            if (this.onError) {
              this.onError(error)
            }
          }
        })
    }
  },
  // mounted: function () {
  //
  // },
  components: {
    BaseDialog
  }
}
</script>
