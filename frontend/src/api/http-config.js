/* eslint-disable */

import Vue from 'vue';
import axios from 'axios';
import store from '@/store';
import router from '@/router';
import { apiDomain } from '@/env';

const baseURL = `${apiDomain}/api/v1/`;

export default {
  endpoint: baseURL,
  timeout: 10_000,

  requestInterceptor: (config) => {
    config.headers.Authorization = store.getters.getToken;
    return config;
  },

  responseHandler: (response) => response,

  responseErrorHandler: (error) => {
    console.log('Response Error Handler:', error.message);
    if (error.response) {
      if (error.response.status === 401) {
        // NOTE this pattern fails if a logged in user 
        //  tries to perform an action they are not authorized for.
        //  Currently, I have manually wrapped those actions in a 
        //    check that the user is verified otherwise I open a modal.
        // TODO check if user is logged in then open that modal here
        //  If not logged in redirect to login.
        console.log('401 nauthorized error');
        router.push('/auth/login?unauthorized=true');
        return Promise.reject(error);
      }
    } else if (error.request) {
      if (error.message.startsWith('timeout')) {
        console.log('timeout error');
        store.dispatch('notify/add', {
          title: 'Server Timeout Error',
          text: 'Sorry, the server did not respond in time. Please reload the page later.',
          type: 'error',
          timeout: 10_000,
        });
      }
    } else {
      // Something happened in setting up the request that triggered an Error
      console.log('Error', error.message);
    }
    console.log(error.config);
  },

  init() {
    Vue.prototype.$http = axios.create({
      baseURL: this.endpoint,
      timeout: this.timeout,
      headers: {
        'Content-Type': 'application/json',
      },
    });
    // Vue.prototype.$http.interceptors.request.use(this.requestInterceptor);
    Vue.prototype.$http.interceptors.response.use(
      (response) => this.responseHandler(response),
      (error) => this.responseErrorHandler(error),
    );
  },
};
