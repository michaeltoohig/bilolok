import Vue from 'vue';
import VueRouter from 'vue-router';
import Meta from 'vue-meta';
import Home from '@/views/Home.vue';

Vue.use(VueRouter);
Vue.use(Meta);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/auth/:auth',
    name: 'Auth',
    component: () => import(/* webpackChunkName: "public" */ '@/views/Auth.vue'),
    // importing store to this file caused a circular dependency error
    // so authRouteGuard is in the component.
    // beforeEnter: authRouteGuard,
    // beforeUpdate: authRouteGuard,
  },
  {
    path: '/user',
    name: 'UserList',
    component: () => import(/* webpackChunkName: "public" */ '@/views/UserList.vue'),
  },
  {
    path: '/user/:id',
    name: 'User',
    component: () => import(/* webpackChunkName: "public" */ '@/views/User.vue'),
  },
  {
    path: '/about',
    name: 'About',
    component: () => import(/* webpackChunkName: "public" */ '@/views/About.vue'),
  },
  {
    path: '/map',
    name: 'Map',
    component: () => import(/* webpackChunkName: "public" */ '@/views/Map.vue'),
  },
  // {
  //   path: '/search',
  //   name: 'Search',
  //   component: () => import(/* webpackChunkName: "public" */ '@/views/Search.vue'),
  // },
  {
    path: '/nakamal/:id',
    name: 'Nakamal',
    component: () => import(/* webpackChunkName: "public" */ '@/views/Nakamal.vue'),
  },
  {
    path: '/nakamal/:id/edit',
    name: 'NakamalEdit',
    component: () => import(/* webpackChunkName: "public" */ '@/views/NakamalEdit.vue'),
  },
  {
    path: '/checkin/:id',
    name: 'Checkin',
    component: () => import(/* webpackChunkName: "public" */ '@/views/share/Checkin.vue'),
  },
  {
    path: '/image/:id',
    name: 'Image',
    component: () => import(/* webpackChunkName: "public" */ '@/views/share/Image.vue'),
  },
  {
    path: '/trip/:id',
    name: 'Trip',
    component: () => import(/* webpackChunkName: "public" */ '@/views/share/Trip.vue'),
  },
  {
    path: '/video/:id',
    name: 'Video',
    component: () => import(/* webpackChunkName: "public" */ '@/views/share/Video.vue'),
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
