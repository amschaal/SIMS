<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      {{ $store.auth.user }}
      <a class="btn" :href="loginUrl">Login</a>
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent } from 'vue'
// import { authStore } from 'src/stores/auth'
export default defineComponent({
  name: 'LoginLayout',
  data () {
    return {
      loginUrl: '/server/admin/'
    }
  },
  components: {
  },
  setup () {
    return {
    }
  }
})
</script>
