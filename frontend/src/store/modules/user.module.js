/* eslint-disable */
import usersApi from '@/api/users.js';

const initialState = () => ({
  users: [],
});

const state = initialState();

const getters = {
  find: (state) => (userId) => {
    const filteredUsers = state.users.filter((user) => user.id === userId);
    if (filteredUsers.length > 0) {
      return { ...filteredUsers[0] };
    }
  },
  list: (state) => state.users,
};

const actions = {
  getUsers: async ({ commit, dispatch, rootState }, payload) => {
    try {
      let token = rootState.auth.token;
      const response = await usersApi.getUsers(token, payload);
      if (response) {
        const users = response.data;
        commit('setUsers', users);
      }
    }
    catch (error) {
      await dispatch('auth/checkApiError', error, { root: true });
    }
  },
  getOne: async ({ commit }, id) => {
    try {
      const response = await usersApi.get(id);
      const user = response.data;
      commit('setUser', user);
    }
    catch (error) {
      console.log('error in get one user', error);
    }
  },
  updateUser: async ({ commit, dispatch, rootState }, { userId, payload }) => {
    try {
      let token = rootState.auth.token;
      const response = await usersApi.updateUser(token, userId, payload);
      commit('setUser', response.data);
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
      commit('setUser', response.data);
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
      commit('setUser', user);
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
  // TODO update below to be same as pattern seen in other modules
  setUsers(state, payload) {
    state.users = payload;
  },
  setUser(state, payload) {
    const users = state.users.filter((user) => user.id !== payload.id);
    users.push(payload);
    state.users = users;
  },
};

export default {
  actions,
  getters,
  mutations,
  namespaced: true,
  state,
};
