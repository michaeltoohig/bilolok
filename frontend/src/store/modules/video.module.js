/* eslint-disable */

import Vue from 'vue';

import { normalizeRelations, resolveRelations } from '@/store/helpers';
import videosApi from '@/api/videos';
import nakamalsApi from '@/api/nakamals';
import usersApi from '@/api/users';

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
    return resolveRelations(state.byId[id], ['nakamal', 'user'], rootGetters);
  },
  // Return a list of videos in the order of `allIds`.
  list: (state, getters) => {
    return state.allIds.map(id => getters.find(id));
  },
  // filteredList: (state, getters) => {
  //   let videos = state.allIds.map(id => getters.find(id));
  //   if ('user' in state.filters && state.filters.user !== null) {
  //     videos = videos.filter((c) => c.user.id === state.filters.user);
  //   }
  //   if ('dt' in state.filters && state.filters.dt !== null) {
  //     videos = videos.filter((c) => state.filters.dt.isBefore(dayjs(c.created_at)));
  //   } else {
  //     // set default 30 day filter for heatmap
  //     videos = videos.filter((c) => dayjs().subtract(30, 'd').isBefore(dayjs(c.created_at)));
  //   }
  //   return videos;
  // },
  // filters: (state) => {
  //   return state.filters;
  // },
  // hasFilters: (state) => {
  //   return Object.keys(state.filters).length > 0;
  // },
  // Return a list of recent videos.
  recent: (state, getters) => {
    // return state.allIds.map(id => getters.find(id)).filter(c => c.created_at)
    return state.recentIds.map(id => getters.find(id));
  },
  recentNakamalIds: (state, getters) => {
    return [...new Set(getters.recent.map((c) => c.nakamal.id))];
  },
  // Return a list of videos of a nakamal.
  nakamal: (state, getters) => nakamalId => {
    if (!state.byNakamalId[nakamalId]) return [];
    return state.byNakamalId[nakamalId].map(id => getters.find(id));
  },
  // Return a list of videos of a user.
  user: (state, getters) => userId => {
    return state.allIds.map(id => getters.find(id)).filter(c => c.user.id === userId);
  },
};

function commitAddVideo(video, commit) {
  // Normalize nested data and swap the nakamal object
  // in the API response with an ID reference.
  commit('add', normalizeRelations(video, ['nakamal', 'user']));
  // // Add or update the nakamal.
  if (video.nakamal) {
    commit('nakamal/add', video.nakamal, {
      root: true,
    });
  }
  commit('user/setUser', video.user, {
    root: true,
  });
};

const actions = {
  getAll: async ({ commit }) => {
    const response = await videosApi.getAll();
    const videos = response.data;
    videos.forEach((item) => {
      commitAddVideo(item, commit);
    });
  },
  getOne: async ({ commit }, id) => {
    let response = await videosApi.get(id);
    const video = response.data;
    commitAddVideo(video, commit);
  },
  getRecent: async ({ commit }) => {
    const threshold = 3; // XXX hardcoded value
    const response = await videosApi.getRecent();
    let items = response.data;
    if (!items.length < threshold) {
      const response = await videosApi.getAll({ limit: threshold })
      items = response.data;
    }
    items.forEach((item) => {
      commitAddVideo(item, commit);
    });
    commit('setRecentIds', items.map((i) => i.id));
  },
  // getNakamal: async ({ commit }, nakamalId) => {
  //   const response = await nakamalsApi.getCheckins(nakamalId);
  //   const videos = response.data;
  //   videos.forEach((item) => {
  //     commitAddVideo(item, commit);
  //   });
  // },
  getUser: async ({ commit }, userId) => {
    const response = await usersApi.getVideos(userId);
    const videos = response.data;
    videos.forEach((item) => {
      commitAddVideo(item, commit);
    });
  },
  add: async ({ commit, dispatch, rootState }, payload) => {
    try {
      let token = rootState.auth.token;
      let response = await videosApi.create(token, payload);
      const trip = response.data;
      commitAddVideo(trip, commit);
      dispatch('notify/add', {
        title: 'Video Uploaded',
        text: 'Your video will be ready to view soon; we have to process it first.',
        color: 'primary',
        duration: 5_000,
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
  remove: async ({ commit, dispatch, rootState }, id) => {
    try {
      let token = rootState.auth.token;
      await videosApi.remove(token, id);
      commit('remove', id);
      dispatch('notify/add', {
        title: 'Video Removed',
        text: 'Video removed from the system.',
        type: 'warning',
      }, { root: true });
    }
    catch (error) {
      console.log('Video remove error');
      await dispatch('auth/checkApiError', error, { root: true });
      dispatch('notify/add', {
        title: 'Not Allowed',
        text: error.response.data.detail,
        type: 'warning',
      }, { root: true });
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
    if (nId) {
      index = state.byNakamalId[nId].indexOf(id);
      if (index !== -1) {
        state.byNakamalId[nId].splice(index, 1);
      }
    }
    index = state.recentIds.indexOf(id);
    if (index !== -1) {
      state.recentIds.splice(index, 1);
    }
    state.allIds.splice(state.allIds.indexOf(id), 1);
    Vue.delete(state.byId, id);
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
