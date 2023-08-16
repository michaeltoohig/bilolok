/* eslint-disable */

import Vue from 'vue';
import dayjs from 'dayjs';
import ls from 'localstorage-slim';

import { normalizeRelations, resolveRelations } from '@/store/helpers';
import tripsApi from '@/api/trips';
import nakamalsApi from '@/api/nakamals';
import usersApi from '@/api/users';
import i18n from '../../plugins/i18n';

const initialState = () => ({
  byId: {},
  byNakamalId: {},
  recentIds: [],
  allIds: [],
  // filters: {},
});

const state = initialState();

const getters = {
  // Return a single image with the given id.
  find: (state, _, __, rootGetters) => id => {
    // Swap ID references with the resolved nakamal objects.
    // return resolveRelations(state.byId[id], ['nakamal', 'user'], rootGetters);
    return state.byId[id];
  },
  // Return a list of images in the order of `allIds`.
  list: (state, getters) => {
    return state.allIds.map(id => getters.find(id));
  },
  // filteredList: (state, getters) => {
  //   let trips = state.allIds.map(id => getters.find(id));
  //   if ('user' in state.filters && state.filters.user !== null) {
  //     trips = trips.filter((c) => c.user.id === state.filters.user);
  //   }
  //   if ('dt' in state.filters && state.filters.dt !== null) {
  //     trips = trips.filter((c) => state.filters.dt.isBefore(dayjs(c.created_at)));
  //   } else {
  //     // set default 30 day filter for heatmap
  //     trips = trips.filter((c) => dayjs().subtract(30, 'd').isBefore(dayjs(c.created_at)));
  //   }
  //   return trips;
  // },
  // filters: (state) => {
  //   return state.filters;
  // },
  // hasFilters: (state) => {
  //   return Object.keys(state.filters).length > 0;
  // },
  // Return a list of recent images.
  recent: (state, getters) => {
    // return state.allIds.map(id => getters.find(id)).filter(c => c.created_at)
    return state.recentIds.map(id => getters.find(id));
  },
  recentNakamalIds: (state, getters) => {
    return [...new Set(getters.recent.map((c) => c.nakamal.id))];
  },
  // Return a list of images of a nakamal.
  nakamal: (state, getters) => nakamalId => {
    if (!state.byNakamalId[nakamalId]) return [];
    return state.byNakamalId[nakamalId].map(id => getters.find(id));
  },
  // Return a list of trips of a user.
  user: (state, getters) => userId => {
    return state.allIds.map(id => getters.find(id)).filter(c => c.user === userId);
  },
};

function commitAddTrip(trip, commit) {
  // Normalize nested data and swap the nakamal object
  // in the API response with an ID reference.
  commit('add', normalizeRelations(trip, ['nakamal', 'user']));
  // Add or update relations
  // commit('user/setUser', trip.user, {
  //   root: true,
  // });
  // if (trip.nakamal.chief) {
  //   commit('user/setUser', trip.nakamal.chief, {
  //     root: true,
  //   });
  // }
  // commit('nakamal/add', normalizeRelations(trip.nakamal, ['chief']), {
  //   root: true,
  // });
};

const actions = {
  load: async ({ commit }) => {
    const cacheKey = 'trips';
    const cached = false; // ls.get('does-not-exist'); // cacheKey - replaced to remove cache
    if (cached) {
      return;
    } else {
      const trips = await tripsApi.getAll();
      trips.forEach((item) => {
        commitAddTrip(item, commit);
      });
      // ls.set(cacheKey, true, { ttl: 300 });
    }
  },
  loadOne: async ({ commit, getters }, id) => {
    // TODO handle network errors
    let trip;
    const cacheKey = `trips:${id}`;
    const cached = false; // ls.get('does-not-exist'); // cacheKey - replaced to remove cache
    if (cached) {
      trip = cached;
    } else {
      const resp = await tripsApi.get(id);
      trip = resp.data;
      // ls.set(cacheKey, trip, { ttl: 300 });
    }
    commitAddTrip(trip, commit);
    return Promise.resolve(getters.find(id));
  },
  getRecent: async ({ commit }) => {
    let items;
    const cacheKey = 'trips:recent';
    const cached = false; // ls.get('does-not-exist'); // cacheKey - replaced to remove cache
    if (cached) {
      return;
    } else {
      const resp = await tripsApi.getRecent();
      items = resp.data;
      const threshold = 3; // XXX hardcoded value
      if (items.length < threshold) {
        const resp = await tripsApi.getAll({ limit: threshold })
        items = resp.data;
      }
      items.forEach((item) => {
        commitAddTrip(item, commit);
      });
      commit('setRecentIds', items.map((i) => i.id));
      // ls.set(cacheKey, true, { ttl: 60 });
    }
  },
  getNakamal: async ({ commit }, nakamalId) => {
    const cacheKey = `trips:nakamal:${nakamalId}`;
    const cached = false; // ls.get('does-not-exist'); // cacheKey - replaced to remove cache
    if (cached) {
      return;
    } else {
      const resp = await nakamalsApi.getTrips(nakamalId);
      const trips = resp.data;
      trips.forEach((item) => {
        commitAddTrip(item, commit);
      });
      // ls.set(cacheKey, true, { ttl: 300 });
    }
  },
  getUser: async ({ commit }, userId) => {
    const cacheKey = `trips:user:${userId}`;
    const cached = false; // ls.get('does-not-exist'); // cacheKey - replaced to remove cache
    if (cached) {
      return;
    } else {
      const resp = await usersApi.getTrips(userId);
      const trips = resp.data;
      trips.forEach((item) => {
        commitAddTrip(item, commit);
      });
      // ls.set(cacheKey, true, { ttl: 300 });
    }
  },
  add: async ({ commit, dispatch, rootState }, payload) => {
    try {
      let token = rootState.auth.token;
      const trip = await tripsApi.create(token, payload);
      commitAddTrip(trip, commit);
      commit('addRecentId', trip.id);
      dispatch('notify/add', {
        title: i18n.t('trip.alert.create_title'),
        text: i18n.t('trip.alert.create_body'),
        color: 'primary',
        duration: 5_000,
      }, { root: true });
    }
    catch (error) {
      await dispatch('auth/checkApiError', error, { root: true });
    }
  },
  remove: async ({ commit, dispatch, rootState }, id) => {
    try {
      let token = rootState.auth.token;
      await tripsApi.remove(token, id);
      commit('remove', id);
      dispatch('notify/add', {
        title: i18n.t('trip.alert.remove_title'),
        text: i18n.t('trip.alert.remove_body'),
        type: 'warning',
      }, { root: true });
    }
    catch (error) {
      console.log('Trip remove error');
      await dispatch('auth/checkApiError', error, { root: true });
    }
  },
  // setFilter: ({ commit }, { key, value }) => {
  //   commit('setFilter', { key, value });
  // },
  // removeFilters: ({ commit }) => {
  //   commit('removeFilters');
  // },
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
    index = state.byNakamalId[nId].indexOf(id);
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
  // setFilter: (state, { key, value }) => {
  //   Vue.set(state.filters, key, value);
  // },
  // removeFilters: (state) => {
  //   Vue.set(state, 'filters', {});
  // },
};

export default {
  actions,
  getters,
  mutations,
  namespaced: true,
  state,
};
