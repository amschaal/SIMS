<template>
  <q-dialog v-model="opened">
    <q-card class="full-width" style="width:90%; max-width: 90%;">
      <q-card-section>
        <div class="text-h6">{{title}}</div>
      </q-card-section>

      <q-separator />

      <q-card-section style="" class="scroll q-pa-sm q-gutter-sm">
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
