<!-- eslint-disable no-case-declarations -->
<template>
  <div>
    <!-- <HotTable :settings="settings"></HotTable> -->
    <!-- <q-select :value="value" :options="options" @change="handleChange" filter filter-placeholder="select"/> -->
    <q-dialog v-model="opened" @show="onShow" :content-css="{height: '90vh', minWidth: '120vw', minHeight: '90vh'}" ref="modal" no-backdrop-dismiss no-esc-dismiss :maximized="maximized">
      <q-card style="min-width:90vw">
        <q-bar class="bg-primary text-white">
          <q-toolbar>
            <q-avatar>
            </q-avatar>

            <q-toolbar-title>Samplesheet: {{type ? type.name : ''}} - {{rootNode.allChildrenCount}} samples
              <span class="float-right">
                <q-btn title="Maximize" dense flat icon="crop_square"  @click="maximized=true" v-if="!maximized"/>
                <q-btn title="Minimize" dense flat icon="maximize" @click="maximized=false" v-if="maximized"/>
              </span></q-toolbar-title>
          </q-toolbar>
        </q-bar>
        <q-card-section style="height:80vh; min-height:80vh;">
            <!-- {{type}} -->
            <q-btn
              color="primary"
              @click="show_help = true"
              label="Help"
              v-if="schema && schema.help"
            ><q-tooltip ref="tooltip">Please click "Help" button for important information on sample requirements!</q-tooltip></q-btn> <!-- icon="fas fa-question-circle" -->
            <q-checkbox v-model="showDescriptions" label="Show descriptions" class="show_descriptions" v-if="hasDescriptions"/> <q-checkbox v-model="showExamples" label="Show examples" v-if="allowExamples && this.sample_schema.examples && sample_schema.examples.length"  class="show_examples"/>
            <q-btn-dropdown label="Resize Columns">
            <q-list>
              <q-item @click="sizeToFit" clickable>
                <q-item-label>
                  Fit all columns
                </q-item-label>
              </q-item>
              <q-item @click="autoSizeAll" clickable>
                <q-item-label>
                  Auto-size
                </q-item-label>
              </q-item>
            </q-list>
          </q-btn-dropdown>
            <ag-grid-vue style="width: 100%; height: 90%;" class="ag-theme-balham"

              rowSelection='multiple'
              :enableColResize='true'
              :enableSorting='true'
              :gridOptions='gridOptions'
              :rowData='rowData'
              :columnDefs='columnDefs'
              :ref="'grid'"
              :pinnedTopRowData="getExampleRows"
              v-if="opened"
              @grid-ready="onGridReady"
              >
            </ag-grid-vue>
            <!-- domLayout='autoHeight' -->
        </q-card-section>
        <q-card-actions>
            <div v-if="editable">
              <q-btn-dropdown split label="Add row" @click="addRow(1)" color="positive">
                <q-list>
                  <q-item clickable v-close-popup @click="addRow(1)">
                    <q-item-label>
                      <q-item-section label>Add 1</q-item-section>
                    </q-item-label>
                  </q-item>
                  <q-item clickable v-close-popup @click="addRow(10)">
                    <q-item-label>
                      <q-item-section label>Add 10</q-item-section>
                    </q-item-label>
                  </q-item>
                  <q-item clickable v-close-popup @click="addRow(25)">
                    <q-item-label>
                      <q-item-section label>Add 25</q-item-section>
                    </q-item-label>
                  </q-item>
                  <q-item clickable v-close-popup @click="addRow(100)">
                    <q-item-label>
                      <q-item-section label>Add 100</q-item-section>
                    </q-item-label>
                  </q-item>
                </q-list>
              </q-btn-dropdown>
              <q-btn
                color="negative"
                label="Remove selected rows"
                @click="removeRows"
              />
              <q-btn
                v-if="validateUrl"
                label="Validate"
                @click="validate(false)"
              />
              <q-btn
                color="negative"
                label="Discard"
                @click="close"
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

          </div>
          <div v-else>
            <q-btn
              color="negative"
              label="Close"
              @click="close"
              class="float-right"
            />
          </div>
        </q-card-actions>
        <!-- <q-card-actions align="right" class="text-primary">
          <q-toolbar slot="footer">
            <q-toolbar-title v-if="editable">
              <q-btn-dropdown split label="Add row" @click="addRow(1)" color="positive">
                <q-list link>
                  <q-item v-close-popup @click.native="addRow(1)">
                    <q-item-main>
                      <q-item-tile label>Add 1</q-item-tile>
                    </q-item-main>
                  </q-item>
                  <q-item v-close-popup @click.native="addRow(10)">
                    <q-item-main>
                      <q-item-tile label>Add 10</q-item-tile>
                    </q-item-main>
                  </q-item>
                  <q-item v-close-popup @click.native="addRow(25)">
                    <q-item-main>
                      <q-item-tile label>Add 25</q-item-tile>
                    </q-item-main>
                  </q-item>
                  <q-item v-close-popup @click.native="addRow(100)">
                    <q-item-main>
                      <q-item-tile label>Add 100</q-item-tile>
                    </q-item-main>
                  </q-item>
                </q-list>
              </q-btn-dropdown>
              <q-btn
                color="negative"
                label="Remove selected rows"
                @click="removeRows"
              />
              <q-btn
                label="Validate"
                @click="validate(false)"
              />
              <q-btn
                color="negative"
                label="Discard"
                @click="close"
                class="float-right"
              />
              <q-btn
                color="positive"
                label="Save"
                @click="validate(true)"
                class="float-right"
              />
            </q-toolbar-title>
            <q-toolbar-title v-else>
              <q-btn
                color="negative"
                label="Close"
                @click="close"
                class="float-right"
              />
            </q-toolbar-title>
          </q-toolbar>
        </q-card-actions> -->
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

  </div>
