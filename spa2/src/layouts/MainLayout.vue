<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          @click="leftDrawerOpen = !leftDrawerOpen"
          aria-label="Menu"
        >
          <q-icon name="menu" />
        </q-btn>

        <q-toolbar-title>
          SIMS
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
              <q-item clickable v-close-popup :to="{ name: 'map_types'}">
                <q-item-section>
                  <q-item-label>Map Types</q-item-label>
                </q-item-section>
              </q-item>
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
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      bordered
      content-class="bg-grey-2"
    >
      <q-list>
        <q-item-label header>MENU</q-item-label>
        <!-- <q-item clickable tag="a" target="_blank" href="https://quasar.dev">
          <q-item-section avatar>
            <q-icon name="school" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Docs</q-item-label>
            <q-item-label caption>quasar.dev</q-item-label>
          </q-item-section>
        </q-item> -->
        <q-item clickable :to="{ name: 'submissions'}">
          <q-item-section>
            <q-item-label>Submissions</q-item-label>
          </q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'projects'}">
          <q-item-section>
            <q-item-label>Projects</q-item-label>
            <!-- <q-item-label caption>Projects</q-item-label> -->
          </q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'samples'}">
          <q-item-section>
            <q-item-label>Samples</q-item-label>
          </q-item-section>
        </q-item>
        <!-- <q-item clickable :to="{ name: 'libraries'}">
          <q-item-section>
            <q-item-label>Libraries</q-item-label>
          </q-item-section>
        </q-item> -->
        <q-item clickable :to="{ name: 'pools'}">
          <q-item-section>
            <q-item-label>Pools</q-item-label>
          </q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'runs'}">
          <q-item-section>
            <q-item-label>Runs</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view :key="$route.fullPath"/>
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useAuthStore } from 'src/stores/authStore'
export default defineComponent({
  name: 'MainLayout',

  components: {
  },

  setup () {
    const leftDrawerOpen = ref(false)
    const auth = useAuthStore()
    return {
      leftDrawerOpen,
      auth,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      },
      logout () {
        window.location.href = '/server/accounts/logout/'
      }
    }
  }
})
</script>
