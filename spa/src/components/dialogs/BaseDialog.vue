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
        <q-btn flat label="Decline" color="primary" v-close-popup />
        <q-btn flat label="Accept" color="primary" v-close-popup />
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
    }
  }
}
</script>
