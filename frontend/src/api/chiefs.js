import Vue from 'vue';

const resource = 'chiefs';

export default {
  async getUser(id) {
    return Vue.prototype.$http.get(`${resource}/${id}`);
  },

  async getAll(params) {
    return Vue.prototype.$http.get(`${resource}`, {
      params: {
        ...params,
      },
    });
  },

  // async getRecent() {
  //   return Vue.prototype.$http.get(`${resource}`, {
  //     params: {
  //       recent: true,
  //     },
  //   });
  // },
};
