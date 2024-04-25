<!-- eslint-disable no-case-declarations -->
<template>
  <div>
    <q-dialog v-model="opened" @show="onShow" :content-css="{height: '90vh', minWidth: '120vw', minHeight: '90vh'}" ref="modal" no-backdrop-dismiss no-esc-dismiss :maximized="maximized">
      <q-card style="min-width:90vw">
        <q-bar class="bg-primary text-white">
          <q-toolbar>
            <q-avatar>
            </q-avatar>

            <q-toolbar-title>{{type ? type.name : 'Rows'}} -
              <span class="float-right">
                <q-btn title="Maximize" dense flat icon="crop_square"  @click="maximized=true" v-if="!maximized"/>
                <q-btn title="Minimize" dense flat icon="maximize" @click="maximized=false" v-if="maximized"/>
              </span></q-toolbar-title>
          </q-toolbar>
        </q-bar>
        <aggrid
              v-if="opened"
              :model-value="modelValue"
              :type="type"
              :schema="schema"
              :editable="editable"
              :allow-examples="allowExamples"
              :allow-force-save="allowForceSave"
              :table-warnings="tableWarnings"
              :tableErrors="tableErrors"
              :admin="admin"
              :validate-url="validateUrl"
              :on-save="save"
              ref="grid"
              >
                <template v-slot:postButtons>
                  <q-btn
                    color="primary"
                    @click="show_help = true"
                    label="Help"
                    v-if="schema && schema.help"
                  />
                  <q-btn
                    v-if="editable"
                    color="negative"
                    label="Dismiss"
                    @click="close"
                    class="float-right"
                  />
                  <q-btn
                    v-else
                    color="negative"
                    label="Close"
                    @click="close"
                    class="float-right"
                  />
              </template>
      </aggrid>
      </q-card>
    </q-dialog>

    <q-dialog v-model="show_help">
      <q-card>
        <q-toolbar>
          Help
        </q-toolbar>

        <q-card-section>
          <div v-html="schema.help" v-if="schema && schema.help"></div>
        </q-card-section>
        <q-card-actions align="right" class="text-primary">
          <q-btn
            color="primary"
            @click="show_help = false"
            label="Close"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-btn label="Open Dialog" @click="openDialog"/>
  </div>
</template>

<script>
// import { QSelect } from 'quasar'
import aggrid from './aggrid.vue'

export default {
  name: 'AgSchema',
  props: ['modelValue', 'schema', 'editable', 'allowExamples', 'allowForceSave', 'tableWarnings', 'tableErrors', 'admin', 'validateUrl'],
  emits: ['update:modelValue'],
  data () {
    return {
      opened: false,
      show_help: false,
      maximized: true
    }
  },
  mounted () {
    console.log('mounted dialog')
  },
  created () {
    console.log('created dialog')
  },
  unmounted () {
    console.log('destroyed dialog')
  },
  methods: {
    openDialog () {
      console.log('openDialog!!!', this.type, this.value)
      this.$refs.modal.show()
    },
    onShow () {
      console.log('onShow')
    },
    save (data) {
      this.$emit('update:modelValue', data)
      // this.$emit('input', this.getRowData(false))
      // this.$emit('update:modelValue', this.getRowData(false))
      // this.$emit('warnings', this.warnings)
      // this.$emit('errors', this.errors)
      this.close()
    },
    close () {
      this.$refs.modal.hide()
    },
    modalOpened () {
      console.log('modal opened')
    }
  },
  computed: {
    grid () {
      return this.$refs.grid
    }
  },
  components: {
    aggrid
  },
  watch: {
  }
}

</script>
