import Vue from 'vue';
import dayjs from 'dayjs';

import { normalizeRelations, resolveRelations } from '@/store/helpers';
import checkinsApi from '@/api/checkins';
import nakamalsApi from '@/api/nakamals';
import usersApi from '@/api/users';
import i18n from '../../plugins/i18n';

const initialState = () => ({
  byId: {},
  byNakamalId: {},
  recentIds: [],
  allIds: [],
  filters: {},
});

const state = initialState();

const getters = {
  // Return a single checkin with the given id.
  find: (state, _, __, rootGetters) => id => {
    // Swap ID references with the resolved nakamal objects.
    return resolveRelations(state.byId[id], ['nakamal', 'user'], rootGetters);
  },
  // Return a list of checkins in the order of `allIds`.
  list: (state, getters) => {
    return state.allIds.map(id => getters.find(id));
  },
  filteredList: (state, getters) => {
    let checkins = state.allIds.map(id => getters.find(id));
    if ('user' in state.filters && state.filters.user !== null) {
      checkins = checkins.filter((c) => c.user.id === state.filters.user);
    }
    if ('dt' in state.filters && state.filters.dt !== null) {
      checkins = checkins.filter((c) => state.filters.dt.isBefore(dayjs(c.created_at)));
    } else {
      // set default 60 day filter for heatmap
      checkins = checkins.filter((c) => dayjs().subtract(60, 'd').isBefore(dayjs(c.created_at)));
    }
    return checkins;
  },
  filters: (state) => {
    return state.filters;
  },
  hasFilters: (state) => {
    return Object.keys(state.filters).length > 0;
  },
  // Return a list of recent checkins.
  recent: (state, getters) => {
    // return state.allIds.map(id => getters.find(id)).filter(c => c.created_at)
    return state.recentIds.map(id => getters.find(id));
  },
  recentNakamalIds: (state, getters) => {
    return [...new Set(getters.recent.map((c) => c.nakamal.id))];
  },
  // Return a list of checkins of a nakamal.
  nakamal: (state, getters) => nakamalId => {
    if (!state.byNakamalId[nakamalId]) return [];
    return state.byNakamalId[nakamalId].map(id => getters.find(id));
  },
  // Return a list of checkins of a user.
  user: (state, getters) => userId => {
    return state.allIds.map(id => getters.find(id)).filter(c => c.user.id === userId);
  },
};

function commitAddCheckin(checkin, commit) {
  // Normalize nested data and swap the nakamal object
  // in the API response with an ID reference.
  commit('add', normalizeRelations(checkin, ['nakamal', 'user']));
  // Add or update relations.
  if (checkin.nakamal.chief) {
    commit('user/setUser', checkin.nakamal.chief, {
      root: true,
    });
  }
  commit('nakamal/add', normalizeRelations(checkin.nakamal, ['chief']), {
    root: true,
  });
  commit('user/setUser', checkin.user, {
    root: true,
  });
};

const actions = {
  getAll: async ({ commit }) => {
    const response = await checkinsApi.getAll();
    const checkins = response.data;
    checkins.forEach((item) => {
      commitAddCheckin(item, commit);
    });
  },
  getOne: async ({ commit }, id) => {
    let response = await checkinsApi.get(id);
    const checkin = response.data;
    commitAddCheckin(checkin, commit);
  },
  getRecent: async ({ commit }) => {
    const threshold = 3; // XXX hardcoded value
    try {
      const response = await checkinsApi.getRecent();
      let items = response.data;
      if (!items.length < threshold) {
        const response = await checkinsApi.getAll({ limit: threshold })
        items = response.data;
      }
      items.forEach((item) => {
        commitAddCheckin(item, commit);
      });
      commit('setRecentIds', items.map((i) => i.id));
    } catch (error) {
      console.log('recent checkin error', error);
    }
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
      const response = await checkinsApi.create(token, payload);
      console.log('resp', response);
      const checkin = response.data;
      commitAddCheckin(checkin, commit);
      commit('addRecentId', checkin.id);
      dispatch('notify/add', {
        title: i18n.t('checkin.alert.create_title'),
        text: i18n.t('checkin.alert.create_body'),
        type: 'primary',
      }, { root: true });
    }
    catch (error) {
      console.log('error in add checkin', error);
      await dispatch('auth/checkApiError', error, { root: true });
    }
  },
  remove: async ({ commit, dispatch, rootState }, id) => {
    try {
      let token = rootState.auth.token;
      await checkinsApi.remove(token, id);
      commit('remove', id);
      dispatch('notify/add', {
        title: i18n.t('checkin.alert.remove_title'),
        text: i18n.t('checkin.alert.remove_body'),
        type: 'warning',
      }, { root: true });
    }
    catch (error) {
      console.log('Check-in remove error');
      await dispatch('auth/checkApiError', error, { root: true });
    }
  },
  setFilter: ({ commit }, { key, value }) => {
    commit('setFilter', { key, value });
  },
  removeFilters: ({ commit }) => {
    commit('removeFilters');
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
  remove: (state, id) => {
    let index;
    const nId = state.byId[id].nakamal;
    index= state.byNakamalId[nId].indexOf(id)
    if (index !== -1) {
      state.byNakamalId[nId].splice(index, 1);
    } 
    index = state.recentIds.indexOf(id);
    if (index !== -1) {
      state.recentIds.splice(index, 1);
    }
    state.allIds.splice(state.allIds.indexOf(id), 1);
    Vue.delete(state.byId, id);
  },
  addRecentId: (state, id) => {
    state.recentIds.unshift(id);
  },
  setRecentIds: (state, ids) => {
    state.recentIds = ids;
  },
  setFilter: (state, { key, value }) => {
    Vue.set(state.filters, key, value);
  },
  removeFilters: (state) => {
    Vue.set(state, 'filters', {});
  }, };

export default {
  actions,
  getters,
  mutations,
  namespaced: true,
  state,
};
