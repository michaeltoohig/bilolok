import authHeaders from './utils';
import http from './http-common';

const resource = 'users';

export default {
  async getMe(token) {
    return http.get(`${resource}/me`, authHeaders(token));
  },

  async updateMe(token, data) {
    return http.put(`${resource}/me`, data, authHeaders(token));
  },

  async getUsers(token) {
    return http.get(`${resource}`, authHeaders(token));
  },

  async updateUser(token, userId, payload) {
    return http.put(`${resource}/${userId}`, payload, authHeaders(token));
  },

  async createUser(token, payload) {
    return http.post(`${resource}`, payload, authHeaders(token));
  },
};
