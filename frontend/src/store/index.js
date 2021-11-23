import Vue from 'vue';
import Vuex from 'vuex';
import authModule from './modules/auth.module';
import checkinModule from './modules/checkin.module';
import imageModule from './modules/image.module';
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
    checkin: checkinModule,
    image: imageModule,
    map: mapModule,
    nakamal: nakamalModule,
    notify: notifyModule,
    user: userModule,
  },
});
