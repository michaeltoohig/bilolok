/* eslint-disable */

import Vue from 'vue';

import imagesApi from '@/api/images';

const initialState = () => ({
  byId: {},
  allIds: [],
  recentIds: [],
});

const state = initialState();

const getters = {
  // Return a single image with the given id.
  find: (state) => id => {
    return state.byId[id];
  },
  // Return a list of images in the order of `allIds`.
  list: (state, getters) => {
    return state.allIds.map(id => getters.find(id));
  },
  // Return a list of recent images. 
  recent: (state, getters) => {
    return state.recentIds.map(id => getters.find(id));
  },
};

const actions = {
  getRecent: async ({ commit }) => {
    const response = await imagesApi.getRecent();
    const images = response.data;
    images.forEach((item) => {
      commit('add', item);
    });
    commit('setRecentIds', images.map(i => i.id));
  },
};

const mutations = {
  RESET (state) {
    const newState = initialState();
    Object.keys(newState).forEach(key => {
      state[key] = newState[key];
    });
  },
  add: (state, item) => {
    Vue.set(state.byId, item.id, item);
    if (state.allIds.includes(item.id)) return;
    state.allIds.push(item.id);
  },
  setRecentIds: (state, ids) => {
    state.recentIds = ids;
  },
};

export default {
  actions,
  getters,
  mutations,
  namespaced: true,
  state,
};
