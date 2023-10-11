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
          D^3
        </q-toolbar-title>

        <div>
          <q-btn-dropdown color="white" flat label="Admin">
            <q-list>
              <q-item clickable v-close-popup :to="{ name: 'machines'}">
                <q-item-section>
                  <q-item-label>Machines</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </div>
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
        <q-item clickable :to="{ name: 'libraries'}">
          <q-item-section>
            <q-item-label>Libraries</q-item-label>
          </q-item-section>
        </q-item>
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

export default defineComponent({
  name: 'MainLayout',

  components: {
  },

  setup () {
    const leftDrawerOpen = ref(false)

    return {
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  }
})
</script>
