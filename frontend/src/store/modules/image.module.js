/* eslint-disable */

import Vue from 'vue';

import imagesApi from '@/api/images';

const initialState = () => ({
  byId: {},
  allIds: [],
});

const state = initialState();

const getters = {
  // Return a single nakamal with the given id.
  find: (state) => id => {
    return state.byId[id];
  },
  // Return a list of images in the order of `allIds`.
  list: (state, getters) => {
    return state.allIds.map(id => getters.find(id));
  },
};

const actions = {};

const mutations = {
  RESET (state) {
    const newState = initialState();
    Object.keys(newState).forEach(key => {
      state[key] = newState[key];
    });
  },
};

export default {
  actions,
  getters,
  mutations,
  namespaced: true,
  state,
};
