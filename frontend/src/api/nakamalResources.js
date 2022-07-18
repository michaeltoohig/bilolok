import Vue from 'vue';
// import authHeaders from './utils';
import ls from 'localstorage-slim';

const resource = 'nakamal-resources';

export default {
  async getAll(params) {
    const cached = ls.get(resource);
    if (cached) {
      return cached;
    } else {
      const resp = await Vue.prototype.$http.get(`${resource}`, { params });
      ls.set(resource, resp.data, { ttl: 3600 });
      return resp.data;
    }
  },

  // async create(token, payload) {
  //   const resp = await Vue.prototype.$http.post(`${resource}`, payload, authHeaders(token));
  //   let cached = ls.get(resource);
  //   if (cached) {
  //     cached.push(resp.data);
  //     ls.set(resource, cached, { ttl: 3600 });
  //   }
  //   return resp.data
  // },

  // async update(token, id, payload) {
  //   return Vue.prototype.$http.put(`${resource}/${id}`, payload, authHeaders(token));
  // },

  // async remove(token, id) {
  //   return Vue.prototype.$http.delete(`${resource}/${id}`, authHeaders(token));
  // },
};
