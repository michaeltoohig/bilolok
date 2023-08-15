import Vue from 'vue';
// import authHeaders from './utils';

const resource = 'nakamal-resources';

export default {
  async getAll(params) {
    return Vue.prototype.$http.get(`${resource}`, { params });
  },

  // async create(token, payload) {
  //   const resp = await Vue.prototype.$http.post(`${resource}`, payload, authHeaders(token));
  //   let cached = ls.get(resource);
  //   if (cached) {
  //     cached.push(resp.data);
  //     // ls.set(resource, cached, { ttl: 3600 });
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
