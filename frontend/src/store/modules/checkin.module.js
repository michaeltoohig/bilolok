/* eslint-disable */

import Vue from 'vue';

import { normalizeRelations, resolveRelations } from '@/store/helpers';
import checkinsApi from '@/api/checkins';
import nakamalsApi from '@/api/nakamals';

const initialState = () => ({
  byId: {},
  byNakamalId: {},
  recentIds: [],
  allIds: [],
});

const state = initialState();

const getters = {
  // Return a single image with the given id.
  find: (state, _, __, rootGetters) => id => {
    // Swap ID references with the resolved nakamal objects.
    // return resolveRelations(state.byId[id], ['nakamal'], rootGetters);
    return state.byId[id];
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
  countToday: (state, getters) => nakamalId => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);  // last midnight
    return getters.nakamal(nakamalId).filter((c) => {
      const date = new Date(c.created_at);
      return today <= date
    }).length;
  },
  countMonth: (state, getters) => nakamalId => {
    const month = new Date();
    month.setDate(month.getDate() - 30);
    month.setHours(0, 0, 0, 0);  // Set to midnight
    return getters.nakamal(nakamalId).filter((c) => {
      const date = new Date(c.created_at);
      return month <= date
    }).length;
  },
};

function commitAddCheckin(checkin, commit) {
  // Normalize nested data and swap the nakamal object
  // in the API response with an ID reference.
  commit('add', normalizeRelations(checkin, ['user', 'nakamal']));
  // // Add or update the nakamal.
  // if (checkin.nakamal) {
  //   commit('nakamal/add', checkin.nakamal, {
  //     root: true,
  //   });
  // }

  // the below load nakamal call here is bad; it causes an API
  // request for every checkin which means when loading checkins
  // for a single kava bar it will try to load the kava bar over
  // and over again in a short period.
  // Probably best to call the load nakamal action only when it
  // may be needed.
  // dispatch('nakamal/loadOne', checkin.nakamal.id, { root: true });
};

const actions = {
  getRecent: async ({ commit }) => {
    const response = await checkinsApi.getRecent();
    const checkins = response.data;
    checkins.forEach((item) => {
      commitAddCheckin(item, commit);
    });
    commit('setRecentIds', checkins.map(i => i.id));
  },
  getNakamal: async ({ commit }, nakamalId) => {
    const response = await nakamalsApi.getCheckins(nakamalId);
    const checkins = response.data;
    checkins.forEach((item) => {
      commitAddCheckin(item, commit);
    });
  },
  add: async ({ commit, dispatch, rootState }, payload) => {
    try {
      let token = rootState.auth.token;
      let response = await checkinsApi.create(token, payload);
      const checkin = response.data;
      commitAddCheckin(checkin, commit);
      dispatch('notify/add', {
        title: 'Checked-In!',
        text: `You are checked-in to this kava bar.`,
        type: 'primary',
      }, { root: true });
    }
    catch (error) {
      dispatch('notify/add', {
        title: 'Not Allowed',
        text: error.response.data.detail,
        type: 'warning',
      }, { root: true });
    }
  },
};

const mutations = {
  RESET(state) {
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
