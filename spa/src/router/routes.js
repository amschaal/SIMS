
const routes = [
  {
    path: '/',
    component: () => import('layouts/base.vue'),
    children: [
      { path: '', component: () => import('pages/Index.vue') },
      { name: 'projects', path: 'projects', component: () => import('pages/Projects.vue') },
      {
        path: '/projects/:id/',
        component: () => import('pages/Project.vue'),
        name: 'project',
        props: true
      },
      { name: 'samples', path: 'samples', component: () => import('pages/Samples.vue') },
      {
        path: '/samples/:id/',
        component: () => import('pages/Sample.vue'),
        name: 'sample',
        props: true
      },
      { name: 'libraries', path: 'libraries', component: () => import('pages/Libraries.vue') },
      {
        path: '/libraries/:id/',
        component: () => import('pages/Library.vue'),
        name: 'library',
        props: true
      },
      { name: 'pools', path: 'pools', component: () => import('pages/Pools.vue') },
      {
        path: '/pools/:id/',
        component: () => import('pages/Pool.vue'),
        name: 'pool',
        props: true
      },
      { name: 'runs', path: 'runs', component: () => import('pages/Runs.vue') },
      {
        path: '/runs/:id/',
        component: () => import('pages/Run.vue'),
        name: 'run',
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
