<!-- eslint-disable no-case-declarations -->
<template>
  <div style="width: 100%; height: 500px;">
  <p>editable: {{ editable }}</p>
  <p>modelValue: {{ modelValue }}</p>
            <ag-grid-vue style="width: 100%; height: 90%;" class="ag-theme-balham"

              rowSelection='multiple'
              :enableColResize='true'
              :enableSorting='true'
              :gridOptions='gridOptions'
              :rowData='rowData'
              :columnDefs='columnDefs'
              ref="grid"
              :pinnedTopRowData="exampleRows"
              v-if="columnDefs.length > 0"
              @grid-ready="onGridReady"
              >
            </ag-grid-vue>
  columnDefs: {{ columnDefs }}
  <q-btn label="add row" @click="agutil.addRow(5)"/>
  </div>
</template>

<script>
// import { QSelect } from 'quasar'
import { AgGridVue } from 'ag-grid-vue3'
// import '../../node_modules/ag-grid-community/dist/styles/ag-grid.css'
// import '../../node_modules/ag-grid-community/dist/styles/ag-theme-balham.css'
import 'ag-grid-community/styles/ag-grid.css' // Core grid CSS, always needed
import 'ag-grid-community/styles/ag-theme-alpine.css' // Optional theme CSS
import 'ag-grid-enterprise'
import NumericComponent from './editors/NumericComponent.vue'
// import DateComponent from './aggrid/DateComponent.vue'
// import AutocompleteComponent from './aggrid/editors/AutocompleteComponent.vue'
import BooleanComponent from './editors/BooleanComponent.vue'
import SelectComponent from './editors/SelectComponent.vue'
import GridComponent from './editors/GridComponent.vue'
import _ from 'lodash'
import sampleWidgetFactory from './widgets.js'
import AgUtil from './agutil'
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
      // schema: Object.freeze({}),
      rowData: [], // this.value,
      rootNode: {},
      columnDefs: [],
      exampleRows: [],
      gridOptions: {},
      //   enableRangeSelection: true,
      //   defaultColDef: {
      //     editable: this.cellEditable,
      //     // suppressSorting: true, // deprecated
      //     sortable: false, // newer version
      //     suppressMenu: true // let's keep it simple
      //   },
      //   getRowStyle: function (params) {
      //     if (params.node.rowPinned) {
      //       return { 'font-weight': 'bold' }
      //     }
      //   },
      //   getRowHeight: function (params) {
      //     // console.log('getRowHeight', params, params.node.rowPinned, params.data)
      //     if (params.node.rowPinned === 'top' && params.data && params.data._row_type === 'description') {
      //       return 75
      //     } else {
      //       return 25
      //     }
      //   },
      //   onPinnedRowDataChanged: this.expandDescriptionRow,
      //   onCellFocused: this.onCellFocused,
      //   // suppressMultiRangeSelection: true,
      //   // suppressRowClickSelection: true,
      //   // checkboxSelection: function () { return true },
      //   processCellFromClipboard (params) {
      //     switch (params.column.colDef.cellDataType) {
      //       case 'boolean':
      //         if (params.value === 'true' || params.value === 'True' || params.value === true) {
      //           return true
      //         }
      //         return false
      //       case 'numeric':
      //         return parseFloat(params.value)
      //       default:
      //         return params.value
      //     }
      //   },
      //   rowGroupPanelSuppressSort: true,
      //   rowSelection: 'multiple'
      // },
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
    setupGrid () {
      this.warnings = this.tableWarnings ? _.cloneDeep(this.agutil.getValidationObject(this.tableWarnings)) : {}
      this.errors = this.tableErrors ? _.cloneDeep(this.agutil.getValidationObject(this.tableErrors)) : {}
      if (this.value && this.value.length > 0) {
        this.rowData = _.cloneDeep(this.value)
      } else {
        this.rowData = _.times(10, _.stubObject)
      }
      this.gridOptions = this.agutil.getGridOptions()
      this.columnDefs = this.agutil.schema2Columns(this.schema)
    },
    onGridReady (params) {
      alert('grid ready!')
      this.agutil.onGridReady(params)
      this.gridApi = params.api
      this.columnApi = params.columnApi
      this.rootNode = this.gridApi.getModel().rootNode
      this.exampleRows = this.agutil.getExampleRows()
      console.log('gridApi', this.gridApi)
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
    // schema2Columns (schema) {
    //   return this.agutil.schema2Columns(schema)
    // console.log('schema2Columns', schema.properties)
    // const columnDefs = []
    // let col = null
    // // var columnDefs = [{ headerName: '', lockPosition: true, valueGetter: this.rowIndex, cellClass: 'locked-col', width: 60, suppressNavigable: true, pinned: 'left' }]
    // const order = schema.order || Object.keys(schema.properties).array
    // order.forEach(prop => {
    //   if (schema.properties[prop].type === 'object') {
    //     // Supported nested properties
    //     const objschema = schema.properties[prop]
    //     const order = objschema.order || Object.keys(objschema.properties).array
    //     order.forEach(nestedProp => {
    //       if (this.editable || this.admin || !objschema.properties[nestedProp].internal) { // (!this.editable || this.$store.getters.isStaff || !schema.properties[prop].internal)
    //         col = this.getColDef(`${prop}.${nestedProp}`, objschema.properties[nestedProp], objschema)
    //         columnDefs.push(col)
    //       }
    //     })
    //   } else if (this.editable || this.admin || !schema.properties[prop].internal) { // (!this.editable || this.$store.getters.isStaff || !schema.properties[prop].internal)
    //     col = this.getColDef(prop, schema.properties[prop], schema)
    //     columnDefs.push(col)
    //   }
    // })

    // if (this.editable) {
    //   columnDefs[0].headerCheckboxSelection = true
    //   columnDefs[0].headerCheckboxSelectionFilteredOnly = true
    //   columnDefs[0].checkboxSelection = true
    // }
    // columnDefs.push({ field: '_row_type', hide: true })
    // console.log('columnDefs', columnDefs)
    // return columnDefs
    // },
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
        if (this.schema.properties[field].error_message) {
          return [this.schema.properties[field].error_message]
        } else {
          return this.errors[row][field]
        }
      } else {
        return null
      }
    },
    getCellWarnings (row, field) {
      if (this.warnings[row] && this.warnings[row][field]) {
        if (this.schema.properties[field].error_message) {
          return [this.schema.properties[field].error_message]
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
      console.log('validate', this.type, this.schema, save)
      const self = this
      // this.$axios.post('/api/submission_types/' + this.type.id + '/validate_data/', {data: this.getRowData(true)})
      this.$axios.post(this.validateUrl, { schema: this.schema, data: this.getRowData(true) })
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
    // addRow (number) {
    //   const rows = []
    //   for (let i = 0; i < number; i++) {
    //     rows.push({})
    //   }
    //   this.gridOptions.api.applyTransaction({ add: rows })
    //   // console.log('addRow', this.getRowData())
    // },
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
    sampleCount () {
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
