import Vue from 'vue';
import authHeaders from './utils';

const resource = 'subscriptions';

export default {
  async getPublicKey(token) {
    return Vue.prototype.$http.get(`${resource}`, authHeaders(token));
  },

  async create(token, payload) {
    return Vue.prototype.$http.post(`${resource}`, payload, authHeaders(token));
  },

  async remove(token, deviceId) {
    const config = authHeaders(token);
    config.params = { deviceId };
    return Vue.prototype.$http.delete(`${resource}`, config);
  },
};
