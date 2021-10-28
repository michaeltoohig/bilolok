import Vue from 'vue';
import Vuex from 'vuex';
import authModule from './modules/auth.module';
import mapModule from './modules/map.module';
import nakamalModule from './modules/nakamal.module';
import notifyModule from './modules/notify.module';
import userModule from './modules/user.module';

Vue.use(Vuex);

export default new Vuex.Store({
  // Making sure that we're doing
  // everything correctly by enabling
  // strict mode in the dev environment.
  strict: process.env.NODE_ENV !== 'production',
  modules: {
    auth: authModule,
    map: mapModule,
    nakamal: nakamalModule,
    notify: notifyModule,
    user: userModule,
  },
});
