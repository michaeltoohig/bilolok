import authHeaders from './utils';
import http from './http-common';

const resource = 'nakamals';

export default {
  async get(id) {
    return http.get(`${resource}/${id}`);
  },

  async getAll(params) {
    return http.get(`${resource}`, { params });
  },

  async create(token, payload) {
    return http.post(`${resource}`, payload, authHeaders(token));
  },

  async update(token, id, payload) {
    return http.put(`${resource}/${id}`, payload, authHeaders(token));
  },

  async remove(token, id) {
    return http.delete(`${resource}/${id}`, authHeaders(token));
  },

  async getFeatured() {
    return http.get(`${resource}/featured`);
  },

  async putFeatured(id) {
    return http.put(`${resource}/${id}/featured`);
  },

  async getImages(id, skip = 0, limit = 100) {
    return http.get(`${resource}/${id}/images`, {
      params: {
        skip,
        limit,
      },
    });
  },

  async getCheckins(id, skip = 0, limit = 100) {
    return http.get(`${resource}/${id}/checkins`, {
      params: {
        skip,
        limit,
      },
    });
  },

  async putResource(token, id, resourceId) {
    return http.put(`${resource}/${id}/resources/${resourceId}`, {}, authHeaders(token));
  },

  async deleteResource(token, id, resourceId) {
    return http.delete(`${resource}/${id}/resources/${resourceId}`, authHeaders(token));
  },
};
