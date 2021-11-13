import authHeaders from './utils';
import http from './http-common';

const resource = 'images';

export default {
  async getRecent() {
    return http.get(`${resource}`);
  },

  async remove(token, id) {
    return http.delete(`${resource}/${id}`, authHeaders(token));
  },
};
