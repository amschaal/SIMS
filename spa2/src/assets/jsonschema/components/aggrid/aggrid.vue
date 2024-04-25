<!-- eslint-disable no-case-declarations -->
<template>
  <div class="ag-theme-balham">
    <!-- <p>exampleRows: {{ example }}</p> -->
  <!-- <p>editable: {{ editable }}</p> -->
  <!-- <p>modelValue: {{ modelValue }}</p> -->
  <slot>
    <q-card style="min-width:90vw">
  <q-card-section style="height:80vh; min-height:80vh;">
    <slot name="grid">
              <ag-grid-vue style="width: 100%; height: 90%;" class="ag-theme-balham"

                rowSelection='multiple'
                :enableColResize='true'
                :enableSorting='true'
                :gridOptions='gridOptions'
                :rowData='rowData'
                :columnDefs='columnDefs'
                :pinnedTopRowData="exampleRows"
                v-if="columnDefs.length > 0"
                @grid-ready="onGridReady"
                >
              </ag-grid-vue>
    </slot>
  </q-card-section>
    <q-card-actions>
    <slot name="preButtons"></slot>
    <slot name="buttons">
      <q-btn-dropdown label="Format" >
          <q-list>
            <q-item clickable v-close-popup @click="agutil.sizeToFit()">
              <q-item-section>
                <q-item-label>Maximize Columns</q-item-label>
              </q-item-section>
            </q-item>
            <q-item clickable v-close-popup @click="agutil.autoSizeAll()">
              <q-item-section>
                <q-item-label>Fit to columns</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
        <q-card-actions v-if="editable">
          <q-btn-dropdown split label="Add row" @click="agutil.addRow(1)" color="positive">
            <q-list>
              <q-item clickable v-close-popup @click="agutil.addRow(1)">
                <q-item-label>
                  <q-item-section label>Add 1</q-item-section>
                </q-item-label>
              </q-item>
              <q-item clickable v-close-popup @click="agutil.addRow(10)">
                <q-item-label>
                  <q-item-section label>Add 10</q-item-section>
                </q-item-label>
              </q-item>
              <q-item clickable v-close-popup @click="agutil.addRow(25)">
                <q-item-label>
                  <q-item-section label>Add 25</q-item-section>
                </q-item-label>
              </q-item>
              <q-item clickable v-close-popup @click="agutil.addRow(100)">
                <q-item-label>
                  <q-item-section label>Add 100</q-item-section>
                </q-item-label>
              </q-item>
            </q-list>
          </q-btn-dropdown>
          <q-btn
            color="negative"
            label="Remove selected rows"
            @click="agutil.removeRows()"
          />
          <q-btn
            v-if="validateUrl"
            label="Validate"
            @click="validate(false)"
          />
          <q-btn
            color="negative"
            label="Discard"
            @click="setupData"
            class="float-right"
          />
          <q-btn
            v-if="validateUrl"
            color="positive"
            label="Save"
            @click="validate(true)"
            class="float-right"
          />
          <q-btn
            v-else
            color="positive"
            label="Save"
            @click="save()"
            class="float-right"
          />

      </q-card-actions>
      <q-card-actions v-else>
        <q-btn
          color="negative"
          label="Close"
          @click="close"
          class="float-right"
        />
      </q-card-actions>
      <!-- <q-btn label="add row" @click="agutil.addRow(5)"/>
      <q-btn label="remove rows" @click="agutil.removeRows()"/> -->
      <!-- <q-btn label="logData" @click="console.log(agutil.getRowData())"/>
      <q-btn label="getFlattenedProperties" @click="console.log(agutil.getFlattenedProperties())"/> -->
    </slot>
    <slot name="postButtons"></slot>
    </q-card-actions>
  </q-card>
  </slot>
  </div>
</template>

<script>
import { AgGridVue } from 'ag-grid-vue3'
import 'ag-grid-community/styles/ag-grid.css' // Core grid CSS, always needed
import 'ag-grid-community/styles/ag-theme-balham.css' // Optional theme CSS
// import 'ag-grid-community/styles/ag-theme-material.css'
import 'ag-grid-enterprise'
import _ from 'lodash'
import AgUtil from './agutil'
// import { ClipboardService } from '../../node_modules/ag-grid-enterprise/dist/lib/clipboardService.js'
// import axios from 'axios'
// var clipboardService = null

