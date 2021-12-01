import authHeaders from './utils';
import http from './http-common';

const resource = 'users';

export default {
  async get(id) {
    return http.get(`${resource}/${id}`);
  },

  async getMe(token) {
    return http.get(`${resource}/me`, authHeaders(token));
  },

  async updateMe(token, data) {
    return http.patch(`${resource}/me`, data, authHeaders(token));
  },

  async getUsers(token) {
    return http.get(`${resource}`, authHeaders(token));
  },

  async updateUser(token, userId, payload) {
    return http.patch(`${resource}/${userId}`, payload, authHeaders(token));
  },

  // TODO replace with using normal registration endpoint
  async createUser(token, payload) {
    console.log('NotImplementedError: use registration endpoint instead');
    return http.post(`${resource}`, payload, authHeaders(token));
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
};
