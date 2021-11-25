import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '@/views/Home.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/auth/:auth',
    name: 'Auth',
    component: () => import(/* webpackChunkName: "auth" */ '@/views/Auth.vue'),
    // importing store to this file caused a circular dependency error
    // so authRouteGuard is in the component.
    // beforeEnter: authRouteGuard,
    // beforeUpdate: authRouteGuard,
  },
  {
    path: '/about',
    name: 'About',
    component: () => import(/* webpackChunkName: "about" */ '@/views/About.vue'),
  },
  {
    path: '/map',
    name: 'Map',
    component: () => import(/* webpackChunkName: "map" */ '@/views/Map.vue'),
  },
  {
    path: '/search',
    name: 'Search',
    component: () => import(/* webpackChunkName: "search" */ '@/views/Search.vue'),
  },
  {
    path: '/nakamal/:id',
    name: 'Nakamal',
    component: () => import(/* webpackChunkName: "nakamal" */ '@/views/Nakamal.vue'),
  },
  {
    path: '/admin',
    name: 'Admin',
    redirect: '/admin/users/all',
    component: () => import(/* webpackChunkName: "admin" */ '@/views/admin/Admin.vue'),
    children: [
      {
        path: 'users',
        redirect: 'users/all',
      },
      {
        path: 'users/all',
        name: 'AdminUsers',
        component: () => import(/* webpackChunkName: "admin" */ '@/views/admin/Users.vue'),
      },
      {
        path: 'users/edit/:id',
        name: 'AdminUsersEdit',
        component: () => import(/* webpackChunkName: "admin" */ '@/views/admin/UserEdit.vue'),
      },
      {
        path: 'users/create',
        name: 'AdminUsersCreate',
        component: () => import(/* webpackChunkName: "admin" */ '@/views/admin/UserCreate.vue'),
      },
    ],
  },
  {
    path: '/*', redirect: '/',
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;