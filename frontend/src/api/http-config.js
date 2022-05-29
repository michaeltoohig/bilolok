/* eslint-disable */

import Vue from 'vue';
// import axiosRetry from 'axios-retry';
import axios from 'axios';
import store from '@/store';
import router from '@/router';
import { apiDomain } from '@/env';

const baseURL = `${apiDomain}/api/v1/`;

// const retry = (error) => {
//   const config = error.config;
//   config.__retryCount = config.__retryCount || 0;
//   console.log('###', config.__retryCount);
//   if (config.__retryCount >= 3) {
//     return Promise.reject(error);
//   }
//   config.__retryCount += 1;
//   const backoff = new Promise((resolve) => {
//     setTimeout(() => {
//       resolve();
//     }, 1000 * (config.__retryCount ** 2));
//   });
//   return backoff.then(() => {
//     return axios(config);
//   });
// };

export default {
  endpoint: baseURL,
  timeout: 15_000,

  // requestInterceptor: (config) => {
  //   config.headers.Authorization = store.getters.getToken;
  //   return config;
  // },

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
        // return Promise.reject(error);
      }
    } else if (error.request) {
      if (error.message.startsWith('timeout')) {
        console.log('timeout error');
        // retry(error)
        //   .then((resp) => resp)
        //   .catch(() => {
        //     store.dispatch('notify/add', {
        //       title: 'Server Timeout Error',
        //       text: 'Sorry, the server is not responding. Please reload the page later.',
        //       type: 'error',
        //       timeout: 10_000,
        //     });
        //   });
        store.dispatch('notify/add', {
          title: 'Server Timeout Error',
          text: 'Sorry, the server is not responding. Please reload the page later.',
          type: 'error',
          timeout: 10_000,
        });
        // return Promise.reject(error);
      }
    } else {
      // Something happened in setting up the request that triggered an Error
      console.log('Error', error.message);
      // return Promise.reject(error);
    }
    // console.log(error.config);
    return Promise.reject(error);
  },

  init() {
    // const interceptorId = rax.attach();
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
    // retry logic - retries is not a priority compared to better caching on backend
    // axiosRetry(Vue.prototype.$http, {
    //   retries: 3,
    //   retryCondition: 
    // });
  },
};
