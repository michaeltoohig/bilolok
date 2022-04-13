/* eslint-disable */

import { latLng } from 'leaflet';

const initialState = () => ({
  location: null,
  showLocationProgress: false,
  bounds: null,
  center: latLng(-17.741526, 168.312024),
  zoom: 15,
  showNewNakamalMarker: false,
  showHeatmap: false,
  showHeatmapMenu: false,
  showFilters: false,
  showSearch: false,
  showDetails: false,
  // showDistance: null,
  watchId: null,
  compassMode: false,
  skipCompassModeIntro: false,
  compassModePolyline: [],
});

const state = initialState()

const getters = {
  location: (state) => {
    return state.location;
  },
  showLocationProgress: (state) => {
    return state.showLocationProgress;
  },
  compassMode: (state) => {
    return state.compassMode;
  },
  skipCompassModeIntro: (state) => {
    return state.skipCompassModeIntro;
  },
  compassModePolyline: (state) => {
    return state.compassModePolyline;
  },
  showHeatmap: (state) => {
    return state.showHeatmap;
  },
  watchId: (state) => {
    return state.watchId;
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
  showHeatmap: (state) => {
    return state.showHeatmap;
  },
  showHeatmapMenu: (state) => {
    return state.showHeatmapMenu;
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
  startCompassMode: async ({ commit, dispatch, getters }) => {
    if (!('geolocation' in navigator)) {
      await dispatch('notify/add', {
        title: 'Location Not Available',
        text: 'Your device does not provide location or you have blocked location access.',
        color: 'info',
        duration: 5_000,
      }, { root: true });
      return;
    }
    commit('skipCompassModeIntro');
    await dispatch('startWatcher');
    commit('setCompassMode', true);
  },
  stopCompassMode: async ({ commit, dispatch }) => {
    commit('setCompassMode', false);
    await dispatch('clearWatcher');
  },
  startWatcher: async ({ commit, dispatch }) => {
    await dispatch('clearWatcher');
    const watchId = navigator.geolocation.watchPosition(position => {
      commit('setLocation', position.coords);
      commit('appendCompassModePolyline', position.coords);
    }, error => {
      console.log(error);
    }, {
      enableHighAccuracy: true,
    });
    commit('setWatchId', watchId);
  },
  clearWatcher: async ({ commit, getters }) => {
    const watchId = getters.watchId;
    if (watchId !== null) {
      console.log("clearing position watcher")
      navigator.geolocation.clearWatch(watchId);
    }
    commit('clearCompassModePolyline');
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
  setShowHeatmap: async ({ commit, dispatch }, show) => {
    commit('setShowHeatmap', show);
    if (show) {
      await dispatch('checkin/getAll', {}, { root: true });
    }
  },
  setShowHeatmapMenu: async ({ commit }, show) => {
    commit('setShowHeatmapMenu', show);
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
  setCompassMode: (state, value) => {
    state.compassMode = value;
  },
  skipCompassModeIntro: (state) => {
    state.skipCompassModeIntro = true;
  },
  appendCompassModePolyline: (state, location) => {
    state.compassModePolyline.push({
      lat: location.latitude,
      lng: location.longitude,
      at: new Date().getTime(),
    });
  },
  clearCompassModePolyline: (state) => {
    state.compassModePolyline = [];
  },
  setWatchId: (state, id) => {
    state.watchId = id;
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
  setShowHeatmap: (state, show) => {
    state.showHeatmap = show;
  },
  setShowHeatmapMenu: (state, show) => {
    state.showHeatmapMenu = show;
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
