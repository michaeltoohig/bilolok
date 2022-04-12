import authHeaders from './utils';
import http from './http-common';

const resource = 'users';

export default {
  async getMe(token) {
    return http.get(`${resource}/me`, authHeaders(token));
  },

  async updateMe(token, data) {
    return http.patch(`${resource}/me`, data, authHeaders(token));
  },

  async get(id, token, auth = false) {
    const options = authHeaders(token);
    if (auth) {
      options.params = { auth };
    }
    console.log('getting user', id);
    return http.get(`${resource}/${id}`, options);
  },

  async getUsers(token, includeDetails = false, auth = false) {
    const options = authHeaders(token);
    console.log('xxx');
    if (auth) {
      options.params = { auth };
    }
    if (includeDetails) {
      options.params = { includeDetails };
    }
    return http.get(`${resource}`, options);
  },

  async updateUser(token, userId, payload) {
    return http.patch(`${resource}/${userId}`, payload, authHeaders(token));
  },

  // TODO replace with using normal registration endpoint
  async createUser(token, payload) {
    console.log('NotImplementedError: use registration endpoint instead');
    return http.post(`${resource}`, payload, authHeaders(token));
  },

  async deleteProfile(id, token) {
    return http.delete(`${resource}/${id}/profile`, authHeaders(token));
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
