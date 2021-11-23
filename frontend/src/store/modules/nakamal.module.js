/* eslint-disable */

import Vue from 'vue';

import { normalizeRelations, resolveRelations } from '@/store/helpers';
import nakamalsApi from '@/api/nakamals';

import {
  latLng,
} from 'leaflet';

const initialState = () => ({
  byId: {},
  allIds: [],
  selectedId: null,
});

const state = initialState();

const getters = {
  // Return a single nakamal with the given id.
  find: (state, _, __, rootGetters) => id => {
    // Swap ID references with the resolved image objects.
    return state.byId[id];
    // return resolveRelations(state.byId[id], ['image'], rootGetters);
  },
  // Return a list of nakamals in the order of `allIds`.
  list: (state, getters) => {
    return state.allIds.map(id => getters.find(id));
  },
  total: (state) => {
    return state.allIds.length;
  },
  selected: (state, getters) => {
    if (state.selectedId === null) return {
      name: '',
      owner: '',
      phone: '',
      image: null,
    };
    return getters.find(state.selectedId);
  },
};

function commitAddNakamal(nakamal, commit) {
  // Normalize nested data and swap the image object
  // in the API response with an ID reference.
  commit('add', normalizeRelations(nakamal, ['image']));
  // Add or update the image.
  if (nakamal.image) {
    commit('image/add', nakamal.image, {
      root: true,
    });
  }
};

const actions = {
  load: async ({ commit }) => {
    const response = await nakamalsApi.getAll({});
    const nakamals = response.data
    nakamals.forEach((item) => {
      commitAddNakamal(item, commit);
    });
  },
  loadOne: async ({ commit }, id) => {
    try {
      let response = await nakamalsApi.get(id);
      const nakamal = response.data;
      commitAddNakamal(nakamal, commit);
    }
    catch (error) {
      console.log('! load one nakamal in catch');
    }
  },
  add: async ({ commit, dispatch, rootState }, payload) => {
    try {
      let token = rootState.auth.token;
      let response = await nakamalsApi.create(token, payload);
      const nakamal = response.data;
      commitAddNakamal(nakamal, commit);
      dispatch('notify/add', {
        title: 'Kava Bar Added',
        text: 'Thank you for sharing!',
        type: 'primary',
      }, { root: true });
    }
    catch (error) { 
      console.log('! add nakamal in catch');
    }
  },
  select: async ({ commit }, id) => {
    commit('select', id);
    // dispatch image action to load image of nakamal
    // disptach('')
  },
  unselect: async ({ commit }) => {
    commit('unselect');
  },
  remove: async ({ commit, dispatch, rootState }, id) => {
    try {
      let token = rootState.auth.token;
      await nakamalsApi.remove(token, id);
      commit('remove', id);
      dispatch('notify/add', {
        title: 'Kava Bar Removed',
        text: 'Kava bar removed from the system.',
        type: 'warning',
      }, { root: true });
    }
    catch (error) {
      console.log('! remove nakamal in catch');
      console.log(error);
      await dispatch('checkApiError', error);
    }
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
    let i = {
      ...item,
      latLng: latLng(item.lat, item.lng),
    };
    Vue.set(state.byId, i.id, i);
    if (state.allIds.includes(i.id)) return;
    state.allIds.push(i.id);
  },
  select: (state, id) => {
    state.selectedId = id;
  },
  unselect: (state) => {
    state.selectedId = null;
  },
  remove: (state, id) => {
    state.allIds.splice(state.allIds.indexOf(id), 1);
    Vue.delete(state.byId, id);
  }
};

export default {
  actions,
  getters,
  mutations,
  namespaced: true,
  state,
};
