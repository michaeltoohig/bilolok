import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '@/store';
import routes from './routes';

Vue.use(VueRouter);

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

// Before each route evaluates...
router.beforeEach((routeTo, routeFrom, next) => {
  // If this isn't an initial page load...
  if (routeFrom.name !== null) {
    // Start the route progress bar.
    // NProgress.start();
  }

  // Check if auth is required on this route
  const authRequired = routeTo.matched.some((route) => route.meta?.authRequired);
  if (!authRequired) return next();

  // const authStore = useAuthStore();
  // authStore.user ? next() : redirectToLogin();
  console.log('login status check', store.getters['auth/isLoggedIn']);
  store.getters['auth/isLoggedIn'] ? next() : redirectToLogin();

  function redirectToLogin() {
    console.log(`[AUTH REDIRECT] must be logged into access ${routeTo.fullPath}`);
    // ElMessage({
    //   message: 'You must be logged in to view that page.',
    //   grouping: true,
    //   type: 'info',
    // });
    // Pass the original route to the login component
    // next({ name: 'login', query: { redirectFrom: routeTo.fullPath } });
    next({ name: 'Auth', params: { auth: 'login' } });
  };
});


router.beforeResolve(async (routeTo, routeFrom, next) => {
  // Create a `beforeResolve` hook, which fires whenever
  // `beforeRouteEnter` and `beforeRouteUpdate` would. This
  // allows us to ensure data is fetched even when params change,
  // but the resolved route does not. We put it in `meta` to
  // indicate that it's a hook we created, rather than part of
  // Vue Router (yet?).
  try {
    // For each matched route...
    for (const route of routeTo.matched) {
      console.log('beforeResolve root');
      await new Promise((resolve, reject) => {
        // If a `beforeResolve` hook is defined, call it with
        // the same arguments as the `beforeEnter` hook.
        if (route.meta && route.meta.beforeResolve) {
          route.meta.beforeResolve(routeTo, routeFrom, (...args) => {
            // If the user chose to redirect...
            if (args.length) {
              // If redirecting to the same route we're coming from...
              if (routeFrom.name === args[0].name) {
                // Complete the animation of the route progress bar.
                // NProgress.done();
              }
              // Complete the redirect.
              next(...args);
              resolve();
              // reject(new Error('Redirected'));
            } else {
              resolve();
            }
          })
        } else {
          // Otherwise, continue resolving the route.
          resolve();
        }
      })
    }
    // If a `beforeResolve` hook chose to redirect, just return.
  } catch (error) {
    return;
  }
  // If we reach this point, continue resolving the route.
  next();
});

// When each route is finished evaluating...
router.afterEach((routeTo, routeFrom) => {
  // Complete the animation of the route progress bar.
  // NProgress.done();
});

export default router;
