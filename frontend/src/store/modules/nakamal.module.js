/* eslint-disable */

import Vue from 'vue';
import ls from 'localstorage-slim';

import { loadRelations, normalizeRelations, resolveRelations, renameRelation } from '@/store/helpers';
import nakamalsApi from '@/api/nakamals';
import chiefsApi from '@/api/chiefs';

import {
  latLng,
} from 'leaflet';

const initialState = () => ({
  byId: {},
  allIds: [],
  selectedId: null,
  featuredId: null,
  filters: {},
});

const state = initialState();

const getters = {
  // Return a single nakamal with the given id.
  find: (state, _, __, rootGetters) => id => {
    // Swap ID referenes with the resolved image objects.
    // XXX here is the key to getting the profile returned with the nakamal... i think
    //   !!! and now it returns max stack exceeded since its an infinite loop nakamal -> image -> nakamal -> ...
    return resolveRelations(state.byId[id], [['chief', 'user']], rootGetters);
  },
  // Return a list of nakamals in the order of `allIds`.
  list: (state, getters) => {
    return state.allIds.map(id => getters.find(id));
  },
  filteredList: (state, getters) => {
    let nakamals = state.allIds.map(id => getters.find(id));
    if ('area' in state.filters) {
      nakamals = nakamals.filter((n) => n.area.id === state.filters.area);
    }
    if ('light' in state.filters) {
      nakamals = nakamals.filter((n) => n.light === state.filters.light);
    }
    if ('resources' in state.filters) {
      if (state.filters.resources.length > 0) {
        nakamals = nakamals.filter((n) => {
          if (n.resources.length > 0) {
            return state.filters.resources.every((rid) => n.resources.map((r) => r.id).indexOf(rid) > -1);
          }
        });
      }
    }
    if ('kava_source' in state.filters) {
      nakamals = nakamals.filter((n) => n.kava_source.id === state.filters.kava_source);
    }
    return nakamals;
  },
  filters: (state) => {
    return state.filters;
  },
  hasFilters: (state) => {
    return Object.keys(state.filters).length > 0;
  },
  total: (state) => {
    return state.allIds.length;
  },
  selected: (state, getters) => {
    if (state.selectedId === null) return null;
    return getters.find(state.selectedId);
  },
  featured: (state, getters) => {
    if (state.featuredId === null) return null;
    return getters.find(state.featuredId);
  },
  // TODO this is not efficient
  listByChief: (state, getters) => (id) => {
    return Object.keys(state.byId).filter((nid) => state.byId[nid].chief === id).map((nid) => getters.find(nid));
  },
};

function setLightBadge(light) {
  let lightBadge = {'color': null, icon: 'mdi-lightbulb-on'};
  switch(light) {
    case 'white':
      lightBadge['color'] = 'white';
      lightBadge['icon'] = 'mdi-lightbulb-on mdi-dark'
      break;
    case 'red':
      lightBadge['color'] = 'red';
      break;
    case 'orange':
      lightBadge['color'] = 'orange darken-1';
      break;
    case 'yellow':
      lightBadge['color'] = 'yellow';
      lightBadge['icon'] = 'mdi-lightbulb-on-outlight mdi-dark';
      break;
    case 'green':
      lightBadge['color'] = 'green darken-1';
      break;
    case 'blue':
      lightBadge['color'] = 'blue';
      break;
    case 'purple':
      lightBadge['color'] = 'purple';
      break;
    case 'pink':
      lightBadge['color'] = 'pink light-2';
      break;
    case 'candle':
      lightBadge['color'] = 'grey';
      lightBadge['icon'] = 'mdi-candle';
      break;
    case 'hurricane light':
      lightBadge['color'] = 'grey';
      lightBadge['icon'] = 'mdi-candle';
      break;
    case 'none':
      lightBadge['color'] = 'grey';
      lightBadge['icon'] = 'mdi-lightbulb-off';
      break;
    case 'other':
      lightBadge['color'] = 'grey';
      lightBadge['icon'] = 'mdi-lightbulb-question';
      break;
    default:
      lightBadge['color'] = 'grey';
      lightBadge['icon'] = 'mdi-lightbulb-question';
  }
  return lightBadge;  
};