export default {
  name: 'AgSchema',
  props: ['modelValue', 'schema', 'editable', 'allowExamples', 'allowForceSave', 'tableWarnings', 'tableErrors', 'admin', 'validateUrl', 'onSave'],
  emits: ['update:modelValue'],
  data () {
    return {
      opened: false,
      show_help: false,
      // schema: Object.freeze({}),
      rowData: [], // this.value,
      rootNode: {},
      columnDefs: [],
      exampleRows: [],
      gridOptions: {},
      errors: {},
      warnings: {},
      maximized: true
    }
  },
  mounted () {
    console.log('mounted agschema')
    this.agutil = new AgUtil(this.schema,
      {
        admin: this.admin,
        editable: this.editable,
        showExamples: this.allowExamples,
        showDescriptions: true
      },
      this)
    this.setupGrid()
  },
  created () {
    console.log('created agschema')
  },
  unmounted () {
    console.log('destroyed agschema')
  },
  methods: {
    setupData () {
      this.warnings = this.tableWarnings ? _.cloneDeep(this.agutil.getValidationObject(this.tableWarnings)) : {}
      this.errors = this.tableErrors ? _.cloneDeep(this.agutil.getValidationObject(this.tableErrors)) : {}
      if (this.value && this.value.length > 0) {
        this.rowData = _.cloneDeep(this.value)
      } else {
        this.rowData = _.times(10, _.stubObject)
      }
    },
    setupGrid () {
      this.setupData()
      this.gridOptions = this.agutil.getGridOptions()
      this.columnDefs = this.agutil.schema2Columns(this.schema)
    },
    onGridReady (params) {
      // alert('grid ready!')
      this.agutil.onGridReady(params)
      this.gridApi = params.api
      this.columnApi = params.columnApi
      this.rootNode = this.gridApi.getModel().rootNode
      this.exampleRows = this.agutil.getExampleRows()
      console.log('gridApi', this.gridApi)
    },
    save () {
      const data = this.agutil.getRowData(false)
      console.log('save', data)
      this.$emit('input', data)
      this.$emit('update:modelValue', data)
      this.$emit('warnings', this.warnings)
      this.$emit('errors', this.errors)
      if (this.onSave) {
        this.onSave(data)
      }
      // this.close()
    },
    validate (save) {
      // this.hst.validateTable(true)
      console.log('validate', this.type, this.schema, save)
      const self = this
      // this.$axios.post('/api/submission_types/' + this.type.id + '/validate_data/', {data: this.getRowData(true)})
      this.$axios.post(this.validateUrl, { schema: this.schema, data: this.agutil.getRowData(true) })
        .then(function (response) {
          // console.log(response)
          self.errors = {}
          self.warnings = {}
          self.gridOptions.api.redrawRows() // redrawCells({force: true})
          self.$q.notify({ message: 'Successfully validated.  Please hit the SUBMIT button when ready to save your changes.', type: 'positive' })
          if (save) {
            self.save()
          }
        })
        .catch(function (error, stuff) {
          console.log('ERROR', error.response, self.$refs.grid, self.gridOptions.api.refreshCells)
          if (!error.response.data || (!error.response.data.errors && !error.response.data.warnings)) {
            self.$q.notify({ message: 'A server error occurred.', type: 'negative' })
            return
          }
          self.errors = error.response.data.errors
          self.warnings = error.response.data.warnings
          self.gridOptions.api.redrawRows() // redrawCells({force: true})
          if (!save || !self.allowForceSave) {
            if (self.hasErrors) {
              self.$q.notify({ message: 'There were errors in your data.', type: 'negative' })
            }
            if (self.hasWarnings) {
              self.$q.notify({ message: 'There were warnings in your data.', type: 'warning' })
            }
          } else {
            const message = self.hasErrors ? 'There were errors.  Any errors will need to be corrected before completing submission.  You may choose to "save anyway" and then save this submission as a draft in order not to lose your work.' : 'There were warnings.  To ignore the warnings, click "save anyway".'
            self.$q.notify({
              message,
              timeout: 10000, // in milliseconds; 0 means no timeout
              type: self.hasErrors ? 'negative' : 'warning',
              // position: 'bottom', // 'top', 'left', 'bottom-left' etc.
              actions: [
                {
                  label: 'Save Anyway',
                  handler: () => {
                    self.save()
                  }
                }
              ]
            })
          }

          // if (error.response) {
          //   self.errors = error.response.data.errors
          // }
        })
    }
  },
  computed: {
    value () {
      return this.modelValue
    },
    // schema () {
    //   console.log('schema', this.schema)
    //   return this.schema ? this.schema : this.type.schema
    // },
    // columnDefs () {
    //   return this._columnDefs
    // },
    hasErrors () {
      // console.log('hasErrors', this.errors)
      return this.errors && _.size(this.errors) > 0
    },
    hasWarnings () {
      // console.log('hasWarnings', this.warnings)
      return this.warnings && _.size(this.warnings) > 0
    },
    rowCount () {
      if (this.gridOptions.api) {
        return this.gridOptions.api.getModel().rootNode.allChildrenCount
      }
      return 0
      // return this.getRowData().length
    }
  },
  components: {
    // QSelect,
    AgGridVue
  },
  watch: {
  }
}

</script>

<style>
  .ag-row .error {
    background-color: pink;
  }
  .ag-row .warning {
    background-color: #ffda85;
  }
  .ag-row .example, .show_examples span {
    background-color: lightgreen !important;
  }
  .ag-row .description, .show_descriptions span {
    background-color: lightgrey !important;
    white-space: normal;
  }
  .ag-theme-balham .ag-row-odd:not(.ag-row-selected) {
    background-color: #fafafa;
  }
  .ag-theme-balham .ag-cell {
    border-right: 1px solid #BDC3C7;
  }
  .ag-theme-balham .ag-ltr .ag-cell {
    border-right: 1px solid #BDC3C7;
  }
  /* .ag-watermark {
    display: none !important;
  } */
</style>
