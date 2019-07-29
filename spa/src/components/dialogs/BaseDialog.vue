<template>
  <q-dialog v-model="opened">
    <q-card>
      <q-card-section>
        <div class="text-h6">{{title}}</div>
      </q-card-section>

      <q-separator />

      <q-card-section style="max-height: 50vh" class="scroll">
        <slot name="content"></slot>
      </q-card-section>

      <q-separator />

      <q-card-actions align="right">
        <slot name="buttons">
          <q-btn flat label="Close" color="primary" v-close-popup />
        </slot>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>
<script>
export default {
  props: ['title'],
  data () {
    return {
      opened: false
    }
  },
  methods: {
    open () {
      this.opened = true
    },
    close () {
      this.opened = false
    }
  }
}
</script>
