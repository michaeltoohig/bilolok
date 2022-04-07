import authHeaders from './utils';
import http from './http-common';

const resource = 'subscriptions';

export default {
  async getPublicKey(token) {
    return http.get(`${resource}`, authHeaders(token));
  },

  async create(token, payload) {
    return http.post(`${resource}`, payload, authHeaders(token));
  },

  async remove(token, deviceId) {
    const config = authHeaders(token);
    config.params = { deviceId };
    return http.delete(`${resource}`, config);
  },
};
