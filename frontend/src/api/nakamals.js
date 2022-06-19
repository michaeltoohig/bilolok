import Vue from 'vue';
import authHeaders from './utils';

const resource = 'nakamals';

export default {
  async get(id) {
    return Vue.prototype.$http.get(`${resource}/${id}`);
  },

  async getAll(params) {
    return Vue.prototype.$http.get(`${resource}`, { params });
  },

  async create(token, payload) {
    return Vue.prototype.$http.post(`${resource}`, payload, authHeaders(token));
  },

  async update(token, id, payload) {
    return Vue.prototype.$http.put(`${resource}/${id}`, payload, authHeaders(token));
  },

  async remove(token, id) {
    return Vue.prototype.$http.delete(`${resource}/${id}`, authHeaders(token));
  },

  async getFeatured() {
    return Vue.prototype.$http.get(`${resource}/featured`);
  },

  async putFeatured(id) {
    return Vue.prototype.$http.put(`${resource}/${id}/featured`);
  },

  async getImages(id, skip = 0, limit = 100) {
    return Vue.prototype.$http.get(`${resource}/${id}/images`, {
      params: {
        skip,
        limit,
      },
    });
  },

  async getCheckins(id, skip = 0, limit = 100) {
    return Vue.prototype.$http.get(`${resource}/${id}/checkins`, {
      params: {
        skip,
        limit,
      },
    });
  },

  async getVideos(id, skip = 0, limit = 100) {
    return Vue.prototype.$http.get(`${resource}/${id}/videos`, {
      params: {
        skip,
        limit,
      },
    });
  },

  async putResource(token, id, resourceId) {
    return Vue.prototype.$http.put(`${resource}/${id}/resources/${resourceId}`, {}, authHeaders(token));
  },

  async deleteResource(token, id, resourceId) {
    return Vue.prototype.$http.delete(`${resource}/${id}/resources/${resourceId}`, authHeaders(token));
  },
};
