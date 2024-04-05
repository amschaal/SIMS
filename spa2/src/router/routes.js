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
      { path: '', component: () => import('layouts/MainLayout.vue') },
      // { path: '', component: () => import('pages/IndexPage.vue') },
      { name: 'submissions', path: 'submissions', component: () => import('pages/SubmissionsPage.vue') },
      {
        path: '/submissions/:id/',
        component: () => import('pages/SubmissionPage.vue'),
        name: 'submission',
        props: true
      },
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
        component: () => import('pages/PoolPage.vue'),
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
      { name: 'submission_types', path: 'submission_types', component: () => import('pages/SubmissionTypesPage.vue') },
      {
        path: '/submission_types/:id/',
        component: () => import('pages/SubmissionTypePage.vue'),
        name: 'submission_type',
        props: true
      },
      {
        path: '/submission_type_mappers/:id/',
        component: () => import('pages/SubmissionTypeMapperPage.vue'),
        name: 'submission_type_mapper',
        props: true
      },
      { name: 'machines', path: 'machines', component: () => import('pages/MachinesPage.vue') },
      {
        path: '/machines/:id/',
        component: () => import('pages/MachinePage.vue'),
        name: 'machine',
        props: true
      },
      { name: 'map_types', path: 'map_types', component: () => import('pages/MapTypesPage.vue') },
      { name: 'model_types', path: 'model_types', component: () => import('pages/ModelTypesPage.vue') },
      {
        path: '/model_types/:id/',
        component: () => import('pages/ModelTypePage.vue'),
        name: 'model_type',
        props: true
      },
      { name: 'json_schema_test', path: 'json_schema_test', component: () => import('pages/JSONSchemaFormTest.vue') }
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
