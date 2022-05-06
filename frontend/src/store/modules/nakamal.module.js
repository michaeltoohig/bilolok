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
  featuredId: null,
  filters: {},
});

const state = initialState();

const getters = {
  // Return a single nakamal with the given id.
  find: (state, _, __, rootGetters) => id => {
    // Swap ID referenes with the resolved image objects.
    return resolveRelations(state.byId[id], ['image'], rootGetters);
  },
  // Return a list of nakamals in the order of `allIds`.
  list: (state, getters) => {
    return state.allIds.map(id => getters.find(id));
  },
  filteredList: (state, getters) => {
    let nakamals = state.allIds.map(id => getters.find(id));
    if ('area' in state.filters) {
      nakamals = nakamals.filter((n) => n.area.id === state.filters.area);
    }
    if ('light' in state.filters) {
      nakamals = nakamals.filter((n) => n.light === state.filters.light);
    }
    if ('resources' in state.filters) {
      if (state.filters.resources.length > 0) {
        nakamals = nakamals.filter((n) => {
          if (n.resources.length > 0) {
            return state.filters.resources.every((rid) => n.resources.map((r) => r.id).indexOf(rid) > -1);
          }
        });
      }
    }
    if ('kava_source' in state.filters) {
      nakamals = nakamals.filter((n) => n.kava_source.id === state.filters.kava_source);
    }
    return nakamals;
  },
  filters: (state) => {
    return state.filters;
  },
  hasFilters: (state) => {
    return Object.keys(state.filters).length > 0;
  },
  total: (state) => {
    return state.allIds.length;
  },
  selected: (state, getters) => {
    if (state.selectedId === null) return null;
    return getters.find(state.selectedId);
  },
  featured: (state, getters) => {
    if (state.featuredId === null) return null;
    return getters.find(state.featuredId);
  }
};

function commitAddNakamal(nakamal, commit) {
  // Normalize nested data and swap the image object
  // in the API response with an ID reference.
  commit('add', normalizeRelations(nakamal, []));
};

const actions = {
  load: async ({ commit }) => {
    const response = await nakamalsApi.getAll({});
    const nakamals = response.data
    nakamals.forEach((item) => {
      commitAddNakamal(item, commit);
    });
  },
  loadOne: async ({ commit, dispatch }, id) => {
    try {
      let response = await nakamalsApi.get(id);
      const nakamal = response.data;
      commitAddNakamal(nakamal, commit);
      // Perhaps do not assume we want to load all right away
      dispatch('load');  // Load all others in background
    }
    catch (error) {
      console.log(error, 'error in catch loadOne');
      await dispatch('auth/checkApiError', error, { root: true });
    }
  },
  update: async ({ commit, dispatch, rootState }, { nakamalId, payload }) => {
    try {
      let token = rootState.auth.token;
      const response = await nakamalsApi.update(token, nakamalId, payload);
      const nakamal = response.data;
      commitAddNakamal(nakamal, commit);
      dispatch('notify/add', {
        title: 'Success',
        text: 'Nakamal details have been updated.',
        type: 'primary',
        duration: 5_000,
      }, { root: true });
    }
    catch (error) {
      console.log('in update nakamal error', error);
      await dispatch('auth/checkApiError', error, { root: true });
    }
  },
  updateResources: async ({ commit, rootState }, { nakamalId, oldResources, resources }) => {
    try {
      const token = rootState.auth.token;
      const deleteList = oldResources.filter(id => resources.indexOf(id) === -1);
      const putlist = resources.filter(id => oldResources.indexOf(id) === -1);
      deleteList.forEach(id => {
        nakamalsApi.deleteResource(token, nakamalId, id);
      });
      putlist.forEach(id => {
        nakamalsApi.putResource(token, nakamalId, id);
      });
    }
    catch (error) {
      console.log('in update nakamal resource error', error);
      await dispatch('auth/checkApiError', error, { root: true });
    }
  },
  add: async ({ commit, dispatch, rootState }, payload) => {
    try {
      let token = rootState.auth.token;
      // Extract resources from payload if exists
      let resources = [];
      if ('resources' in payload) {
        resources = payload.resources;
        delete payload.resources;
      }
      // POST new nakamal
      let response = await nakamalsApi.create(token, payload);
      const nakamal = response.data;
      // PUT resources to new nakamal
      if (resources.length) {
        for (let i = 0; i < resources.length; i += 1) {
          await nakamalsApi.putResource(token, nakamal.id, resources[i]);
        };
      }
      commitAddNakamal(nakamal, commit);
      dispatch('notify/add', {
        title: 'Kava Bar Added',
        text: 'Thank you for sharing!',
        type: 'primary',
      }, { root: true });
    }
    catch (error) { 
      await dispatch('auth/checkApiError', error, { root: true });
    }
  },
  loadFeatured: async ({ commit }) => {
    const response = await nakamalsApi.getFeatured();
    const nakamal = response.data;
    commitAddNakamal(nakamal, commit);
    commit('setFeatured', nakamal.id);
  },
  setFeatured: async ({ commit }, id) => {
    await nakamalsApi.putFeatured(id);
    commit('setFeatured', id);
  },
  select: async ({ commit }, id) => {
    commit('select', id);
  },
  unselect: async ({ commit }) => {
    commit('unselect');
  },
  setFilter: ({ commit }, { key, value }) => {
    commit('setFilter', { key, value });
  },
  removeFilters: ({ commit }) => {
    commit('removeFilters');
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
      await dispatch('auth/checkApiError', error, { root: true });
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
  setFeatured: (state, id) => {
    state.featuredId = id;
  },
  setFilter: (state, { key, value }) => {
    if (value === []) {
      Vue.delete(state.filters, 'resources');
    }
    else {
      Vue.set(state.filters, key, value);
    }
  },
  removeFilters: (state) => {
    Vue.set(state, 'filters', {});
  },
  remove: (state, id) => {
    state.allIds.splice(state.allIds.indexOf(id), 1);
    Vue.delete(state.byId, id);
    state.selectedId = null;  // XXX why do this?
  }
};

export default {
  actions,
  getters,
  mutations,
  namespaced: true,
  state,
};
