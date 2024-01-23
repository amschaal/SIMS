<template>
    <q-list padding bordered class="rounded-borders">
      <q-expansion-item
        dense
        dense-toggle
        expand-separator
        label="Submission Data"
      >
        <q-card>
          <q-card-section>
            <CustomFields v-model="submission_data" :schema="schema" ref="submission_fields" v-if="schema && data" :modify="false" :warnings="{}"/>
            <q-markup-table v-else>
              <thead>
                <tr>
                  <th class="text-left">Field</th>
                  <th class="text-right">Value</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(value, variable) in data" :key="variable">
                  <td class="text-left">{{variable}}</td>
                  <td class="text-right">{{value}}</td>
                </tr>
              </tbody>
          </q-markup-table>
          </q-card-section>
        </q-card>
      </q-expansion-item>
    </q-list>
</template>

<style>
</style>

<script>
import CustomFields from 'src/assets/jsonschema/forms/customFields.vue'
export default {
  name: 'LibraryDetail',
  props: ['data', 'schema'],
  data () {
    return {
      submission_data: this.data
    }
  },
  mounted: function () {
  },
  components: {
    CustomFields
  }
}
</script>
