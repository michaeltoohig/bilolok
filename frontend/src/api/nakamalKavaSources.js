import Vue from 'vue';
import authHeaders from './utils';

const resource = 'nakamal-kava-sources';

export default {
  async getAll(params) {
    return Vue.prototype.$http.get(`${resource}`, { params });
  },

  async create(token, payload) {
    return Vue.prototype.$http.post(`${resource}`, payload, authHeaders(token));
  },

  // async update(token, id, payload) {
  //   return Vue.prototype.$http.put(`${resource}/${id}`, payload, authHeaders(token));
  // },

  // async remove(token, id) {
  //   return Vue.prototype.$http.delete(`${resource}/${id}`, authHeaders(token));
  // },
};
