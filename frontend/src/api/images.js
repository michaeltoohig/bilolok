import authHeaders from './utils';
import http from './http-common';

const resource = 'images';

export default {
  async getRecent() {
    return http.get(`${resource}`, {
      params: {
        limit: 3,
      },
    });
  },

  async remove(token, id) {
    return http.delete(`${resource}/${id}`, authHeaders(token));
  },
};
