import http from './http-common';

const resource = 'auth';

export default {
  async register(payload) {
    return http.post(`${resource}/register`, payload);
  },

  async login(payload) {
    const formData = new FormData();
    formData.set('username', payload.username);
    formData.set('password', payload.password);
    return http.post(
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
    return http.post(`${resource}/forgot-password`, payload);
  },

  async resetPassword(payload) {
    return http.post(`${resource}/reset-password`, payload);
  },

  async requestVerification(email) {
    return http.post(`${resource}/request-verify-token`, { email });
  },

  async verify(token) {
    return http.post(`${resource}/verify`, { token });
  },
};
