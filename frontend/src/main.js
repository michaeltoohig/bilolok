import Vue from 'vue';
import * as Sentry from '@sentry/vue';
import { BrowserTracing } from '@sentry/tracing';
import { sentryDsn, sentryTunnel } from '@/env';

import App from './App.vue';
import './registerServiceWorker';
import i18n from './plugins/i18n';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';
import './plugins/photoswipe';
import 'roboto-fontface/css/roboto/roboto-fontface.css';
import '@mdi/font/css/materialdesignicons.css';
import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.css'; // eslint-ignore import/no-extraneous-dependencies
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'; // eslint-ignore
import './geo';
import './deviceId';

// Testing the following
function getPWADisplayMode() {
  const isStandalone = window.matchMedia('(display-mode: standalone)').matches;
  if (document.referrer.startsWith('android-app://')) {
    return 'twa';
  }
  if (navigator.standalone || isStandalone) {
    return 'standalone';
  }
  return 'browser';
}
console.log('PWA Display Mode:', getPWADisplayMode());

Vue.config.productionTip = false;

Sentry.init({
  Vue,
  dsn: sentryDsn,
  tunnel: sentryTunnel,
  logErrors: true,
  integrations: [
    new BrowserTracing({
      routingInstrumentation: Sentry.vueRouterInstrumentation(router),
      tracingOrigins: ['localhost', 'bilolok.com', /^\//],
    }),
  ],
  // Set tracesSampleRate to 1.0 to capture 100%
  // of transactions for performance monitoring.
  // We recommend adjusting this value in production
  tracesSampleRate: 0.05,
});

new Vue({
  i18n,
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
