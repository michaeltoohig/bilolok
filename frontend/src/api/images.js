import authHeaders from './utils';
import http from './http-common';

const resource = 'images';

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

  async remove(token, id) {
    return http.delete(`${resource}/${id}`, authHeaders(token));
  },
};
