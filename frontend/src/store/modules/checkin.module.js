import Vue from 'vue';
import dayjs from 'dayjs';
import ls from 'localstorage-slim';

import { normalizeRelations, renameRelation, resolveRelations } from '@/store/helpers';
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
    // return resolveRelations(state.byId[id], ['nakamal', 'user'], rootGetters);
    return state.byId[id];
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
    return state.allIds.map(id => getters.find(id)).filter(c => c.user === userId);
  },
  favoriteNakamals: (state, getters) => userId => {
    let checkins = getters.user(userId);
    const count = {};
    const threshold = dayjs().subtract(30, 'd');
    checkins = checkins.filter((c) => threshold.isBefore(dayjs(c.created_at)));
    checkins.forEach((c) => {
      const nId = c.nakamal;
      if (Object.keys(count).includes(nId)) {
        count[nId].count += 1;
        if (dayjs(count[nId].created_at).isBefore(c.created_at)) {
          count[nId].created_at = c.created_at;
        }
      } else {
        count[nId] = {
          count: 1,
          created_at: c.created_at,
          nakamal: c.nakamal,
        };
      }
    });
    const sorted = Object.values(count).sort((a, b) => {
      if (a.count === b.count) {
        return dayjs(b.created_at).isBefore(dayjs(a.created_at)) ? -1 : 1;
      }
      return a.count > b.count ? -1 : 1;
    });
    return sorted.slice(0, 3);
  },
};

function commitAddCheckin(checkin, commit) {
  // Normalize nested data and swap the nakamal object
  // in the API response with an ID reference.
  // commit('add', normalizeRelations(checkin, ['nakamal', 'user']));
  commit('add', renameRelation(checkin, [['nakamal_id', 'nakamal'], ['user_id', 'user']]));
  
  // Add or update relations.
  // if (checkin.nakamal.chief) {
  //   commit('user/setUser', checkin.nakamal.chief, {
  //     root: true,
  //   });
  // }
  // commit('nakamal/add', normalizeRelations(checkin.nakamal, ['chief']), {
  //   root: true,
  // });
  // commit('user/setUser', checkin.user, {
  //   root: true,
  // });
};

const actions = {
  load: async ({ commit }) => {
    const cacheKey = 'checkins';
    const cached = false; // ls.get('does-not-exist'); // cacheKey - replaced to remove cache
    if (cached) {
      return;
    } else {
      const resp = await checkinsApi.getAll();
      const checkins = resp.data;
      checkins.forEach((item) => {
        commitAddCheckin(item, commit);
      });
      // ls.set(cacheKey, true, { ttl: 300 });
    }
  },
  loadOne: async ({ commit, getters }, id) => {
    // TODO handle network errors
    let checkin;
    const cacheKey = `checkins:${id}`;
    const cached = false; // ls.get('does-not-exist'); // cacheKey - replaced to remove cache
    if (cached) {
      checkin = cached;
    } else {
      const resp = await checkinsApi.get(id);
      checkin = resp.data;
      // ls.set(cacheKey, checkin, { ttl: 300 });
    }
    commitAddCheckin(checkin, commit);
    return Promise.resolve(getters.find(id));
  },
  getRecent: async ({ commit }) => {
    let items;
    const cacheKey = 'checkins:recent';
    const cached = false; // ls.get('does-not-exist'); // cacheKey - replaced to remove cache
    if (cached) {
      return;
    } else {
      const resp = await checkinsApi.getRecent();
      items = resp.data;
      const threshold = 3; // XXX hardcoded value
      if (items.length < threshold) {
        const resp = await checkinsApi.getAll({ limit: threshold })
        items = resp.data;
      }
      items.forEach((item) => {
        commitAddCheckin(item, commit);
      });
      commit('setRecentIds', items.map((i) => i.id));
      // ls.set(cacheKey, true, { ttl: 60 });  
    }
  },
  getNakamal: async ({ commit }, nakamalId) => {
    const cacheKey = `checkins:nakamal:${nakamalId}`;
    const cached = false; // ls.get('does-not-exist'); // cacheKey - replaced to remove cache
    if (cached) {
      return;
    } else {
      const resp = await nakamalsApi.getCheckins(nakamalId);
      const checkins = resp.data;
      checkins.forEach((item) => {
        commitAddCheckin(item, commit);
      });
      // ls.set(cacheKey, true, { ttl: 300 });
    }
  },
  getUser: async ({ commit }, userId) => {
    const cacheKey = `checkins:user:${userId}`;
    const cached = false; // ls.get('does-not-exist'); // cacheKey - replaced to remove cache
    if (cached) {
      return;
    } else {
      const resp = await usersApi.getCheckins(userId);
      const checkins = resp.data;
      checkins.forEach((item) => {
        commitAddCheckin(item, commit);
      });
      // ls.set(cacheKey, true, { ttl: 300 });
    }
  },
  add: async ({ commit, dispatch, rootState }, payload) => {
    try {
      let token = rootState.auth.token;
      const resp = await checkinsApi.create(token, payload);
      console.log('resp', resp);
      const checkin = resp.data;
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
