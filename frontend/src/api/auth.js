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

  // async passwordRecovery(email: string) {
  //   return axios.post(`${apiUrl}/api/v1/password-recovery/${email}`);
  // },
  // async resetPassword(password: string, token: string) {
  //   return axios.post(`${apiUrl}/api/v1/reset-password/`, {
  //     new_password: password,
  //     token,
  //   });
  // },

  // async getMe(token) {
  //   return http.get(`${apiUrl}/api/v1/users/me`, authHeaders(token));
  // },
  // async updateMe(token, data) {
  //   return http.put(`${apiUrl}/api/v1/users/me`, data, authHeaders(token));
  // },
};
