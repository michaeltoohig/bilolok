import Vue from 'vue';
import authHeaders from './utils';

const resource = 'users';

export default {
  async getMe(token) {
    return Vue.prototype.$http.get(`${resource}/me`, authHeaders(token));
  },

  async updateMe(token, data) {
    return Vue.prototype.$http.patch(`${resource}/me`, data, authHeaders(token));
  },

  async get(id, token, params) {
    const options = authHeaders(token);
    options.params = params;
    return Vue.prototype.$http.get(`${resource}/${id}`, options);
  },

  async getUsers(token, params) {
    const options = authHeaders(token);
    options.params = params;
    return Vue.prototype.$http.get(`${resource}`, options);
  },

  async updateUser(token, userId, payload) {
    return Vue.prototype.$http.patch(`${resource}/${userId}`, payload, authHeaders(token));
  },

  // TODO replace with using normal registration endpoint
  async createUser(token, payload) {
    console.log('NotImplementedError: use registration endpoint instead');
    return Vue.prototype.$http.post(`${resource}`, payload, authHeaders(token));
  },

  async deleteProfile(id, token) {
    return Vue.prototype.$http.delete(`${resource}/${id}/profile`, authHeaders(token));
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

  async getTrips(id, skip = 0, limit = 100) {
    return Vue.prototype.$http.get(`${resource}/${id}/trips`, {
      params: {
        skip,
        limit,
      },
    });
  },

  async getVideos(id, skip = 0, limit = 0) {
    return Vue.prototype.$http.get(`${resource}/${id}/videos`, {
      params: {
        skip,
        limit,
      },
    });
  },
};
