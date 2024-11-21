<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-toolbar-title>
          Core Omics Lab
        </q-toolbar-title>
          <q-btn-dropdown color="white" flat label="Admin">
            <q-list>
              <q-item clickable v-close-popup :to="{ name: 'model_types'}">
                <q-item-section>
                  <q-item-label>Model Types</q-item-label>
                </q-item-section>
              </q-item>
              <q-item clickable v-close-popup :to="{ name: 'machines'}">
                <q-item-section>
                  <q-item-label>Machines</q-item-label>
                </q-item-section>
              </q-item>
              <q-item clickable v-close-popup :to="{ name: 'submission_types'}">
                <q-item-section>
                  <q-item-label>Submission Types</q-item-label>
                </q-item-section>
              </q-item>
              <!-- <q-item clickable v-close-popup :to="{ name: 'map_types'}">
                <q-item-section>
                  <q-item-label>Map Types</q-item-label>
                </q-item-section>
              </q-item> -->
            </q-list>
          </q-btn-dropdown>
          <q-btn-dropdown v-if="auth.user" color="primary" class="q-btn--flat" icon="person" :label="auth.user.username">
              <q-list>
                <q-item clickable v-close-popup @click="logout()">
                  <q-item-section>
                    <q-item-label>Logout</q-item-label>
                  </q-item-section>
                </q-item>
              </q-list>
            </q-btn-dropdown>
      </q-toolbar>
      <q-tabs>
          <q-route-tab :to="{ name: 'submissions'}" replace label="Submissions"/>
          <q-route-tab :to="{ name: 'projects'}" replace label="Projects"/>
          <q-route-tab :to="{ name: 'samples'}" replace label="Samples"/>
          <q-route-tab :to="{ name: 'pools'}" replace label="Pools"/>
          <q-route-tab :to="{ name: 'runs'}" replace label="Runs"/>
        </q-tabs>
    </q-header>
    <q-page-container>
      <router-view :key="$route.fullPath"/>
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent } from 'vue'
import { useAuthStore } from 'src/stores/authStore'
export default defineComponent({
  name: 'MainLayout',

  components: {
  },

  setup () {
    const auth = useAuthStore()
    return {
      auth,
      logout () {
        window.location.href = '/server/accounts/logout/'
      }
    }
  }
})
</script>
