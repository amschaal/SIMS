import { useJsonSchemaStore } from 'src/stores/jsonschema'

const sampleSchema = {
  type: 'object',
  properties: {
    // id: { type: 'string', maxLength: 50, minLength: 1, title: 'Id' },
    // type: { type: 'string', title: 'Type' },
    // data: { type: 'object', title: 'Data' },
    // physical_type: { type: ['string', 'null'], maxLength: 25, minLength: 1, title: 'Physical type' },
    name: { type: 'string', maxLength: 50, minLength: 1, title: 'Name' }
    // barcodes: { type: 'object', title: 'Barcodes' },
    // sample: { type: 'integer', title: 'Sample' },
    // project: { type: 'integer', title: 'Project' },
    // submission: { type: 'integer', title: 'Submission' },
    // adapter: { type: 'integer', title: 'Adapter' }
  },
  required: ['name'],
  order: ['name', 'data']
}
const poolSchema = {
  type: 'object',
  properties: {
    name: { type: 'string', maxLength: 50, minLength: 1, title: 'Name' }
  },
  required: ['name'],
  order: ['name', 'data']
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