function commitAddNakamal(nakamal, commit) {
  // Normalize nested data and swap the image object
  // in the API response with an ID reference.
  let normalizedNakamal = normalizeRelations(nakamal, ['chief']);
  normalizedNakamal = renameRelation(normalizedNakamal, [['profile_id', 'profile']]);
  commit('add', normalizedNakamal);
  // load relations - I don't think we need to load so much just to fetch a basic object
  // loadRelations(normalizedNakamal, { 'profile': 'image' }, rootGetters);
  // Add or update the user
  // if (nakamal.chief) {
  //   commit('user/setUser', nakamal.chief, {
  //     root: true,
  //   });
  // }
};

const loadingPromises = {
  nakamals: false,
  nakamal: {},
};

async function loadOrWait(loadingPromises, id, fetchFunction) {
  if (!loadingPromises[id]) {
    loadingPromises[id] = fetchFunction();
  }
  await loadingPromises[id];
};

const actions = {
  load: async ({ commit }) => {
    const cacheKey = 'nakamals';
    const cached = false; // ls.get('does-not-exist'); // cacheKey - replaced to remove cache
    if (cached) {
      return;
    } else {
      const resp = await nakamalsApi.getAll({});
      // ls.set(cacheKey, true, { ttl: 300 });
      const nakamals = resp.data
      nakamals.forEach((item) => {
        commitAddNakamal(item, commit);
      });
    }
  },
  loadOne: async ({ commit, dispatch, getters }, id) => {
    let nakamal;
    const cacheKey = `nakamals:${id}`;
    const cached = false; // ls.get('does-not-exist'); // cacheKey - replaced to remove cache
    if (cached) {
      nakamal = cached;
    } else {
      await loadOrWait(loadingPromises.nakamal, id, async () => {
        let resp = await nakamalsApi.get(id);
        nakamal = resp.data;
        // ls.set(cacheKey, nakamal, { ttl: 300 });
      });
    }
    commitAddNakamal(nakamal, commit);
    return Promise.resolve(getters.find(id));
  },
  update: async ({ commit, dispatch, rootState }, { nakamalId, payload }) => {
    try {
      let token = rootState.auth.token;
      const resp = await nakamalsApi.update(token, nakamalId, payload);
      const nakamal = resp.data;
      commitAddNakamal(nakamal, commit);
      dispatch('notify/add', {
        title: 'Success',
        text: 'Nakamal details have been updated.',
        type: 'primary',
        duration: 5_000,
      }, { root: true });
    }
    catch (error) {
      console.log('in update nakamal error', error);
      await dispatch('auth/checkApiError', error, { root: true });
    }
  },
  updateResources: async ({ commit, rootState }, { nakamalId, oldResources, resources }) => {
    try {
      const token = rootState.auth.token;
      const deleteList = oldResources.filter(id => resources.indexOf(id) === -1);
      const putlist = resources.filter(id => oldResources.indexOf(id) === -1);
      deleteList.forEach(id => {
        nakamalsApi.deleteResource(token, nakamalId, id);
      });
      putlist.forEach(id => {
        nakamalsApi.putResource(token, nakamalId, id);
      });
    }
    catch (error) {
      console.log('in update nakamal resource error', error);
      await dispatch('auth/checkApiError', error, { root: true });
    }
  },
  add: async ({ commit, dispatch, rootState }, payload) => {
    try {
      let token = rootState.auth.token;
      // Extract resources from payload if exists
      let resources = [];
      if ('resources' in payload) {
        resources = payload.resources;
        delete payload.resources;
      }
      // POST new nakamal
      let resp = await nakamalsApi.create(token, payload);
      const nakamal = resp.data;
      // PUT resources to new nakamal
      if (resources.length) {
        for (let i = 0; i < resources.length; i += 1) {
          await nakamalsApi.putResource(token, nakamal.id, resources[i]);
        };
      }
      commitAddNakamal(nakamal, commit);
      dispatch('notify/add', {
        title: 'Kava Bar Added',
        text: 'Thank you for sharing!',
        type: 'primary',
      }, { root: true });
    }
    catch (error) { 
      await dispatch('auth/checkApiError', error, { root: true });
    }
  },
  loadChiefNakamals: async ({ commit, getters }, userId) => {
    const cacheKey = `nakamals:chief:${userId}`;
    const cached = false; // ls.get('does-not-exist'); // cacheKey - replaced to remove cache
    if (cached) {
      return;
    } else {
      try {
        const resp = await chiefsApi.getUser(userId);
        const nakamals = resp.data;
        nakamals.forEach((item) => {
          commitAddNakamal(item, commit);
        });
        // ls.set(cacheKey, true, { ttl: 300 });
      } catch(error) {
        console.log('load cheif of nakamals error', error);
      }
    }
  },
  loadFeatured: async ({ commit, getters }) => {
    let nakamal;
    const cacheKey = `nakamals:featured`;
    const cached = false; // ls.get('does-not-exist'); // cacheKey - replaced to remove cache
    if (cached) {
      nakamal = cached;
    } else {
      try {
        const resp = await nakamalsApi.getFeatured();
        nakamal = resp.data;
        // ls.set(cacheKey, nakamal, { ttl: 300 });
      } catch(error) {
        console.log('featured nakamal error', error);
      }
    }
    commit('setFeatured', nakamal.id);
    commitAddNakamal(nakamal, commit);
    return Promise.resolve(getters.find(nakamal.id))
  },
  updateFeatured: async ({ commit }, id) => {
    await nakamalsApi.putFeatured(id);
    ls.remove('nakamals:featured');
    commit('setFeatured', id);
  },
  updateProfile: async ({ commit, dispatch, rootState }, { nakamalId, imageId }) => {
    try {
      let token = rootState.auth.token;
      const resp = await nakamalsApi.putProfileImage(token, nakamalId, imageId);
      const nakamal = resp.data;
      commitAddNakamal(nakamal, commit);
      // TODO this is fragile - multiple locations setting cache values
      // ls.set(`nakamals:${nakamalId}`, nakamal, { ttl: 300 });
      // ls.remove(`nakamals:${nakamalId}`);
    } catch (error) {
      console.log('set profile image for nakamal error', error);
    }
  },
  removeProfile: async ({ commit, dispatch, rootState }, { nakamalId, imageId }) => {
    try {
      let token = rootState.auth.token;
      const resp = await nakamalsApi.removeProfile(token, nakamalId, imageId)
      const nakamal = resp.data;
      commitAddNakamal(nakamal, commit);
    } catch (error) {
      console.log('remove profile image for nakamal error', error);
    }
  },
  select: async ({ commit, dispatch }, id) => {
    commit('select', id);
  },
  unselect: async ({ commit }) => {
    commit('unselect');
  },
  setFilter: ({ commit }, { key, value }) => {
    commit('setFilter', { key, value });
  },
  removeFilters: ({ commit }) => {
    commit('removeFilters');
  },
  remove: async ({ commit, dispatch, rootState }, id) => {
    try {
      let token = rootState.auth.token;
      await nakamalsApi.remove(token, id);
      // TODO this is fragile - multiple locations updating cache
      ls.remove(`nakamals:${id}`);
      commit('remove', id);
      dispatch('notify/add', {
        title: 'Kava Bar Removed',
        text: 'Kava bar removed from the system.',
        type: 'warning',
      }, { root: true });
    }
    catch (error) {
      await dispatch('auth/checkApiError', error, { root: true });
    }
  },
};

const mutations = {
  RESET (state) {
    const newState = initialState();
    Object.keys(newState).forEach(key => {
      state[key] = newState[key];
    });
  },
  add: (state, item) => {
    let i = {
      ...item,
      latLng: latLng(item.lat, item.lng),
      lightBadge: setLightBadge(item.light !== null ? item.light.toLowerCase() : null),
    };
    Vue.set(state.byId, i.id, i);
    if (state.allIds.includes(i.id)) return;
    state.allIds.push(i.id);
  },
  select: (state, id) => {
    state.selectedId = id;
  },
  unselect: (state) => {
    state.selectedId = null;
  },
  setFeatured: (state, id) => {
    state.featuredId = id;
  },
  setFilter: (state, { key, value }) => {
    if (value === []) {
      Vue.delete(state.filters, 'resources');
    }
    else {
      Vue.set(state.filters, key, value);
    }
  },
  removeFilters: (state) => {
    Vue.set(state, 'filters', {});
  },
  remove: (state, id) => {
    state.allIds.splice(state.allIds.indexOf(id), 1);
    Vue.delete(state.byId, id);
    state.selectedId = null;  // XXX why do this?
  }
};

export default {
  actions,
  getters,
  mutations,
  namespaced: true,
  state,
};
