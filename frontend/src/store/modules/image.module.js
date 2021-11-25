/* eslint-disable */

import Vue from 'vue';

import { normalizeRelations, resolveRelations } from '@/store/helpers';
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
  find: (state, _, __, rootGetters) => id => {
    return resolveRelations(state.byId[id], ['nakamal'], rootGetters);
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

function commitAddImage(image, commit) {
  // Normalize nested data and swap the image object
  // in the API response with an ID reference.
  commit('add', normalizeRelations(image, ['nakamal']));
  // Add or update the image.
  commit('nakamal/add', image.nakamal, {
    root: true,
  });
};

const actions = {
  getRecent: async ({ commit }) => {
    const response = await imagesApi.getRecent();
    const images = response.data;
    images.forEach((item) => {
      commitAddImage(item, commit);
    });
    commit('setRecentIds', images.map(i => i.id));
  },
  getNakamal: async ({ commit }, nakamalId) => {
    const response = await nakamalsApi.getImages(nakamalId);
    const images = response.data;
    images.forEach((item) => {
      commitAddImage(item, commit);
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
    if (!state.byNakamalId[item.nakamal]) {
      Vue.set(state.byNakamalId, item.nakamal, []);
      state.byNakamalId[item.nakamal].push(item.id);
    }
    else if (!state.byNakamalId[item.nakamal].includes(item.id)) {
      state.byNakamalId[item.nakamal].push(item.id);
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
