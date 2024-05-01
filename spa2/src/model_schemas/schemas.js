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
        cellRendererParams: {}
      }
    },
    name: {
      type: 'string',
      maxLength: 50,
      minLength: 1,
      title: 'Name',
      description: 'Sample Name'
    }
    // barcodes: { type: 'object', title: 'Barcodes' },
    // sample: { type: 'integer', title: 'Sample' },
    // project: { type: 'integer', title: 'Project' },
    // submission: { type: 'integer', title: 'Submission' },
    // adapter: { type: 'integer', title: 'Adapter' }
  },
  required: ['name'],
  order: ['id', 'name', 'data']
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
const projectSchema = {
  type: 'object',
  properties: {
    // id: { type: 'string', maxLength: 50, minLength: 1, title: 'Id' },
    // type: { type: 'string', title: 'Type' },
    // data: { type: 'object', title: 'Data' },
    // physical_type: { type: ['string', 'null'], maxLength: 25, minLength: 1, title: 'Physical type' },
    // comment: { type: 'string', title: 'Comment' }
    // barcodes: { type: 'object', title: 'Barcodes' },
    // sample: { type: 'integer', title: 'Sample' },
    // project: { type: 'integer', title: 'Project' },
    // submission: { type: 'integer', title: 'Submission' },
    // adapter: { type: 'integer', title: 'Adapter' }
  },
  required: [],
  order: ['data']
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

  static schemaStore = useJsonSchemaStore()

  static getSchema (model, typeId, dataField) {
    dataField = dataField || 'data'
    const schema = ModelSchemas.schemas[model]
    const type = ModelSchemas.schemaStore.typeSchemas[typeId]
    schema.properties[dataField] = type.schema
    if (schema.order.indexOf(dataField) === -1) {
      schema.order.push(dataField)
    }
    return schema
  }
}

// const SampleSchema = BaseModelSchema(sample)
// const SampleSchema = BaseModelSchema(sample)

export default ModelSchemas
