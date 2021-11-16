/* eslint-disable */

import Vue from 'vue';

import imagesApi from '@/api/images';
import nakamalsApi from '@/api/nakamals';

const initialState = () => ({
  byId: {},
  byNakamalId: {},
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
  // Return a list of images of a nakamal.
  nakamal: (state, getters) => nakamalId => {
    if (!state.byNakamalId[nakamalId]) return [];
    return state.byNakamalId[nakamalId].map(id => getters.find(id));
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
  getNakamal: async ({ commit }, nakamalId) => {
    const response = await nakamalsApi.getImages(nakamalId);
    const images = response.data;
    images.forEach((item) => {
      commit('add', item);
    });
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
    if (!state.allIds.includes(item.id)) {
      state.allIds.push(item.id);
    }
    if (!state.byNakamalId[item.nakamal_id]) {
      Vue.set(state.byNakamalId, item.nakamal_id, []);
      state.byNakamalId[item.nakamal_id].push(item.id);
    }
    else if (!state.byNakamalId[item.nakamal_id].includes(item.id)) {
      state.byNakamalId[item.nakamal_id].push(item.id);
    }
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
