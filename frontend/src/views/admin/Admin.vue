<template>
  <router-view></router-view>
</template>

<script>
import store from '@/store';

const adminRouteGuard = async (to, from, next) => {
  if (!store.getters['auth/hasAdminAccess']) {
    next('/home');
  }
  next();
};

export default {
  name: 'Admin',
  beforeRouteEnter(to, from, next) {
    adminRouteGuard(to, from, next);
  },
  beforeRouteUpdate(to, from, next) {
    adminRouteGuard(to, from, next);
  },
};
</script>
