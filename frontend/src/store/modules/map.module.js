/* eslint-disable */

import { latLng } from 'leaflet';

const initialState = () => ({
  location: null,
  showLocationProgress: false,
  bounds: null,
  center: latLng(-17.741526, 168.312024),
  zoom: 15,
  showNewNakamalMarker: false,
  showFilters: false,
  showSearch: false,
  showDetails: false,

  showDistance: null,
});

const state = initialState()

const getters = {
  location: (state) => {
    return state.location;
  },
  showLocationProgress: (state) => {
    return state.showLocationProgress;
  },
  // showDistance: (state) => {
  //   return state.showDistance;
  // },
  // showDistanceLine: (state) => {
  //   if (!state.showDistance) return [];
  //   return [
  //     [
  //       state.showDistance.from.lat,
  //       state.showDistance.from.lng,
  //     ],
  //     [
  //       state.showDistance.to.lat,
  //       state.showDistance.to.lng,
  //     ],
  //   ];
  // },
  // displayDistance: (state) => {
  //   if (!state.showDistance) return null;
  //   let distance = Math.round(latLng(
  //     state.showDistance.from.lat,
  //     state.showDistance.from.lng,
  //   ).distanceTo(latLng(
  //     state.showDistance.to.lat,
  //     state.showDistance.to.lng,
  //   )));
  //   if (distance < 1000) {
  //     distance = `${distance} meters`
  //   } else {
  //     distance = (distance / 1000).toFixed(1);
  //     distance = `${distance} kilometers`
  //   }
  //   return distance;
  // },
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
  showFilters: (state) => {
    return state.showFilters;
  },
  showSearch: (state) => {
    return state.showSearch;
  },
  showDetails: (state) => {
    return state.showDetails;
  },
};

const actions = {
  RESET: ({ commit }) => {
    commit('RESET');
  },
  setLocation: async ({ commit }, location) => {
    commit('setLocation', location);
  },
  setShowLocationProgress: async ({ commit }, show) => {
    commit('setShowLocationProgress', show);
  },
  // setShowDistance: async ({ commit }, { from, to }) => {
  //   commit('setShowDistance', { from, to });
  // },
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
  setShowFilters: async ({ commit }, show) => {
    commit('setShowFilters', show);
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
  setShowLocationProgress: (state, show) => {
    state.showLocationProgress = show;
  },
  // setShowDistance: (state, payload) => {
  //   state.showDistance = payload;
  // },
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
  setShowFilters: (state, show) => {
    state.showFilters = show;
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
