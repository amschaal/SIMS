<template>
  <div class="fullscreen bg-blue text-white text-center q-pa-md flex flex-center">
    <div>
      <div style="font-size: 20vh">
        Coreomics LIMS
      </div>

      <!-- <div class="text-h3" style="opacity:.4">
        Please click on the link below to login
      </div> -->

      <q-btn
        class="login-button"
        color="white"
        text-color="blue"
        unelevated
        to="/server/admin"
        label="Login"
        no-caps
      />
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage'
}
</script>

<style scoped>
.login-button {
  font-size: 1.2rem;
  width: 200px;
}
</style>
