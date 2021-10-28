/* eslint-disable */

import { latLng } from 'leaflet';

const initialState = () => ({
  location: null,
  bounds: null,
  center: latLng(-17.741526, 168.312024),
  zoom: 15,
  showNewNakamalMarker: false,
  showSearch: false,
  showDetails: false,
});

const state = initialState()

const getters = {
  location: (state) => {
    return state.location;
  },
  bounds: (state) => {
    return state.bounds;
  },
  center: (state) => {
    return state.center;
  },
  zoom: (state) => {
    return state.zoom;
  },
  showNewNakamalMarker: (state) => {
    return state.showNewNakamalMarker;
  },
  showSearch: (state) => {
    return state.showSearch;
  },
  showDetails: (state) => {
    return state.showDetails;
  },
};

const actions = {
  setLocation: async ({ commit }, location) => {
    commit('setLocation', location);
  },
  setBounds: async ({ commit }, bounds) => {
    commit('setBounds', bounds);
  },
  setCenter: async ({ commit }, center) => {
    commit('setCenter', center);
  },
  setZoom: async ({ commit }, zoom) => {
    commit('setZoom', zoom);
  },
  setShowNewNakamalMarker: async ({ commit }, show) => {
    commit('setShowNewNakamalMarker', show);
  },
  setShowSearch: async ({ commit }, show) => {
    commit('setShowSearch', show);
  },
  setShowDetails: async ({ commit }, show) => {
    commit('setShowDetails', show);
  },
};

const mutations = {
  RESET (state) {
    const newState = initialState()
    Object.keys(newState).forEach(key => {
      state[key] = newState[key]
    })
  },
  setLocation: (state, location) => {
    state.location = location;
  },
  setBounds: (state, bounds) => {
    state.bounds = bounds;
  },
  setCenter: (state, center) => {
    state.center = center;
  },
  setZoom: (state, zoom) => {
    state.zoom = zoom;
  },
  setShowNewNakamalMarker: (state, show) => {
    state.showNewNakamalMarker = show;
  },
  setShowSearch: (state, show) => {
    state.showSearch = show;
  },
  setShowDetails: (state, show) => {
    state.showDetails = show;
  },
};

export default {
  actions,
  getters,
  mutations,
  namespaced: true,
  state,
};
