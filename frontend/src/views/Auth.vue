<template>
  <div class="auth">
    <component :is="$route.params.auth"></component>
  </div>
</template>

<script>
import store from '@/store';
import Login from '@/components/auth/Login.vue';
import Register from '@/components/auth/Register.vue';

const authRouteGuard = async (to, from, next) => {
  await store.dispatch('auth/checkLoggedIn');
  if (store.getters['auth/isLoggedIn']) {
    if ((to.path).startsWith('/auth')) {
      next('/');
    }
  }
  next();
};

export default {
  name: 'Auth',
  components: {
    login: Login,
    signup: Register,
  },
  beforeRouteEnter(to, from, next) {
    authRouteGuard(to, from, next);
  },
  beforeRouteUpdate(to, from, next) {
    authRouteGuard(to, from, next);
  },
};
</script>

<style scoped>

</style>
