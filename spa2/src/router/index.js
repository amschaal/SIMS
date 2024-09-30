import { route } from 'quasar/wrappers'
import { createRouter, createMemoryHistory, createWebHistory, createWebHashHistory } from 'vue-router'
import routes from './routes'
import { useAuthStore } from 'src/stores/authStore'

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default route(function ({ store }) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory)

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(process.env.VUE_ROUTER_BASE)
  })
  const authStore = useAuthStore()
  Router.beforeEach((to, from, next) => {
    // // redirect to login page if not logged in and trying to access a restricted page
    // const { authorize } = to.meta
    if (authStore.user || to.path !== '/login') {
      next()
    } else {
      authStore.fetchUser().then(f => {
        if (!authStore.user && to.path !== '/login') {
          return next({ path: '/login' })
        } else {
          next()
        }
      })
    }
  })
  return Router
})
