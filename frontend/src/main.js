import Vue from 'vue';
import App from './App.vue';
import './registerServiceWorker';
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

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
