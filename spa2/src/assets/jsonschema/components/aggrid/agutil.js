import _ from 'lodash'
import sampleWidgetFactory from './widgets.js'
import NumericComponent from './editors/NumericComponent.vue'
// import DateComponent from './aggrid/DateComponent.vue'
// import AutocompleteComponent from './aggrid/editors/AutocompleteComponent.vue'
import BooleanComponent from './editors/BooleanComponent.vue'
import SelectComponent from './editors/SelectComponent.vue'
import GridComponent from './editors/GridComponent.vue'

class AgUtil {
  constructor (schema, props, component) {
    this.schema = schema
    this.props = props
    this.component = component
    this.errors = component.errors
    this.warnings = component.warnings
  }

  onGridReady (params) {
    this.gridApi = params.api
    this.columnApi = params.columnApi
    this.rootNode = this.gridApi.getModel().rootNode
  }

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
          if (this.props.editable || this.props.admin || !objschema.properties[nestedProp].internal) { // (!this.editable || this.$store.getters.isStaff || !schema.properties[prop].internal)
            col = this.getColDef(`${prop}.${nestedProp}`, objschema.properties[nestedProp], objschema)
            columnDefs.push(col)
          }
        })
      } else if (this.props.editable || this.props.admin || !schema.properties[prop].internal) { // (!this.editable || this.$store.getters.isStaff || !schema.properties[prop].internal)
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
  }

  getColDescriptions (schema) {
    // console.log('getColDescriptions', schema)
    const descriptions = {}
    Object.keys(schema.properties).forEach(prop => {
      descriptions[prop] = schema.properties[prop].description
    })
    return descriptions
  }

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
  }

  rowIsEmpty (row) {
    return !_.values(row).some(x => x !== undefined && x !== '')
  }

  addRow (number) {
    const rows = []
    for (let i = 0; i < number; i++) {
      rows.push({})
    }
    this.gridOptions.api.applyTransaction({ add: rows })
    // console.log('addRow', this.getRowData())
  }

  removeRows () {
    const selectedData = this.gridOptions.api.getSelectedRows()
    this.gridOptions.api.applyTransaction({ remove: selectedData })
    // this.errors = {}
    this.gridOptions.api.redrawRows()
    // this.validate(false)
  }

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
  }

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
  }

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
  }
}
export default AgUtil
