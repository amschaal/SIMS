<template>
  <BaseForm
    :model="model"
    ref="form"
    api-method="post"
    api-url="/api/machines/"
    :on-success="onSuccess"
    :on-error="onError"
    :hide-buttons="hideButtons"
  >
    <template v-slot:content="{ model, _errors, has_error }">
      Errors: {{ _errors }}
      <TypeSelect v-model="model.type" @schema="schema => changeSchema(schema)" />
      <!-- <q-input outlined v-model="model.type" label="Type"
        :error-message="errors.type"
        :error="has_error.type"
        /> -->
      <q-input outlined v-model="model.name" label="Name"
        :error-message="_errors.name"
        :error="has_error.name"
        />
      <q-input outlined v-model="model.description" label="Description" />
      <q-input outlined v-model="model.num_lanes" type="number" label="Number of Cells/Lanes"
        :error-message="_errors.num_lanes"
        :error="has_error.num_lanes"
      />
      <CustomFields v-model="model.data" :schema="schema" ref="custom_fields" v-if="schema" :modify="true" :errors="_errors.data" :warnings="{}"/>
      {{ model.data }}
    </template>
  </BaseForm>
</template>
<script>
import BaseForm from './BaseForm.vue'
import TypeSelect from '../TypeSelect.vue'
import CustomFields from 'assets/jsonschema/forms/customFields.vue'
export default {
  props: ['onSuccess', 'onError', 'hideButtons'],
  data () {
    return {
      errors: {},
      model: { data: { foo: 'baz' }, type: 'machine_illumina_hiseq' },
      schema: {}
    }
  },
  methods: {
    changeSchema (schema) {
      this.schema = schema
    }
  },
  components: {
    BaseForm,
    TypeSelect,
    CustomFields
  }
}
</script>
