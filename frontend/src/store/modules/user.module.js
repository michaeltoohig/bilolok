/* eslint-disable */

import ls from 'localstorage-slim';

import usersApi from '@/api/users.js';
import Vue from 'vue';

const initialState = () => ({
  byId: {},
  allIds: [],
});

const state = initialState();

const getters = {
  find: (state, _, __, rootGetters) => id => {
    return state.byId[id];
  },
  list: (state, getters) => {
    return state.allIds.map(id => getters.find(id));
  },
};

const actions = {
  getUsers: async ({ commit, dispatch, rootState }, payload) => {
    try {
      let token = rootState.auth.token;
      const response = await usersApi.getUsers(token, payload);
      if (response) {
        const users = response.data;
        users.forEach((item) => {
          commit('add', item);
        });
      }
    }
    catch (error) {
      await dispatch('auth/checkApiError', error, { root: true });
    }
  },
  loadOne: async ({ commit, getters, rootState }, id, payload) => {
    const token = rootState.auth.token;
    // Handle admin requesting user data
    if (payload && payload.auth) {
      console.log('getting user for admin')
      let resp = await usersApi.get(id, token, payload);
      const user = resp.data;
      return Promise.resolve(user);
    }
    
    // TODO handle network errors
    let user;
    const cacheKey = `users-one:${id}`;
    const cached = ls.get(cacheKey);
    if (cached) {
      user = cached;
    } else {
      let resp = await usersApi.get(id, token);
      user = resp.data;
      ls.set(cacheKey, user, { ttl: 300 });
    }
    commit('add', user);
    return Promise.resolve(getters.find(id));
    
    // TODO can't cache until we have endpoint for admin access to user vs normal user details api endpoint
    // This means we have to remove the payload option

    // try {
    //   let token = rootState.auth.token;
    //   const response = await usersApi.get(id, token, payload);
    //   const user = response.data;
    //   commit('add', user);
    //   return Promise.resolve(user);
    // }
    // catch (error) {
    //   console.log('error in get one user', error);
    //   await dispatch('auth/checkApiError', error, { root: true });
    // }
  },
  // TODO loadOne same as getOne but with cache
  updateUser: async ({ commit, dispatch, rootState }, { userId, payload }) => {
    try {
      let token = rootState.auth.token;
      const response = await usersApi.updateUser(token, userId, payload);
      commit('add', response.data);
      dispatch('notify/add', {
        title: 'Success',
        text: 'User details have been updated.',
        type: 'primary',
        duration: 5_000,
      }, { root: true });
    }
    catch (error) {
      console.log('in updateUser', error);
      await dispatch('auth/checkApiError', error, { root: true });
    }
  },
  createUser: async ({ commit, dispatch, rootState }, payload) => {
    try {
      let token = rootState.auth.token;
      const response = await usersApi.createUser(token, payload);
      commit('add', response.data);
      dispatch('notify/add', {
        title: 'Success',
        text: 'User has been created.',
        type: 'primary',
        duration: 5_000,
      }, { root: true });
    }
    catch (error) {
      console.log('in createUser', error);
      await dispatch('auth/checkApiError', error, { root: true });
    }
  },
  removeProfile: async ({ commit, dispatch, rootState }) => {
    try {
      let user = rootState.auth.user;
      let token = rootState.auth.token;
      const response = await usersApi.deleteProfile(user.id, token);
      user = response.data;
      commit('add', user);
    }
    catch (error) {
      console.log('in removeProfile', error);
      await dispatch('auth/checkApiError', error, { root: true });
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
  },
  // TODO update below to be same as pattern seen in other modules
  // setUsers(state, payload) {
  //   state.users = payload;
  // },
  // setUser(state, payload) {
  //   const users = state.users.filter((user) => user.id !== payload.id);
  //   users.push(payload);
  //   state.users = users;
  // },
};

export default {
  actions,
  getters,
  mutations,
  namespaced: true,
  state,
};
