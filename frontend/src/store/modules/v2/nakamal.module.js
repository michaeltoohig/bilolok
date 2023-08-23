import Vue from 'vue';
import nakamalsApi from '@/api/nakamals';
import { latLng } from 'leaflet';

const initialState = () => ({
  byId: [],
  allIds: [],
  selectedId: null, // the currently active nakamal (not featured or something else)
});

const state = initialState();

const getters = {
  get: (state) => id => {
    return state.byId[id];
  },
  selected: (state, getters) => {
    if (state.selectedId === null) return null;
    return getters.get(state.selectedId);
  },
  timeline: (state) => {
    return state.timeline;
  },
};

const actions = {
  fetch: async ({ commit, dispatch, getters }, id) => {
    try {
      let resp = await nakamalsApi.get(id);
      commit('ADD', resp.data);
    } catch (err) {
      console.error('nakamal load error', err);
      throw err;
    }
  },
  select: async ({ commit, dispatch }, id) => {
    commit('SELECT', id);
  },
  fetchTimeline: async ({ commit }, id) => {
    try {
      const resp = await nakamalsApi.getTimeline(id);
      commit('TIMELINE', resp.data);
    } catch (err) {
      console.error('nakamal timeline load error', err);
      throw err;
    }
  }
}

const mutations = {
  ADD: (state, nakamal) => {
    let i = {
      ...nakamal,
      latLng: latLng(nakamal.lat, nakamal.lng),
      // lightBadge: null,
    };
    Vue.set(state.byId, i.id, i);
    if (state.allIds.includes(i.id)) return;
    state.allIds.push(i.id);
  },
  SELECT: (state, id) => {
    // reset previously selected nakamal state
    state.timeline = undefined;
    // set the ID for the selected ID now that state is reset
    state.selectedId = id;
  },
  TIMELINE: (state, items) => {
    state.timeline = items;
  },
};

export default {
  actions,
  getters,
  mutations,
  namespaced: true,
  state,
};