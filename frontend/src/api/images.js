import Vue from 'vue';
// import http from './http-common';
import authHeaders from './utils';

const resource = 'images';

export default {
  async get(id) {
    return Vue.prototype.$http.get(`${resource}/${id}`);
  },

  async getAll(params) {
    return Vue.prototype.$http.get(`${resource}`, {
      params: {
        ...params,
      },
    });
  },

  async getRecent() {
    return Vue.prototype.$http.get(`${resource}`, {
      params: {
        recent: true,
      },
    });
  },

  async remove(token, id) {
    return Vue.prototype.$http.delete(`${resource}/${id}`, authHeaders(token));
  },
};
