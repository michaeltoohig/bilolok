/* eslint-disable */

import Vue from 'vue';

import { normalizeRelations, resolveRelations } from '@/store/helpers';
import checkinsApi from '@/api/checkins';
import nakamalsApi from '@/api/nakamals';
import usersApi from '@/api/users';

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
    return resolveRelations(state.byId[id], ['nakamal', 'user'], rootGetters);
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
  // consider calculating in the component not here in store
  countToday: (state, getters) => nakamalId => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);  // last midnight
    return getters.nakamal(nakamalId).filter((c) => {
      const date = new Date(c.created_at);
      return today <= date
    }).length;
  },
  // consider calculating in the component not here in store
  countMonth: (state, getters) => nakamalId => {
    const month = new Date();
    month.setDate(month.getDate() - 30);
    month.setHours(0, 0, 0, 0);  // Set to midnight
    return getters.nakamal(nakamalId).filter((c) => {
      const date = new Date(c.created_at);
      return month <= date
    }).length;
  },
  // Return a list of checkins of a user.
  // TODO filter by `user` when API response includes an user object that will need to be resolved
  user: (state, getters) => userId => {
    return state.allIds.map(id => getters.find(id)).filter(c => c.user.id === userId);
  },
};

function commitAddCheckin(checkin, commit) {
  // Normalize nested data and swap the nakamal object
  // in the API response with an ID reference.
  commit('add', normalizeRelations(checkin, ['nakamal', 'user']));
  // // Add or update the nakamal.
  commit('nakamal/add', checkin.nakamal, {
    root: true,
  });
  commit('user/setUser', checkin.user, {
    root: true,
  });
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
  getUser: async ({ commit }, userId) => {
    const response = await usersApi.getCheckins(userId);
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
      await dispatch('auth/checkApiError', error, { root: true });
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
