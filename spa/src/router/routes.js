
const routes = [
  {
    path: '/',
    component: () => import('layouts/base.vue'),
    children: [
      { path: '', component: () => import('pages/Index.vue') },
      { name: 'projects', path: 'projects', component: () => import('pages/Projects.vue') },
      {
        path: '/projects/:id',
        component: () => import('pages/Project.vue'),
        name: 'project',
        props: true
      }
    ]
  }
]

// Always leave this as last one
if (process.env.MODE !== 'ssr') {
  routes.push({
    path: '*',
    component: () => import('pages/Error404.vue')
  })
}

export default routes
