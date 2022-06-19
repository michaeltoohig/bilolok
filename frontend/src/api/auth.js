import Vue from 'vue';

const resource = 'auth';

export default {
  async register(payload) {
    return Vue.prototype.$http.post(`${resource}/register`, payload);
  },

  async login(payload) {
    const formData = new FormData();
    formData.set('username', payload.username);
    formData.set('password', payload.password);
    return Vue.prototype.$http.post(
      `${resource}/jwt/login`,
      formData,
      {
        headers: {
          'content-type': 'application/x-www-form-urlencoded',
        },
      },
    );
  },

  async forgotPassword(payload) {
    return Vue.prototype.$http.post(`${resource}/forgot-password`, payload);
  },

  async resetPassword(payload) {
    return Vue.prototype.$http.post(`${resource}/reset-password`, payload);
  },

  async requestVerification(email) {
    return Vue.prototype.$http.post(`${resource}/request-verify-token`, { email });
  },

  async verify(token) {
    return Vue.prototype.$http.post(`${resource}/verify`, { token });
  },
};
