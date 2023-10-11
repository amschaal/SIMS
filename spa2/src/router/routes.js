// const routes = [
//   {
//     path: '/',
//     component: () => import('layouts/MainLayout.vue'),
//     children: [
//       { path: '', component: () => import('pages/IndexPage.vue') }
//     ]
//   },

//   // Always leave this as last one,
//   // but you can also remove it
//   {
//     path: '/:catchAll(.*)*',
//     component: () => import('pages/ErrorNotFound.vue')
//   }
// ]
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/MainLayout.vue') },
      { name: 'projects', path: 'projects', component: () => import('pages/ProjectsPage.vue') },
      {
        path: '/projects/:id/',
        component: () => import('pages/ProjectPage.vue'),
        name: 'project',
        props: true
      },
      { name: 'samples', path: 'samples', component: () => import('pages/SamplesPage.vue') },
      {
        path: '/samples/:id/',
        component: () => import('pages/SamplePage.vue'),
        name: 'sample',
        props: true
      },
      { name: 'libraries', path: 'libraries', component: () => import('pages/LibrariesPage.vue') },
      {
        path: '/libraries/:id/',
        component: () => import('pages/LibraryPage.vue'),
        name: 'library',
        props: true
      },
      { name: 'pools', path: 'pools', component: () => import('pages/PoolsPage.vue') },
      {
        path: '/pools/:id/',
        component: () => import('pages/Pool.vue'),
        name: 'pool',
        props: true
      },
      { name: 'runs', path: 'runs', component: () => import('pages/RunsPage.vue') },
      {
        path: '/runs/:id/',
        component: () => import('pages/RunPage.vue'),
        name: 'run',
        props: true
      },
      { name: 'machines', path: 'machines', component: () => import('pages/MachinesPage.vue') },
      {
        path: '/machines/:id/',
        component: () => import('pages/MachinePage.vue'),
        name: 'machine',
        props: true
      }
    ]
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