</template>

<script>
// import { QSelect } from 'quasar'
import { AgGridVue } from 'ag-grid-vue3'
// import '../../node_modules/ag-grid-community/dist/styles/ag-grid.css'
// import '../../node_modules/ag-grid-community/dist/styles/ag-theme-balham.css'
import 'ag-grid-community/styles/ag-grid.css' // Core grid CSS, always needed
import 'ag-grid-community/styles/ag-theme-balham.css' // Optional theme CSS
import 'ag-grid-enterprise'
import NumericComponent from './editors/NumericComponent.vue'
// import DateComponent from './aggrid/DateComponent.vue'
// import AutocompleteComponent from './aggrid/editors/AutocompleteComponent.vue'
import BooleanComponent from './editors/BooleanComponent.vue'
import SelectComponent from './editors/SelectComponent.vue'
import GridComponent from './editors/GridComponent.vue'
import _ from 'lodash'
import sampleWidgetFactory from './widgets.js'
// import { ClipboardService } from '../../node_modules/ag-grid-enterprise/dist/lib/clipboardService.js'
// import axios from 'axios'
// var clipboardService = null

export default {
  name: 'AgSchema',
  props: ['modelValue', 'type', 'schema', 'editable', 'allowExamples', 'allowForceSave', 'submission', 'tableWarnings', 'tableErrors', 'admin', 'validateUrl'],
  data () {
    return {
      opened: false,
      show_help: false,
      showExamples: this.allowExamples,
      showDescriptions: true,
      // sample_schema: Object.freeze({}),
      rowData: [], // this.value,
      rootNode: {},
      // columnDefs: [],
      gridOptions: {
        enableRangeSelection: true,
        defaultColDef: {
          editable: this.cellEditable,
          // suppressSorting: true, // deprecated
          sortable: false, // newer version
          suppressMenu: true // let's keep it simple
        },
        getRowStyle: function (params) {
          if (params.node.rowPinned) {
            return { 'font-weight': 'bold' }
          }
        },
        getRowHeight: function (params) {
          // console.log('getRowHeight', params, params.node.rowPinned, params.data)
          if (params.node.rowPinned === 'top' && params.data && params.data._row_type === 'description') {
            return 75
          } else {
            return 25
          }
        },
        onPinnedRowDataChanged: this.expandDescriptionRow,
        onCellFocused: this.onCellFocused,
        // suppressMultiRangeSelection: true,
        // suppressRowClickSelection: true,
        // checkboxSelection: function () { return true },
        processCellFromClipboard (params) {
          switch (params.column.colDef.cellDataType) {
            case 'boolean':
              if (params.value === 'true' || params.value === 'True' || params.value === true) {
                return true
              }
              return false
            case 'numeric':
              return parseFloat(params.value)
            default:
              return params.value
          }
        },
        rowGroupPanelSuppressSort: true,
        rowSelection: 'multiple'
      },
      errors: {},
      warnings: {},
      maximized: true
    }
  },
  mounted () {
    console.log('mounted agschema')
  },
  created () {
    console.log('created agschema')
  },
  unmounted () {
    console.log('destroyed agschema')
  },
  methods: {
    onGridReady (params) {
      this.gridApi = params.api
      this.columnApi = params.columnApi
      this.rootNode = this.gridApi.getModel().rootNode
      console.log('gridApi', this.gridApi)
    },
    getValidationObject (validation) {
      // validation errors or warnings could be a list mixed strings and objects, we only want the object
      if (typeof validation === 'object' && !Array.isArray(validation)) {
        return validation
      } else if (Array.isArray(validation)) {
        for (const i in validation) {
          if (typeof validation[i] === 'object' && !Array.isArray(validation[i])) {
            return validation[i]
          }
        }
      }
      return {}
    },
    openSamplesheet () {
      console.log('openSamplesheet!!!', this.type, this.value)
      // var self = this
      // if (this.submission && this.submission.data) {
      //   this.errors = this.submission.data.errors && this.submission.data.errors.sample_data ? this.submission.data.errors.sample_data : {}
      //   this.warnings = this.submission.data.warnings && this.submission.data.warnings.sample_data ? this.submission.data.warnings.sample_data : {}
      // }
      // console.log('warnings', this.warnings)
      this.warnings = this.tableWarnings ? _.cloneDeep(this.getValidationObject(this.tableWarnings)) : {}
      this.errors = this.tableErrors ? _.cloneDeep(this.getValidationObject(this.tableErrors)) : {}
      console.log('Samplesheet errors, warnings', this.warnings, this.errors)
      if (this.value && this.value.length > 0) {
        this.rowData = _.cloneDeep(this.value)
      } else {
        this.rowData = _.times(10, _.stubObject)
      }

      // if (!this.type || !this.type.sample_schema) {
      //   this.$q.dialog({
      //     title: 'Alert',
      //     message: 'Please select a submission type first.'
      //   })
      //   return
      // }
      // this.sample_schema = this.schema || this.type.sample_schema
      this._columnDefs = this.schema2Columns(this.sample_schema)
      // console.log('openSamplesheet', this.rowData, this.value, this.columnDefs)
      // console.log('agschema refs', this.$refs)
      this.$refs.modal.show()
      // .then(() => {
      //   if (self.rowData.length === 0) {
      //     self.addRow()
      //   }
      //   this.rootNode = this.gridOptions.api.getModel().rootNode
      //   setTimeout(function () {
      //     self.$refs.tooltip.show()
      //   }, 1000)
      //   setTimeout(function () {
      //     self.$refs.tooltip.hide()
      //   }, 6000)
      // })
    },
    onShow () {
      // var self = this
      if (this.rowData.length === 0) {
        this.addRow()
      }
      console.log('gridOptions', this.gridOptions.api)
      // this.rootNode = this.gridOptions.api.getModel().rootNode
    },
    cellEditable (params) {
      // console.log('cellEditable', this.editable, params)
      if (params.node.rowPinned === 'top') {
        this.$q.notify({ position: 'top', message: 'Description and example rows are not editable.  Please use the "Add row" button for editable rows.' })
        return false
      }
      return this.editable
    },
    onCellFocused (params) {
      if (this.dismiss) {
        this.dismiss()
      }
      if (params.column) {
        const errors = this.getCellErrors(params.rowIndex, params.column.colDef.field)
        if (errors) {
          this.dismiss = this.$q.notify({ position: 'top', message: `Error at Row ${params.rowIndex + 1}, Column "${params.column.colDef.headerName}": ` + errors.join(', ') })
        } else {
          const warnings = this.getCellWarnings(params.rowIndex, params.column.colDef.field)
          if (warnings) {
            this.dismiss = this.$q.notify({ position: 'top', color: 'warning', message: `Warning at Row ${params.rowIndex + 1}, Column "${params.column.colDef.headerName}": ` + warnings.join(', ') })
          }
        }
      }
    },
    sizeToFit () {
      this.gridOptions.api.sizeColumnsToFit()
    },
    autoSizeAll () {
      const allColIds = this.gridOptions.columnApi.getAllColumns().map(column => column.colId)
      this.gridOptions.columnApi.autoSizeColumns(allColIds)
    },
    // rowIndex (params) {
    //   return params.node.rowIndex + 1
    // },
    schema2Columns (schema) {
      console.log('schema2Columns', schema.properties)
      const columnDefs = []
      let col = null
      // var columnDefs = [{ headerName: '', lockPosition: true, valueGetter: this.rowIndex, cellClass: 'locked-col', width: 60, suppressNavigable: true, pinned: 'left' }]
      const order = schema.order || Object.keys(schema.properties).array
      order.forEach(prop => {
        if (schema.properties[prop].type === 'object') {
          // Supported nested properties
          const objschema = schema.properties[prop]
          const order = objschema.order || Object.keys(objschema.properties).array
          order.forEach(nestedProp => {
            if (this.editable || this.admin || !objschema.properties[nestedProp].internal) { // (!this.editable || this.$store.getters.isStaff || !schema.properties[prop].internal)
              col = this.getColDef(`${prop}.${nestedProp}`, objschema.properties[nestedProp], objschema)
              columnDefs.push(col)
            }
          })
        } else if (this.editable || this.admin || !schema.properties[prop].internal) { // (!this.editable || this.$store.getters.isStaff || !schema.properties[prop].internal)
          col = this.getColDef(prop, schema.properties[prop], schema)
          columnDefs.push(col)
        }
      })

      if (this.editable) {
        columnDefs[0].headerCheckboxSelection = true
        columnDefs[0].headerCheckboxSelectionFilteredOnly = true
        columnDefs[0].checkboxSelection = true
      }
      columnDefs.push({ field: '_row_type', hide: true })
      console.log('columnDefs', columnDefs)
      return columnDefs
    },
    getColDescriptions (schema) {
      // console.log('getColDescriptions', schema)
      const descriptions = {}
      Object.keys(schema.properties).forEach(prop => {
        descriptions[prop] = schema.properties[prop].description
      })
      // for (const prop in schema.properties) {
      //   if (schema.properties.hasOwn(prop)) {
      //     descriptions[prop] = schema.properties[prop].description
      //   }
      // }
      // console.log('descriptions', descriptions)
      return descriptions
    },
    getCellErrors (row, field) {
      if (this.errors[row] && this.errors[row][field]) {
        if (this.sample_schema.properties[field].error_message) {
          return [this.sample_schema.properties[field].error_message]
        } else {
          return this.errors[row][field]
        }
      } else {
        return null
      }
    },
    getCellWarnings (row, field) {
      if (this.warnings[row] && this.warnings[row][field]) {
        if (this.sample_schema.properties[field].error_message) {
          return [this.sample_schema.properties[field].error_message]
        } else {
          return this.warnings[row][field]
        }
      } else {
        return null
      }
    },
    getColDef (id, definition, schema) {
      console.log('getColDef', definition, schema)
      const self = this
      function cellClass (params) {
        // console.log('cellClass', params, self.errors)
        if (params.node.rowPinned) {
          if (params.data._row_type === 'description') {
            return ['description']
          } else {
            return ['example']
          }
        } else if (self.errors[params.rowIndex] && self.errors[params.rowIndex][params.colDef.field]) {
          return ['error']
        } else if (self.warnings[params.rowIndex] && self.warnings[params.rowIndex][params.colDef.field]) {
          return ['warning']
        }
        return []
      }
      let header = id
      if (definition.title) {
        header = definition.title
      }
      if (schema.required && schema.required.indexOf(id) !== -1) {
        header = '*' + header
      }
      function cellTooltip (params) {
        // console.log('cellTooltip', params)
        if (params.data._row_type === 'description' || params.data._row_type === 'example') {
          return 'Descriptions and examples cannot be modified.  Please use blank rows for user data.' // params.value
        }
        const errors = self.getCellErrors(params.rowIndex, params.colDef.field)
        const warnings = self.getCellWarnings(params.rowIndex, params.colDef.field)
        const text = `row ${params.rowIndex + 1}, ${header}`
        if (errors) {
          return text + ': ' + errors.join(', ')
        } else if (warnings) {
          return text + ': ' + warnings.join(', ')
        }
        return params.value ? text + ': ' + params.value : text
      }
      // console.log('definition', id, definition, schema)
      // var header = id
      let tooltip = null
      // if (definition.title) {
      //   header = definition.title
      // }
      // if (schema.required && schema.required.indexOf(id) !== -1) {
      //   header = '*' + header
      // }
      if (definition.description) {
        tooltip = definition.description
      }
      let WidgetClass = null
      if (definition.widget && definition.widget.type) {
        // console.log('getcolwidget', definition.widget, definition.widget.type)
        WidgetClass = sampleWidgetFactory.getWidget(definition.widget.type)
      }
      // console.log('widget', definition, WidgetClass)
      // console.log('factory', sampleWidgetFactory)
      let options = null, def = null
      if (WidgetClass) {
        // console.log('WidgetClass', definition.widget.options)
        options = definition.widget.options
        // options._schema = JSON.parse(JSON.stringify(schema))
        // Object.freeze(options)
        const widget = new WidgetClass(id, options)
        return { headerName: header, headerTooltip: tooltip, field: id, cellEditor: WidgetClass.component, cellEditorParams: { definition, widget_options: widget.getOptions() }, cellClass, tooltipValueGetter: cellTooltip, pinned: definition.pinned } // values: definition.enum, widget: definition.widget,
      }
      switch (definition.type) {
        case 'table':
          // console.log('object', definition)
          // var _options = JSON.parse(JSON.stringify(definition.widget.options))
          // const _options = { _schema: JSON.parse(JSON.stringify(definition.schema)) }
          Object.freeze(options)
          // var widget = new WidgetClass(id, options)
          return { headerName: header, headerTooltip: tooltip, field: id, cellEditor: GridComponent, cellEditorParams: { definition, widget_options: { _schema: JSON.parse(JSON.stringify(definition.schema)) } }, cellClass, tooltipValueGetter: cellTooltip, pinned: definition.pinned }
        case 'string':
          if (definition.enum) {
            // console.log('enum', {headerName: header, headerTooltip: tooltip, field: id, cellEditor: SelectComponent, cellEditorParams: {definition: definition, widget_options: {multiple: definition.multiple}}, cellClass: cellClass, tooltip: cellTooltip, pinned: definition.pinned})
            // return {headerName: header, headerTooltip: tooltip, field: id, cellEditor: AutocompleteComponent, cellEditorParams: {values: definition.enum, widget: definition.widget, definition: definition}, cellClass: cellClass, tooltip: cellTooltip, pinned: definition.pinned} // cellEditor: 'agRichSelectCellEditor', cellEditorParams: {values: definition.enum}
            // return {headerName: header, headerTooltip: tooltip, field: id, cellEditor: 'agRichSelectCellEditor', cellEditorParams: {values: definition.enum}, cellClass: cellClass, tooltip: cellTooltip, pinned: definition.pinned} // cellEditor: 'agRichSelectCellEditor', cellEditorParams: {values: definition.enum} // cellEditor: AutocompleteComponent
            return { headerName: header, headerTooltip: tooltip, field: id, cellEditor: SelectComponent, cellEditorParams: { definition, widget_options: { multiple: definition.multiple } }, cellClass, tooltipValueGetter: cellTooltip, pinned: definition.pinned }
          } else {
            return { headerName: header, headerTooltip: tooltip, field: id, cellDataType: 'text', cellClass, tooltipValueGetter: cellTooltip, pinned: definition.pinned }
          }
        case 'number':
          return { headerName: header, headerTooltip: tooltip, field: id, cellEditor: NumericComponent, cellClass, tooltipValueGetter: cellTooltip, cellDataType: 'number', pinned: definition.pinned }
        case 'boolean':
          return { headerName: header, headerTooltip: tooltip, field: id, cellEditor: BooleanComponent, cellClass, tooltipValueGetter: cellTooltip, cellDataType: 'boolean', pinned: definition.pinned }
        case 'array':
          def = { headerName: header, field: id, cellClass, tooltipValueGetter: cellTooltip, pinned: definition.pinned }
          if (definition.items && definition.items.enum) {
            def.source = definition.items.enum
          }
          return def
        default:
          // console.log(id,definition);
          throw new Error('Unsupported type ' + definition.type)
      }
    },
    save () {
      this.$emit('input', this.getRowData(false))
      this.$emit('update:modelValue', this.getRowData(false))
      this.$emit('warnings', this.warnings)
      this.$emit('errors', this.errors)
      this.close()
    },
    validate (save) {
      // this.hst.validateTable(true)
      console.log('validate', this.type, this.sample_schema, save)
      const self = this
      // this.$axios.post('/api/submission_types/' + this.type.id + '/validate_data/', {data: this.getRowData(true)})
      this.$axios.post(this.validateUrl, { sample_schema: this.sample_schema, data: this.getRowData(true) })
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
    },
    getRowData (filterAndSort) {
      const data = []
      const method = filterAndSort ? 'forEachNodeAfterFilterAndSort' : 'forEachNode'
      if (!this.gridOptions.api) {
        return []
      }
      this.gridOptions.api[method](function (node) {
        data.push(node.data)
      })
      const self = this, cleaned = []
      let take = false
      _.forEachRight(data, function (row) {
        if (take) {
          cleaned.unshift(row)
        } else if (!self.rowIsEmpty(row)) {
          take = true
          cleaned.unshift(row)
        }
      })
      // console.log('getRowData', data, cleaned)
      return cleaned
    },
    rowIsEmpty (row) {
      return !_.values(row).some(x => x !== undefined && x !== '')
    },
    addRow (number) {
      const rows = []
      for (let i = 0; i < number; i++) {
        rows.push({})
      }
      this.gridOptions.api.applyTransaction({ add: rows })
      // console.log('addRow', this.getRowData())
    },
    removeRows () {
      const selectedData = this.gridOptions.api.getSelectedRows()
      this.gridOptions.api.applyTransaction({ remove: selectedData })
      // this.errors = {}
      this.gridOptions.api.redrawRows()
      // this.validate(false)
    },
    close () {
      this.$refs.modal.hide()
    },
    modalOpened () {
      console.log('modal opened')
    }// ,
    // expandDescriptionRow (params) {
    //   console.log('expandDescriptionRow', params, params.api, params.api.getPinnedTopRow(0)) //
    //   params.api.getPinnedTopRow(0).isDescription = true
    //   params.api.onRowHeightChanged()
    // }
    // ,
    // beforeMount () {
    //   this.gridOptions.numericComponentFramework = NumericComponent
    // }
  },
  computed: {
    value () {
      return this.modelValue
    },
    sample_schema () {
      console.log('sample_schema', this.schema)
      return this.schema ? this.schema : this.type.sample_schema
    },
    columnDefs () {
      return this._columnDefs ? this._columnDefs : []
    },
    hasErrors () {
      // console.log('hasErrors', this.errors)
      return this.errors && _.size(this.errors) > 0
    },
    hasWarnings () {
      // console.log('hasWarnings', this.warnings)
      return this.warnings && _.size(this.warnings) > 0
    },
    sampleCount () {
      if (this.gridOptions.api) {
        return this.gridOptions.api.getModel().rootNode.allChildrenCount
      }
      return 0
      // return this.getRowData().length
    },
    hasDescriptions () {
      for (const prop in this.sample_schema.properties) {
        // if (this.sample_schema.properties.hasOwn(prop)) {
        if (this.sample_schema.properties[prop].description) {
          return true
        }
        // }
      }
      return false
    },
    getExampleRows () {
      const examples = []
      if (this.showDescriptions && this.hasDescriptions) {
        const descriptions = this.getColDescriptions(this.sample_schema)
        descriptions._row_type = 'description'
        examples.push(descriptions)
      }
      if (this.showExamples) {
        for (const i in this.sample_schema.examples) {
          const example = this.sample_schema.examples[i]
          example._row_type = 'example'
          examples.push(example)
        }
        // examples = examples.concat(this.sample_schema.examples)
      }
      // console.log('examples', examples)
      return examples
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
