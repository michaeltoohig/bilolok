import authHeaders from './utils';
import http from './http-common';

const resource = 'videos';

export default {
  async getAll(params) {
    return http.get(`${resource}`, {
      params: {
        ...params,
      },
    });
  },

  async getRecent() {
    return http.get(`${resource}`, {
      params: {
        recent: true,
      },
    });
  },

  async create(token, payload) {
    return http.post(`${resource}`, payload, authHeaders(token));
  },

  // async update(token, id, payload) {
  //   return http.put(`${resource}/${id}`, payload, authHeaders(token));
  // },

  async remove(token, id) {
    return http.delete(`${resource}/${id}`, authHeaders(token));
  },
};
