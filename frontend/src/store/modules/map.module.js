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
  showCompass: false,
  watchId: null,
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
  showCompass: (state) => {
    return state.showCompass;
  },
  watchId: (state) => {
    return state.watchId;
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
  setShowCompass: async ({ commit, dispatch }, show) => {
    if (!('geolocation' in navigator)) {
      await dispatch('notify/add', {
        title: 'Location Not Available',
        text: 'Your device does not provide location or you have blocked location access.',
        color: 'info',
        duration: 5_000,
      }, { root: true });
      return;
    }
    commit('setShowCompass', show);
    if (show) {
      await dispatch('clearWatcher');
      const watchId = navigator.geolocation.watchPosition(position => {
        commit('setLocation', position.coords);
      }, error => {
        console.log(error);
      }, {
        enableHighAccuracy: true,
      });
      commit('setWatchId', watchId);
    } else {
      await dispatch('clearWatcher');
    }
  },
  clearWatcher: async ({ getters }) => {
    const watchId = getters.watchId;
    if (watchId !== null) {
      console.log(watchId);
      navigator.geolocation.clearWatch(watchId);
    }
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
    console.log('zzz', location.heading, location);
    state.location = location;
  },
  setShowLocationProgress: (state, show) => {
    state.showLocationProgress = show;
  },
  setShowCompass: (state, show) => {
    state.showCompass = show;
  },
  setWatchId: (state, id) => {
    state.watchId = id;
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
