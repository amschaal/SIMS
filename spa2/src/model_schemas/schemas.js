import { useJsonSchemaStore } from 'src/stores/jsonschema'

const sampleSchema = {
  type: 'object',
  properties: {
    // id: { type: 'string', maxLength: 50, minLength: 1, title: 'Id' },
    // type: { type: 'string', title: 'Type' },
    // data: { type: 'object', title: 'Data' },
    // physical_type: { type: ['string', 'null'], maxLength: 25, minLength: 1, title: 'Physical type' },
    id: {
      type: 'string',
      maxLength: 50,
      minLength: 1,
      title: 'ID',
      description: 'System ID',
      readOnly: true,
      'x-aggrid': {
        cellRenderer: params => {
          // return a hyperlink to sample if not header
          return params.value ? `<a href="/samples/${params.value}/">${params.value}</a>` : params.value
          // return params.node.rowPinned ? params.value : `<a href="/samples/${params.value}/">${params.value}</a>` // this should get checked in cellRendererSelector
        },
        cellRendererParams: {},
        sortable: true
      },
      checkboxSelection: true
    },
    type: {
      type: 'string',
      title: 'Type',
      readOnly: true,
      'x-aggrid': {
        cellRenderer: params => {
          // return a hyperlink to sample if not header
          return params.value ? params.value.id : params.value
          // return params.node.rowPinned ? params.value : `<a href="/samples/${params.value}/">${params.value}</a>` // this should get checked in cellRendererSelector
        },
        cellRendererParams: {}
      }
    },
    name: {
      type: 'string',
      maxLength: 50,
      minLength: 1,
      title: 'Name',
      description: 'Sample Name'
    },
    alias: {
      type: 'string',
      title: 'Alias',
      description: 'Sample Alias / Tube Name'
    },
    barcodes: {
      type: 'object',
      properties: {
        i5: {
          type: 'string',
          minLength: 1,
          title: 'I5'
        },
        i7: {
          type: 'string',
          minLength: 1,
          title: 'I7'
        },
        adapter_db: {
          type: 'string',
          minLength: 1,
          title: 'Adapter db'
        },
        adapter: {
          type: 'string',
          minLength: 1,
          title: 'Adapter'
        }
      },
      order: ['i5', 'i7', 'adapter_db', 'adapter'],
      title: 'Barcodes'
    }
    // barcodes: { type: 'object', title: 'Barcodes' },
    // sample: { type: 'integer', title: 'Sample' },
    // project: { type: 'integer', title: 'Project' },
    // submission: { type: 'integer', title: 'Submission' },
    // adapter: { type: 'integer', title: 'Adapter' }
  },
  required: ['name'],
  order: ['id', 'type', 'name', 'alias', 'barcodes', 'data']
}
const poolSchema = {
  type: 'object',
  properties: {
    id: { type: 'string', maxLength: 50, minLength: 1, title: 'ID', description: 'System ID', readOnly: true },
    name: { type: 'string', maxLength: 50, minLength: 1, title: 'Name' }
  },
  required: ['name'],
  order: ['id', 'name', 'data']
}
// const projectSchema = {
//   type: 'object',
//   properties: {
//     id: { type: 'string', maxLength: 50, minLength: 1, title: 'Id' },
//     type: { type: 'string', title: 'Type' },
//     data: { type: 'object', title: 'Data' }
//     // physical_type: { type: ['string', 'null'], maxLength: 25, minLength: 1, title: 'Physical type' },
//     // comment: { type: 'string', title: 'Comment' }
//     // barcodes: { type: 'object', title: 'Barcodes' },
//     // sample: { type: 'integer', title: 'Sample' },
//     // project: { type: 'integer', title: 'Project' },
//     // submission: { type: 'integer', title: 'Submission' },
//     // adapter: { type: 'integer', title: 'Adapter' }
//   },
//   required: [],
//   order: ['id', 'type', 'data']
// }
const projectSchema = {
  type: 'object',
  properties: {
    id: { type: 'string', maxLength: 50, minLength: 1, title: 'Id' },
    type: { type: 'string', title: 'Type' },
    data: { type: 'object', title: 'Data' },
    first_name: { type: 'string', maxLength: 50, minLength: 1, title: 'First name' },
    last_name: { type: 'string', maxLength: 50, minLength: 1, title: 'Last name' },
    email: { type: 'string', format: 'email', maxLength: 75, minLength: 1, title: 'Email' },
    phone: { type: 'string', maxLength: 20, minLength: 1, title: 'Phone' },
    pi_first_name: { type: 'string', maxLength: 50, minLength: 1, title: 'Pi first name' },
    pi_last_name: { type: 'string', maxLength: 50, minLength: 1, title: 'Pi last name' },
    pi_email: { type: 'string', format: 'email', maxLength: 75, minLength: 1, title: 'Pi email' },
    pi_phone: { type: 'string', maxLength: 20, minLength: 1, title: 'Pi phone' },
    institute: { type: 'string', maxLength: 75, minLength: 1, title: 'Institute' },
    comments: { type: ['string', 'null'], title: 'Comments' }
  },
  required: ['id', 'data', 'first_name', 'last_name', 'email', 'phone', 'pi_first_name', 'pi_last_name', 'pi_email', 'pi_phone', 'institute'],
  order: ['id', 'type', 'first_name', 'last_name', 'email', 'phone', 'pi_first_name', 'pi_last_name', 'pi_email', 'pi_phone', 'institute', 'comments', 'data']
}

const dataSchema = {
  type: 'object',
  properties: {
  },
  required: [],
  order: []
}

// const schema = {
//   type: 'object',
//   properties: {
//     type: { type: 'string', title: 'Type' },
//     data: { type: 'object', title: 'Data' }
//   },
//   required: ['data']
// }

class ModelSchemas {
  static schemas = {
    project: projectSchema,
    sample: sampleSchema,
    pool: poolSchema
  }

  static layouts = {
    project: { id: { width: 'col-6' }, type: { width: 'col-6' }, first_name: { width: 'col-3' }, last_name: { width: 'col-3' }, phone: { width: 'col-3' }, email: { width: 'col-3' }, pi_first_name: { width: 'col-3' }, pi_last_name: { width: 'col-3' }, pi_phone: { width: 'col-3' }, pi_email: { width: 'col-3' } }
  }

  static schemaStore = useJsonSchemaStore()

  static getSchema (model, type, dataField) {
    dataField = dataField || 'data'
    const schema = ModelSchemas.schemas[model]
    if (typeof type === 'string' || type instanceof String) {
      type = ModelSchemas.schemaStore.typeSchemas[type]
    }
    if (type) {
      schema.properties[dataField] = type.schema
    } else {
      schema.properties[dataField] = dataSchema
    }
    if (schema.order.indexOf(dataField) === -1) {
      schema.order.push(dataField)
    }
    return schema
  }
}

// const SampleSchema = BaseModelSchema(sample)
// const SampleSchema = BaseModelSchema(sample)

export default ModelSchemas
