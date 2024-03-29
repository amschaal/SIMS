<template>
  <!-- Loosely based on example: https://codepen.io/Hawkeye64/pen/xxbXajq -->
  <div>
    <div>
      <q-select
        v-model="model"
        :options="getOptions()"
        label="Foreign Key Reference"
        hint="You may validate that the value for this column matches a record from another table.  Select which table and column to reference."
        stack-label
        clearable
        @input="change"
      >
        <template v-slot:option="scope">
          <q-expansion-item
            expand-separator
            :default-opened="hasChild(scope)"
             header-class="text-weight-bold"
            :label="scope.opt.label"
          >
            <template v-for="child in scope.opt.children" :key="child.label">
              <q-item
                clickable
                v-ripple
                v-close-popup
                @click="set(scope.opt.label, child.label)"
                :class="{ 'bg-light-blue-1': model === child.label }"
              >
                <q-item-section>
                  <q-item-label class="q-ml-md" >{{ child.label }}</q-item-label>
                  <!-- <q-item-label v-html="child.label" class="q-ml-md" ></q-item-label> -->
                </q-item-section>
              </q-item>
            </template>
          </q-expansion-item>
        </template>
      </q-select>
    </div>
    <q-badge color="primary" multi-line v-if="model">
      Table: {{ model[0] }} Column: {{ model[1] }}
    </q-badge>
  </div>
</template>

<script>
import schema from '../schema'
export default {
  props: ['schema', 'modelValue'],
  emits: ['update:modelValue'],
  data () {
    return {
      model: this.modelValue && this.modelValue.slice ? this.modelValue.slice() : null
    }
  },
  methods: {
    set (table, column) {
      this.model = [table, column]
      this.change()
    },
    change () {
      this.$emit('update:modelValue', this.model)
    },
    getLabel (scope) {
      console.log(scope)
      return scope.label
    },
    hasChild (scope) {
      return scope.opt.children.some(c => c.label === this.model)
    },
    getOptions () {
      const options = []
      // {
      //   label: 'American cars',
      //   children: [
      //     {
      //       label: 'Ford'
      //     },
      //     {
      //       label: 'General Motors'
      //     },
      //     {
      //       label: 'Tesla'
      //     }
      //   ]
      // },
      schema.getTableSchemas(this.schema).forEach(function (table) {
        const tableOptions = { label: table.table }
        tableOptions.children = schema.getNonTables(table.schema).map(function (v) {
          return { label: v }
        })
        options.push(tableOptions)
      })
      return options
    }
  }
}
</script>
