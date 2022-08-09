import Vue from 'vue';
import ls from 'localstorage-slim';
import authHeaders from './utils';

const resource = 'videos';

export default {
  async get(id) {
    return Vue.prototype.$http.get(`${resource}/${id}`);
  },

  async getAll(params) {
    const cacheKey = `${resource}:${JSON.stringify(params)}`;
    const cached = ls.get(cacheKey);
    if (cached) {
      return cached;
    } else {
      const resp = await Vue.prototype.$http.get(`${resource}`, {
        params: {
          ...params,
        },
      });
      ls.set(cacheKey, resp.data, { ttl: 600 });
      return resp.data;
    }
  },

  async getRecent() {
    const cacheKey = `${resource}:recent`;
    const cached = ls.get(cacheKey);
    if (cached) {
      return cached;
    } else {
      const resp = await Vue.prototype.$http.get(`${resource}`, {
        params: {
          recent: true,
        },
      });
      if (resp.data.length > 0) {
        ls.set(cacheKey, resp.data, { ttl: 300 });
      }
      return resp.data;
    }
  },

  async create(token, payload) {
    const resp = await Vue.prototype.$http.post(`${resource}`, payload, authHeaders(token));
    let cached = ls.get(resource);
    if (cached) {
      cached.push(resp.data);
      ls.set(resource, cached, { ttl: 600 });
    }
    return resp.data;
  },

  // async update(token, id, payload) {
  //   return Vue.prototype.$http.put(`${resource}/${id}`, payload, authHeaders(token));
  // },

  async remove(token, id) {
    return Vue.prototype.$http.delete(`${resource}/${id}`, authHeaders(token));
  },
};
