import Vue from 'vue';
import nakamalsApi from '@/api/nakamals';
import { latLng } from 'leaflet';

const initialState = () => ({
  byId: [],
  allIds: [],
  selectedId: null,
});

const state = initialState();

const getters = {
  get: (state, _, __, rootGetters) => id => {
    return state.byId[id];
  },
  selected: (state, getters) => {
    if (state.selectedId === null) return null;
    return getters.get(state.selectedId);
  },
};

const actions = {
  fetch: async ({ commit, dispatch, getters }, id) => {
    try {
      let resp = await nakamalsApi.get(id);
      commit('ADD', resp.data);
    } catch (err) {
      console.error('nakamal load error');
      throw err;
    }
  },
  select: async ({ commit, dispatch }, id) => {
    commit('SELECT', id);
  },
}

const mutations = {
  ADD (context, nakamal) {
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
    state.selectedId = id;
  },
};

export default {
  actions,
  getters,
  mutations,
  namespaced: true,
  state,
};